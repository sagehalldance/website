# Launching sagehalldance.com

The goal: Sage Hall owns everything (the code, the domain and the hosting) in accounts under a business email, with nothing left on the friend's personal Hostinger account or server. Staff keep editing exactly as they do now.

**Who's needed:** the owner (to create accounts), whoever is helping with the setup, and the friend who holds the current Hostinger account (one visit to Hostinger, step 5).
**Cost:** the domain only, about $10–11 a year at Cloudflare. Hosting is free.
**Downtime:** fine. Neither the old site nor the mock-up is in use, so the steps below skip the precautions that would keep the old site up during the switch.
**Status (Oct 21, 2026):** steps 1–4 are done. Next is the friend's visit to Hostinger (step 5). The repo lives at `sagehalldance/website`, and the schedule comes from the Sage Hall Dances Google Calendar.

---

## 1. Before you start

- [x] **Find out whether anyone uses an @sagehalldance.com email address.** Confirmed: no one does.
- [x] **Check the domain can be transferred.** It can't move within 60 days of being registered or transferred. Public registry record (Oct 21): registered at Hostinger on May 15, 2025, so it's clear to transfer. It **expires May 15, 2027**. The transfer lock is on, as usual; the friend turns it off in step 5.
- [x] ~~Screenshot the DNS records in Hostinger.~~ Skipped: it only mattered for keeping live services running through the switch. A public lookup on Oct 21 found only Hostinger defaults (the old site's A record, `www`, and unused mail records) and no verification records.
- [ ] *Optional:* **back up the current website** from the friend's server, but only if the owner wants anything from it. It's gone once the friend cancels the hosting (step 7).

## 2. Create Sage Hall's accounts

Use a shared business email that the owner controls, such as sagehallutah@gmail.com, not anyone's personal address.

- [x] **GitHub:** account `sagehalldance` created for Sage Hall.
- [x] **Cloudflare:** account created.
- [x] **Google:** Sage Hall account created. It holds the Sage Hall Dances calendar and the Gemini key for the flyer backup.

## 3. Move the code to Sage Hall's GitHub

- [x] Transfer the repository to the Sage Hall account. Done: `alejandro-usu/sagehall` is now **`sagehalldance/website`** (transferred, then renamed). Old repo links redirect automatically. The mock-up is at <https://sagehalldance.github.io/website/>.
- [x] Put the docs, `scripts/build.sh` and the editor-link setting (`CMS_REPO` in `admin/index.html`) on `main`, so Cloudflare can build from `main`.
- [x] Alejandro is a collaborator as `amontesinos`; `sagehalldance` stays the owner.

## 4. Put the site on Cloudflare

- [x] Cloudflare → **Workers & Pages → Create**, connect GitHub, pick `sagehalldance/website`, and set the build command to `sh scripts/build.sh` (the deploy command stays `npx wrangler deploy`). Cloudflare sets this up as a **Worker** named `website`. `wrangler.jsonc` in the repo tells it to publish only `dist/`, the public site.
- [x] Check <https://website.sagehalldance.workers.dev> works on desktop and phone, and that repo files like `/AGENTS.md` and `/.git/config` return "not found". Checked Oct 21.
- [x] **Add the domain to Cloudflare** (Free plan). Done Oct 21. It shows as "Pending" until the nameservers change in step 5. The records are trimmed to four:

  | Record | Value | Notes |
  | --- | --- | --- |
  | A `sagehalldance.com` | `157.173.212.97` | The old site. Replaced when the domain is attached to the Worker (step 6) |
  | CNAME `www` | `sagehalldance.com` | Same |
  | TXT `sagehalldance.com` | `v=spf1 -all` | The domain sends no email, so spoofed mail gets rejected |
  | TXT `_dmarc` | `v=DMARC1; p=reject` | Same reason |

  The Hostinger mail records were deleted (2 MX, SPF, `autoconfig`, `autodiscover`, and 3 `hostingermail-*` DKIM CNAMEs) because nobody uses email. For email later, see *Email (later)* below.

## 5. The friend: one visit to Hostinger

Everything the friend needs to do, in one sitting (hPanel → Domains → sagehalldance.com):

- [ ] **Change the nameservers:** replace `ns1.dns-parking.com` and `ns2.dns-parking.com` with **`carol.ns.cloudflare.com`** and **`terin.ns.cloudflare.com`**. DNSSEC is already off (checked Oct 21), so nothing else needs changing.
- [ ] **Turn off the domain lock** (also called transfer lock).
- [ ] **Copy the transfer code** (EPP or auth code) and send it to you privately. Treat it like a password.

Message you can send them:

> Could you do three things for sagehalldance.com in Hostinger (hPanel → Domains → sagehalldance.com)? 1) Change the nameservers to `carol.ns.cloudflare.com` and `terin.ns.cloudflare.com`. 2) Turn off the domain/transfer lock. 3) Send me the transfer (EPP/auth) code. Thanks! Please don't cancel the hosting yet; I'll let you know when the transfer is done.

