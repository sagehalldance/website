# AGENTS.md: Sage Hall website

Briefing for any coding agent (Claude Code, Codex, Cursor, Copilot…) or person picking this project up on any computer. Read this first, then `README.md` (how the site works) and `LAUNCH.md` (go-live checklist).

**At the end of every work session:** update the *Status*, *To do* and *Decision log* sections below, commit, and push. That's what makes the project resumable from another machine.

---

## What this is

A redesign of the website for **Sage Hall**, a country swing dance in Logan / Cache Valley, Utah (Instagram/Facebook `@sage.hall.utah`; current domain sagehalldance.com). Alejandro (GitHub `amontesinos`, a collaborator) is building it as a volunteer for the owner. The repo belongs to Sage Hall's GitHub account: `sagehalldance/website`.

Goals:
1. An easy-to-update dance schedule (the monthly flyer, but live).
2. Staff sign-in to edit everything without code.
3. Instagram reels, a weekly *Dancers of the Week* spotlight and weekly photos.
4. Seasonal looks: spring, summer, fall and winter.

## Status (update every session)

*Last updated: 2026-10-21*

- **Repo moved (Oct 20):** `alejandro-usu/sagehall` was transferred to Sage Hall's account and renamed **`sagehalldance/website`**. GitHub Pages carried over. The Pages CMS app is installed on the new repo, and the `/admin` editor links point to it.
- **Mock-up is live** on GitHub Pages at <https://sagehalldance.github.io/website/>, served from `main`. It shows a "concept mock-up" footer note and the season switch, for demos. The old `alejandro-usu.github.io/sagehall/` address is gone and doesn't redirect.
- **Most of the launch version is on `main`:** the docs (`AGENTS.md`, `CLAUDE.md`, `LAUNCH.md`), `scripts/build.sh` for Cloudflare, and `CMS_REPO` in `admin/index.html`. **Four changes still wait** on branch `ccr-b6d97a4a-1cdu41` (a name left over from the cloud session): removing the mock-up footer note (`index.html`), hiding the season switch (`data/site.json`), and dropping the GitHub-Pages republish step from `.github/workflows/shrink-photos.yml` and `.github/workflows/import-flyer.yml`. Merge that branch into `main` after the nameserver switch, right before attaching sagehalldance.com to the Worker (LAUNCH.md step 4). Merging earlier changes the live demo and stops uploaded photos from republishing on GitHub Pages. Don't edit docs on that branch; edit them on `main`.
- **Schedule source: Google Calendar.** The site reads the public **Sage Hall Dances** calendar (Sage Hall Google account; ID and browser API key in `data/site.json` → `google_calendar`). The owner adds nights by giving the flyer to Gemini (gemini.google.com) with the prompt on `/admin`. Gemini app output goes unchecked: on the first try it invented 9 PM starts for both October TBD nights and put the fundraiser in the location, so someone has to check TBD nights. `data/events.json` and the flyer import are now only the fallback, shown if Google can't be reached. Note: if the calendar loads but is *empty*, the site shows an empty schedule, not the fallback.
- **Hosting decision:** move everything to Sage Hall-owned accounts. Code goes to GitHub, and hosting, DNS and the domain go to Cloudflare. Today the domain sits on the owner's friend's personal Hostinger account and server.
- **Owner-provided content** is in: September and October 2026 schedules, the high-res logo, and the confirmed facts listed below.

## To do

### Launch (details in LAUNCH.md)
- [x] Confirm whether anyone uses @sagehalldance.com email. Nobody does.
- [x] Create Sage Hall GitHub and Cloudflare accounts.
- [x] Domain is clear to transfer: registered at Hostinger May 15, 2025; expires May 15, 2027.
- [ ] Friend: screenshot Hostinger DNS records; back up the old site.
- [x] Transfer the repo to the Sage Hall GitHub account. It's now `sagehalldance/website`.
- [x] Set `CMS_REPO` in `admin/index.html` to `sagehalldance/website/main` (on the launch branch).
- [x] Put the docs, `scripts/build.sh` and the `CMS_REPO` change on `main`.
- [ ] Merge the rest of the launch branch into `main` (footer note, season switch, republish steps in the photo and flyer workflows), after the nameserver switch and right before attaching the domain.
- [x] Cloudflare: repo connected as the Worker `website` (build `sh scripts/build.sh`; `wrangler.jsonc` publishes `dist/`). Test URL: <https://website.sagehalldance.workers.dev>.
- [x] Check the workers.dev site on desktop and phone.
- [x] Cloudflare: domain added (Pending). Old A and `www` records kept as DNS only; email records removed; SPF `-all` and DMARC `p=reject` set.
- [ ] Friend switches nameservers to `carol.ns.cloudflare.com` and `terin.ns.cloudflare.com`. Once Cloudflare says Active, merge the launch branch, then attach the domain to the Worker as a custom domain.
- [x] Install the Pages CMS app on `sagehalldance/website` under the Sage Hall account.
- [ ] Pages CMS: invite (or re-invite) staff; test an edit and a photo upload (check the Actions tab).
- [ ] Transfer the domain from Hostinger to Cloudflare Registrar; turn on auto-renew.
- [ ] Unpublish GitHub Pages; friend cancels the old hosting; set the default season; turn on 2FA everywhere.
- [ ] Make the repo private, only after Cloudflare is live and GitHub Pages is unpublished. A private repo on a free account can't serve GitHub Pages.

