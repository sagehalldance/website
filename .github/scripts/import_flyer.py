"""Fill in the dance schedule from the monthly flyer.

Staff upload the flyer they post on Instagram under "Monthly flyer" in the
editor, which saves its path in data/flyer.json. Gemini reads the flyer, this
script checks what it read, and rewrites that month in data/events.json.

Safety rules:
- Only the flyer's month changes. Other months are never touched.
- Venues and start times must be ones the editor offers (read from .pages.yml).
- Every date must fall on the weekday printed next to it on the flyer. That
  also picks the year, since flyers don't print one.
- Hand edits survive a re-upload: if the flyer still says TBA for a night
  someone already filled in, the filled-in time or venue stays, and so do
  titles, notes and "cancelled".
If any check fails, nothing is written and the script exits with an error.

Usage: python .github/scripts/import_flyer.py   (needs GEMINI_API_KEY)
Writes a commit message to $FLYER_COMMIT_MSG and a summary to $GITHUB_STEP_SUMMARY.
"""
import base64
import datetime
import io
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.request
import zoneinfo

API = "https://generativelanguage.googleapis.com/v1beta"
# The "-latest" names follow Google's current models, so a retired model
# doesn't break the import. The checks below catch a model that reads worse.
MODELS = os.environ.get("FLYER_MODELS", "gemini-flash-lite-latest,gemini-flash-latest").split(",")
DAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
TZ = zoneinfo.ZoneInfo("America/Denver")
FIELDS = ["date", "time", "venue", "title", "note", "cancelled"]

ROOT = pathlib.Path(__file__).resolve().parents[2]
EVENTS = ROOT / "data" / "events.json"
FLYER = ROOT / "data" / "flyer.json"


class FlyerError(Exception):
    """A problem with the flyer or what was read from it. Nothing gets written."""


def editor_choices():
    """Start times and venues offered by the schedule form in .pages.yml."""
    import yaml
    config = yaml.safe_load((ROOT / ".pages.yml").read_text(encoding="utf-8"))
    events = next(c for c in config["content"] if c["name"] == "events")
    night = next(f for f in events["fields"] if f["name"] == "events")
    fields = {f["name"]: f for f in night["fields"]}

    def values(name):
        return [v["value"] if isinstance(v, dict) else v for v in fields[name]["options"]["values"]]
    return values("time"), values("venue")


def prompt(times, venues):
    return f"""This image should be a monthly dance-schedule flyer for Sage Hall, a country swing dance in Cache Valley, Utah.
If it isn't a schedule flyer, set is_schedule_flyer to false and return no nights.
Otherwise:
- month: the month in the flyer's heading, 1-12.
- nights: one entry per night listed, in order.
  - day: the day of the month.
  - weekday: the weekday exactly as printed next to it (THUR means THU). Empty if none is printed.
  - time: the start time in 24-hour HH:MM, one of: {", ".join(times)}. "TBA" if the flyer gives no time.
  - venue: one of: {", ".join(venues)}. If the flyer names no venue, says TBD/TBA, or names a place not in that list, use "Location TBA".
  - title: empty for a regular night. If the line names a special event or group instead of (or besides) a venue, such as a fundraiser or a club night, put that name here.
  - note: empty unless the flyer gives extra information for that night beyond venue, time and title. "21+" next to Cache Bar is standard; leave it out.
  - cancelled: true only if the flyer says that night is cancelled.
Don't invent nights or details that aren't on the flyer."""


