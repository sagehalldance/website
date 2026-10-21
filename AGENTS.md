# AGENTS.md: Sage Hall website

Briefing for any coding agent (Claude Code, Codex, Cursor, Copilot…) or person picking this project up on any computer. Read this first, then `README.md` (how the site works) and `LAUNCH.md` (go-live checklist).

**At the end of every work session:** update the *Status*, *To do* and *Decision log* sections below, commit, and push. That's what makes the project resumable from another machine.

---

## What this is

A redesign of the website for **Sage Hall**, a country swing dance in Logan / Cache Valley, Utah (Instagram/Facebook `@sage.hall.utah`; current domain sagehalldance.com). Alejandro (GitHub `alejandro-usu`) is building it as a volunteer for the owner.

Goals:
1. An easy-to-update dance schedule (the monthly flyer, but live).
2. Staff sign-in to edit everything without code.
3. Instagram reels, a weekly *Dancers of the Week* spotlight and weekly photos.
4. Seasonal looks: spring, summer, fall and winter.

## Status (update every session)

*Last updated: 2026-10-21*

- **Mock-up is live** on GitHub Pages at <https://alejandro-usu.github.io/sagehall/>, served from `main` (commit `52f33b9`). It shows a "concept mock-up" footer note and the season switch, for demos.
- **The launch version is ready but NOT on `main`.** It's commit `bc3b287` on branch `ccr-b6d97a4a-1cdu41` (a name left over from the cloud session). It removes the mock-up note, hides the season switch, adds `scripts/build.sh` and `LAUNCH.md`, and drops the GitHub-Pages-only workflow step. Merge it into `main` only when the move to Cloudflare starts (LAUNCH.md step 3), because it changes the live demo.
- **Hosting decision:** move everything to Sage Hall-owned accounts. Code goes to GitHub, and hosting, DNS and the domain go to Cloudflare. Today the domain sits on the owner's friend's personal Hostinger account and server.
- **Owner-provided content** is in: September and October 2026 schedules, the high-res logo, and the confirmed facts listed below.

## To do

### Launch (details in LAUNCH.md)
- [x] Confirm whether anyone uses @sagehalldance.com email. Nobody does.
- [x] Create Sage Hall GitHub and Cloudflare accounts.
- [ ] Friend: screenshot Hostinger DNS records; back up the old site; check the domain is more than 60 days past its last registration or transfer.
- [ ] Transfer the repo `alejandro-usu/sagehall` to the Sage Hall GitHub account.
- [ ] Merge the launch version into `main`; set `CMS_REPO` in `admin/index.html` to the new owner/repo/branch.
- [ ] Cloudflare Pages: connect the repo (build `sh scripts/build.sh`, output `dist`), add the domain, friend switches nameservers.
- [ ] Reconnect Pages CMS under the Sage Hall account; invite staff; test an edit and a photo upload (check the Actions tab).
- [ ] Transfer the domain from Hostinger to Cloudflare Registrar; turn on auto-renew.
- [ ] Unpublish GitHub Pages; friend cancels the old hosting; set the default season; turn on 2FA everywhere.

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
- **Keep paths relative.** No leading `/`: the mock-up lives under `/sagehall/` on GitHub Pages. Pages CMS media output is `assets/uploads` (no slash) for the same reason.
- **Text from JSON goes in via `textContent`** (the `h()` helper in `main.js`), never `innerHTML`. Image URLs pass through `mediaUrl()`, which allows only relative paths and https.
- **Color tokens:** `--primary` / `--accent` are UI accents that themes change. `--denim`, `--sage`, `--copper`, `--gold` and `--rose` are **venue colors** and must look the same in every theme. Don't recolor a venue to theme the UI.
- **Dates and times are Cache Valley wall-clock (America/Denver)**, stored as `date` `YYYY-MM-DD` plus `time` `HH:MM` or `"TBA"`. Venue `"Location TBA"` is allowed.
- **After editing `.pages.yml`**, validate it against Pages CMS's schema. There's a known-good config in git history if something breaks.
- **No test suite.** Verify changes by serving locally and checking desktop (about 1280px) and phone (about 390px) widths in all four themes, with no horizontal scroll and no console errors. Screenshot with Playwright if available.
- **Content honesty:** don't invent facts about Sage Hall, such as prices, claims or names. Mark anything unverified in *Content to confirm*.

### Git workflow
- `main` is what's published. Do work on a branch, and merge (fast-forward) into `main` only when Alejandro says to ("merge it").
- Write clear commit messages explaining why. Push at the end of every session.

## Decision log

Newest first. Record decisions and the reasons behind them here, not a running chat transcript; git history already records *what* changed.

| Date | Decision | Why |
| --- | --- | --- |
| 2026-10-21 | Move code to a Sage Hall GitHub account; host on Cloudflare Pages; transfer domain to Cloudflare Registrar | Get off the friend's personal Hostinger account/server; static site needs no paid hosting; at-cost domain renewals; one business-owned account |
| 2026-10-21 | Launch build copies only public files to `dist/` | Keep `.pages.yml`, README and workflows off the live site |
| 2026-10-04 | Dancers of the Week and weekly photos added; ship empty | New tradition, no fake names. Photos auto-shrunk with GPS stripped; consent and takedown note on the site |
| 2026-10-03 | Spring redone as a Cache Valley mountains-and-forest theme | Owner's request; replaced blossoms and tulips |
| 2026-10-03 | Four seasonal themes on one page (Classic renamed Summer); `?theme=classic` still works | One site and one data source; easy to demo and switch seasonally |
| 2026-10-03 | Removed "biggest dance floor in Utah"; stat is "400+" | Unverifiable self-claim; owner confirmed 400+ |
| 2026-10-03 | Separate date and time fields with TBA options; "Location TBA" venue | October flyer had TBA nights; Pages CMS required both fields |
| 2026-10-03 | Pages CMS for staff editing | Free; staff invited by email with no GitHub account; edits commit to the repo |
| 2026-10-03 | Static HTML/CSS/JS, no framework or build | Simple to host anywhere and easy for anyone to maintain |