### Content to confirm with the owner
- [ ] Admission ($6 students / $7 general, from older listings).
- [ ] Addresses for Mountain Valley Athletics and Cache Bar (blank, so Directions searches by name).
- [ ] Fairgrounds address: 450 S 500 W (one source) vs 490 S 500 W (2023 Cache Valley Daily). Also whether the Indoor Barn is at the same fairgrounds.
- [ ] About-section facts: opened 2021, founders Josh Lyman and Manuel Carias-Pineda.
- [ ] Remaining first-timer and FAQ copy (placeholder wording).
- [ ] Times and places for the Whispering Canyon Fundraiser (Oct 15) and USU Swing Club (Oct 22), which were TBA on the flyer.
- [ ] Instagram handle `@sage.hall.utah` and the Facebook link.
- [ ] November schedule, when the flyer comes out.

### Ideas / later
- A plainer one-page launch summary for the owner (offered, not requested yet).
- Google Calendar mode exists but isn't set up (README §3).
- Email for the domain: Cloudflare Email Routing (free forwarding) or a paid mailbox. See LAUNCH.md *Email (later)*.

## Confirmed facts (from the owner; don't change without asking)

- Tuesday nights and Cache Bar nights start with instruction for beginners.
- Fairgrounds and Mountain Valley Athletics nights end at midnight. Cache Bar end times vary.
- "400+ dancers a week" is the approved stat. The "biggest dance floor in Utah" claim was removed on purpose; don't bring it back.
- Cache Bar nights are 21+.
- Dancers of the Week is a **new tradition**. It ships empty ("first pick coming soon"); never add placeholder names.
- No one uses @sagehalldance.com email.

## How the project works

- **Plain static site, no build step for development.** `index.html`, `assets/css/*.css`, `assets/js/main.js`, and `admin/index.html` (staff sign-in page).
- **Content is JSON** that staff edit through **Pages CMS** (app.pagescms.org; config in `.pages.yml`):
  - `data/events.json`: the schedule.
  - `data/site.json`: announcement, theme, venues, reels, FAQ, Google Calendar.
  - `data/weekly.json`: Dancers of the Week and weekly photos.
  - `data/flyer.json`: the monthly flyer. Saving it runs `.github/workflows/import-flyer.yml`, which has Gemini read the flyer and rewrite that month in `data/events.json`, committing straight to `main` as github-actions[bot]. The safety rules are in the docstring of `.github/scripts/import_flyer.py`. On failure nothing changes, and a GitHub issue is opened. It needs the repo secret `GEMINI_API_KEY` (free tier, Google AI Studio). Models are set by `FLYER_MODELS`, default `gemini-flash-lite-latest,gemini-flash-latest`.
- **Uploads** land in `assets/uploads/`. `.github/workflows/shrink-photos.yml` resizes them to 1600px and strips EXIF/GPS.
- **Themes:** summer is the base `styles.css`. `theme-spring.css`, `theme-fall.css` and `theme-winter.css` layer on top, scoped to `html[data-theme=...]`. An inline script in `index.html` applies the theme before first paint.

### Run and preview locally
```sh
python3 -m http.server 8000      # then open http://localhost:8000
```
Opening `index.html` from disk won't work, because the browser blocks loading the JSON files. Useful URL params:
- `?today=2026-10-12` pretends it's that date.
- `?theme=fall` forces a season.

### Conventions and gotchas
- **Keep paths relative.** No leading `/`: the mock-up lives under `/website/` on GitHub Pages. Pages CMS media output is `assets/uploads` (no slash) for the same reason.
- **Text from JSON goes in via `textContent`** (the `h()` helper in `main.js`), never `innerHTML`. Image URLs pass through `mediaUrl()`, which allows only relative paths and https.
- **Color tokens:** `--primary` / `--accent` are UI accents that themes change. `--denim`, `--sage`, `--copper`, `--gold` and `--rose` are **venue colors** and must look the same in every theme. Don't recolor a venue to theme the UI.
- **Dates and times are Cache Valley wall-clock (America/Denver)**, stored as `date` `YYYY-MM-DD` plus `time` `HH:MM` or `"TBA"`. Venue `"Location TBA"` is allowed.
- **After editing `.pages.yml`**, validate it against Pages CMS's schema. There's a known-good config in git history if something breaks.
- **No test suite.** Verify changes by serving locally and checking desktop (about 1280px) and phone (about 390px) widths in all four themes, with no horizontal scroll and no console errors. Screenshot with Playwright if available.
- **Content honesty:** don't invent facts about Sage Hall, such as prices, claims or names. Mark anything unverified in *Content to confirm*.