The nameserver change has to happen first: Cloudflare only accepts a transfer for a domain that's already Active on Cloudflare. After they save, click **I updated my nameservers** in Cloudflare (Domains → sagehalldance.com → Overview), which just makes it check sooner.

## 6. When Cloudflare says the domain is Active

Cloudflare emails when it's Active, usually within an hour, at most a day. These can then happen in any order:

- [ ] **Start the transfer:** Cloudflare → **Domain Registration → Transfer Domains** → select sagehalldance.com, enter the code, and pay (it includes a year of renewal). Approve the confirmation email if one arrives.
- [ ] **Merge the launch branch** (`ccr-b6d97a4a-1cdu41`) into `main`. It removes the "mock-up" footer note, hides the season switch, and drops the GitHub Pages republish steps from the photo and flyer workflows.
- [ ] **Attach the domain:** `website` Worker → **Settings → Domains & Routes → Add → Custom domain**, add `sagehalldance.com`, then `www.sagehalldance.com`. This replaces the old A and `www` records, and sagehalldance.com shows the new site within minutes.
- [ ] **Check the live site:** the schedule loads from Google Calendar (the "Subscribe" links appear under it), `/admin` opens, and the themes work.

## 7. When the transfer finishes (up to 5 days)

The site is already live on sagehalldance.com; this only changes who owns the domain.

- [ ] Check sagehalldance.com appears under Cloudflare → **Domain Registration**, then turn on **auto-renew** so it never lapses.
- [ ] Tell the friend they can cancel the old hosting and server (after the optional backup in step 1).

## 8. Staff

- [ ] **Pages CMS:** open the repo → **Collaborators** and invite each staff member by email. Re-invite anyone invited before the move.
- [ ] Do a test edit, such as a word in the announcement. Save, and check it shows on the site within a minute or two.
- [ ] Upload one test photo under **Dancers of the Week & photos**. Check the repo's **Actions** tab: "Shrink uploaded photos" should run and finish green. Delete the test photo afterwards.
- [ ] **Google Calendar:** share the **Sage Hall Dances** calendar with staff who'll add nights (Settings → Share with specific people → **Make changes to events**).

## 9. Wrap up

- [ ] Turn off GitHub Pages (**Settings → Pages → Unpublish**), so there's only one copy of the site.
- [ ] **Make the repo private** (**Settings → General → Danger Zone → Change repository visibility**). Do this only after GitHub Pages is off: on a free account a private repo can't serve GitHub Pages. Cloudflare and Pages CMS both work with private repos.
- [ ] Set the default look under **Site settings → Site theme** (spring, summer, fall or winter).
- [ ] Confirm the facts on the README's "Before showing this to Sage Hall" list: prices, venue addresses, the Fairgrounds address (450 vs 490 S 500 W) and the about-section facts.
- [ ] Keep a note of which email owns the GitHub, Cloudflare and Google accounts, and turn on two-factor sign-in for all three.

## Email (later)

Nobody uses @sagehalldance.com email today. Set it up only after the domain is Active on Cloudflare.

- **Forwarding only (free):** Cloudflare → sagehalldance.com → **Email → Email Routing**. For example, forward `info@` to the shared Gmail. Cloudflare adds its own MX and SPF records and replaces `v=spf1 -all`. Replies come from the Gmail address.
- **Send and receive as @sagehalldance.com (paid):** Google Workspace, Microsoft 365 or Zoho. Add the provider's MX, SPF and DKIM records in Cloudflare. Set `_dmarc` to `v=DMARC1; p=none` while testing, then back to `p=reject` once mail flows.