def schema(times, venues):
    night_fields = ["day", "weekday", "time", "venue", "title", "note", "cancelled"]
    return {
        "type": "OBJECT", "required": ["is_schedule_flyer", "month", "nights"],
        "propertyOrdering": ["is_schedule_flyer", "month", "nights"],
        "properties": {
            "is_schedule_flyer": {"type": "BOOLEAN"},
            "month": {"type": "INTEGER"},
            "nights": {"type": "ARRAY", "items": {
                "type": "OBJECT", "required": night_fields, "propertyOrdering": night_fields,
                "properties": {
                    "day": {"type": "INTEGER"},
                    "weekday": {"type": "STRING", "enum": DAYS + [""]},
                    "time": {"type": "STRING", "enum": times},
                    "venue": {"type": "STRING", "enum": venues},
                    "title": {"type": "STRING"},
                    "note": {"type": "STRING"},
                    "cancelled": {"type": "BOOLEAN"},
                }}},
        },
    }


def image_part(path):
    from PIL import Image
    with Image.open(path) as im:
        im = im.convert("RGB")
        im.thumbnail((1600, 1600))
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=88)
    return {"inline_data": {"mime_type": "image/jpeg", "data": base64.b64encode(buf.getvalue()).decode()}}


def ask_gemini(model, body):
    req = urllib.request.Request(
        f"{API}/models/{model}:generateContent", data=json.dumps(body).encode(),
        headers={"x-goog-api-key": os.environ["GEMINI_API_KEY"], "Content-Type": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                out = json.load(r)
            text = "".join(p.get("text", "") for p in out["candidates"][0]["content"]["parts"])
            return json.loads(text)
        except urllib.error.HTTPError as ex:
            # Rate limits and outages are worth a retry; anything else isn't.
            if ex.code not in (429, 500, 502, 503, 504) or attempt == 2:
                raise
            time.sleep(20 * (attempt + 1))


def pick_year(month, nights, today):
    """The year, nearest to today, in which every printed weekday matches its date."""
    printed = [(n["day"], n["weekday"]) for n in nights if n["weekday"]]
    for year in sorted(range(today.year - 1, today.year + 2),
                       key=lambda y: abs((datetime.date(y, month, 1) - today.replace(day=1)).days)):
        try:
            if all(DAYS[datetime.date(year, month, d).weekday()] == w for d, w in printed):
                if printed or year >= today.year:
                    return year
        except ValueError:
            continue  # e.g. Feb 29 in a non-leap year
    if not printed:
        raise FlyerError("couldn't work out the year")
    raise FlyerError("the dates don't match the weekdays printed on the flyer in any nearby year")


def to_events(reading, times, venues, today):
    """Check what the model read and turn it into events.json entries."""
    if not reading.get("is_schedule_flyer"):
        raise FlyerError("the image doesn't look like a schedule flyer")
    month, nights = reading.get("month"), reading.get("nights") or []
    if not isinstance(month, int) or not 1 <= month <= 12:
        raise FlyerError(f"couldn't read the month (got {month!r})")
    if not nights:
        raise FlyerError("no dance nights found on the flyer")
    for n in nights:
        if n["time"] not in times:
            raise FlyerError(f"day {n['day']}: start time {n['time']!r} isn't one the editor offers")
        if n["venue"] not in venues:
            raise FlyerError(f"day {n['day']}: venue {n['venue']!r} isn't one the editor offers")
    days = [n["day"] for n in nights]
    if len(set(days)) != len(days):
        raise FlyerError("the same day is listed twice")
    year = pick_year(month, nights, today)
    events = []
    for n in sorted(nights, key=lambda n: n["day"]):
        try:
            date = datetime.date(year, month, n["day"])
        except ValueError:
            raise FlyerError(f"{MONTHS[month - 1]} has no day {n['day']}")
        events.append({"date": date.isoformat(), "time": n["time"], "venue": n["venue"],
                       "title": n["title"].strip(), "note": n["note"].strip(),
                       "cancelled": bool(n["cancelled"])})
    return year, month, events


def merge(existing, new):
    """Replace one month's nights, keeping hand edits the flyer doesn't contradict."""
    old = {e["date"]: e for e in existing}
    merged, kept = [], []
    for n in new:
        o = old.get(n["date"])
        if o:
            if n["time"] == "TBA" and o.get("time", "TBA") != "TBA":
                n["time"] = o["time"]; kept.append(f"{n['date']} time")
            if n["venue"] == "Location TBA" and o.get("venue", "Location TBA") != "Location TBA":
                n["venue"] = o["venue"]; kept.append(f"{n['date']} venue")
            for k in ("title", "note"):
                if not n[k] and o.get(k):
                    n[k] = o[k]; kept.append(f"{n['date']} {k}")
            if o.get("cancelled") and not n["cancelled"]:
                n["cancelled"] = True; kept.append(f"{n['date']} cancelled")
        merged.append(n)
    removed = sorted(set(old) - {n["date"] for n in new})
    return merged, kept, removed


def describe(e):
    when = "time TBA" if e["time"] == "TBA" else datetime.time.fromisoformat(e["time"]).strftime("%I:%M %p").lstrip("0")
    bits = [e["title"], e["venue"], when, e["note"], "CANCELLED" if e["cancelled"] else ""]
    return f"{e['date']}: " + " · ".join(b for b in bits if b)


def main():
    flyer = json.loads(FLYER.read_text(encoding="utf-8")).get("image", "").strip()
    if not flyer:
        print("No flyer set in data/flyer.json; nothing to do.")
        return
    path = ROOT / flyer.lstrip("/")
    if not path.is_file():
        raise FlyerError(f"can't find the flyer image {flyer}")

    times, venues = editor_choices()
    body = {
        "contents": [{"role": "user", "parts": [{"text": prompt(times, venues)}, image_part(path)]}],
        "generationConfig": {"temperature": 0, "responseMimeType": "application/json",
                             "responseSchema": schema(times, venues)},
    }
    today = datetime.datetime.now(TZ).date()

    problems = []
    for model in MODELS:
        try:
            year, month, new = to_events(ask_gemini(model, body), times, venues, today)
            break
        except (FlyerError, urllib.error.URLError, KeyError, ValueError, TypeError) as ex:
            detail = ex.read().decode()[:300] if isinstance(ex, urllib.error.HTTPError) else ex
            problems.append(f"{model}: {detail}")
            print(f"{model} didn't work: {detail}", file=sys.stderr)
    else:
        raise FlyerError("couldn't read the flyer.\n" + "\n".join(problems))

    data = json.loads(EVENTS.read_text(encoding="utf-8"))
    prefix = f"{year}-{month:02d}-"
    others = [e for e in data["events"] if not e["date"].startswith(prefix)]
    existing = [e for e in data["events"] if e["date"].startswith(prefix)]
    merged, kept, removed = merge(existing, new)

    label = f"{MONTHS[month - 1]} {year}"
    lines = [f"Read {len(merged)} nights for {label} from {flyer} ({model}):", ""]
    lines += [f"- {describe(e)}" for e in merged]
    if kept:
        lines += ["", "Kept from hand edits (the flyer says TBA or leaves it blank): " + ", ".join(kept)]
    if removed:
        lines += ["", "Removed (not on the flyer): " + ", ".join(removed)]
    summary = "\n".join(lines)
    print(summary)

    if [{k: e.get(k) for k in FIELDS} for e in existing] == merged:
        print("\nThe schedule already matches the flyer; nothing to change.")
        return
    data["events"] = sorted(others + merged, key=lambda e: (e["date"], e["time"]))
    EVENTS.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    if os.environ.get("FLYER_COMMIT_MSG"):
        pathlib.Path(os.environ["FLYER_COMMIT_MSG"]).write_text(
            f"Fill in the {label} schedule from the flyer\n\n{summary}\n", encoding="utf-8")
    if os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as f:
            f.write(summary + "\n")


if __name__ == "__main__":
    try:
        main()
    except FlyerError as ex:
        print(f"Flyer import stopped: {ex}\nThe schedule was not changed.", file=sys.stderr)
        sys.exit(1)