### Git workflow
- `main` is what's published. **During launch, work directly on `main`.** Once feature requests start coming in, do each one on its own branch and merge (fast-forward) into `main` only when Alejandro says to ("merge it").
- **Accounts:** `sagehalldance` owns the repo; keep its login for settings and secrets only. Alejandro works as the collaborator **`amontesinos`** and is assigned the issues opened by failed flyer imports (repo variable `FLYER_ISSUE_ASSIGNEE`, default `amontesinos`). Commits should be credited to him: on a new computer, run `git config user.name amontesinos` and `git config user.email 14097725+amontesinos@users.noreply.github.com`. Ignore `alejandromontesinos-dev`: it's an account Alejandro can't sign in to, created by accident from a Git sign-in pop-up. A few Oct 20–21 commits are credited to it.
- Write clear commit messages explaining why. Push at the end of every session.

## Decision log

Newest first. Record decisions and the reasons behind them here, not a running chat transcript; git history already records *what* changed.

| Date | Decision | Why |
| --- | --- | --- |
| 2026-10-21 | Schedule comes from the public Sage Hall Dances Google Calendar, filled by the owner through the Gemini app; the flyer import is kept as a fallback | The owner already uses Google and Gemini on their phone, and dancers get Subscribe links. The fallback keeps the site working if Google is unreachable. The trade-off: the Gemini app's output isn't checked automatically |
| 2026-10-21 | Alejandro is a collaborator (`amontesinos`, write access); Sage Hall's `sagehalldance` account stays the owner | Sage Hall owns the code and secrets and can remove access with one click; Alejandro's commits and issue assignments are under his own name; no shared password |
| 2026-10-21 | Monthly flyer → schedule import with Gemini, committing straight to `main` (no PR review) | The owner already posts a flyer on Instagram each month, so uploading it once in the editor replaces typing the nights in by hand. Gemini's free tier is enough; GitHub Models was retired Jul 30, 2026. Tested live: Sept and Oct flyers read 120/120 fields right, a re-upload kept hand edits, and a non-flyer was refused. The checks are why no review step is needed |
| 2026-10-21 | Host on a Cloudflare **Worker** with static assets, not a Pages project | Cloudflare's Git import now creates Workers. It's free for a static site and supports custom domains. `wrangler.jsonc` pins the published folder to `dist/`, because the first auto-configured deploy published the whole repo, `.git/` included |
| 2026-10-21 | Work directly on `main` during launch; use feature branches once requests come in. Docs, build script and `CMS_REPO` moved to `main`; footer, season switch and photo workflow wait for the Cloudflare cutover | Launching as we go. The held changes would alter the live demo or break photo republishing on GitHub Pages |
| 2026-10-21 | Repo transferred to the `sagehalldance` account and renamed `website`; to be made private after launch | Sage Hall owns the code (LAUNCH.md step 3). Private waits until GitHub Pages is no longer needed |
| 2026-10-21 | Move code to a Sage Hall GitHub account; host on Cloudflare Pages; transfer domain to Cloudflare Registrar | Get off the friend's personal Hostinger account/server; static site needs no paid hosting; at-cost domain renewals; one business-owned account |
| 2026-10-21 | Launch build copies only public files to `dist/` | Keep `.pages.yml`, README and workflows off the live site |
| 2026-10-04 | Dancers of the Week and weekly photos added; ship empty | New tradition, no fake names. Photos auto-shrunk with GPS stripped; consent and takedown note on the site |
| 2026-10-03 | Spring redone as a Cache Valley mountains-and-forest theme | Owner's request; replaced blossoms and tulips |
| 2026-10-03 | Four seasonal themes on one page (Classic renamed Summer); `?theme=classic` still works | One site and one data source; easy to demo and switch seasonally |
| 2026-10-03 | Removed "biggest dance floor in Utah"; stat is "400+" | Unverifiable self-claim; owner confirmed 400+ |
| 2026-10-03 | Separate date and time fields with TBA options; "Location TBA" venue | October flyer had TBA nights; Pages CMS required both fields |
| 2026-10-03 | Pages CMS for staff editing | Free; staff invited by email with no GitHub account; edits commit to the repo |
| 2026-10-03 | Static HTML/CSS/JS, no framework or build | Simple to host anywhere and easy for anyone to maintain |
