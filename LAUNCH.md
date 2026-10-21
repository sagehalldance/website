# Launching sagehalldance.com

The goal: Sage Hall owns everything (the code, the domain and the hosting) in accounts under a business email, with nothing left on the friend's personal Hostinger account or server. Staff keep editing exactly as they do now.

**Who's needed:** the owner (to create accounts), whoever is helping with the setup, and the friend who holds the current Hostinger account (for steps 4 and 6).
**Cost:** the domain only, about $10–11 a year at Cloudflare. Hosting is free.
**Downtime:** none if you follow the order below.
**Status (Oct 21, 2026):** steps 1–3 partly done and step 5 started (marked below). The repo now lives at `sagehalldance/website`. Nobody uses @sagehalldance.com email, so there are no email records to protect.

---

## 1. Before you start: backups and the domain

- [x] **Find out whether anyone uses an @sagehalldance.com email address.** Confirmed: no one does.
- [ ] **Have the friend screenshot the domain's DNS records** in Hostinger (hPanel → Domains → sagehalldance.com → DNS): an actual picture of the record list. Cloudflare's copy in step 4 is a best guess and can miss records; this is what you check it against. Low-stakes: a public lookup on Oct 21 found only Hostinger defaults (A `157.173.212.97`, `www` CNAME, Hostinger mail MX/SPF, DMARC `p=none`) and no verification records. It isn't needed before adding the domain to Cloudflare, only before the nameserver switch.
- [ ] **Back up the current website** from the friend's server, just in case.
- [x] **Check the domain can be transferred.** It can't move within 60 days of being registered or transferred. Public registry record (Oct 21): registered at Hostinger on May 15, 2025, so it's clear to transfer. It **expires May 15, 2027** and has the usual transfer lock on. The friend keeps control of it until step 6, so do step 6 soon after launch rather than near the expiry date.

## 2. Create Sage Hall's accounts

Use a shared business email that the owner controls, such as sagehallutah@gmail.com, not anyone's personal address.

- [x] **GitHub:** account created for Sage Hall.
- [x] **Cloudflare:** account created.

## 3. Move the code to Sage Hall's GitHub

- [x] Alejandro transfers the repository to the Sage Hall account. Done: `alejandro-usu/sagehall` is now **`sagehalldance/website`** (transferred, then renamed). Old repo links redirect automatically, but the old mock-up address `alejandro-usu.github.io/sagehall/` doesn't. The mock-up is now at <https://sagehalldance.github.io/website/>.
- [x] Put the docs, `scripts/build.sh` and the editor-link setting on `main`, so Cloudflare can build from `main`.
- [ ] Merge the rest of the launch branch (`ccr-b6d97a4a-1cdu41`) into `main` once the `website.sagehalldance.workers.dev` site checks out, after the nameserver switch in step 4 and right before attaching the domain to the Worker. This turns off the season switch, removes the "mock-up" footer note and drops the GitHub-Pages-only automation step.
- [x] In `admin/index.html`, set `var CMS_REPO` to the new owner/repo/branch (`"sagehalldance/website/main"`). It's live on `main`.
- [ ] Turn off GitHub Pages for the repo (**Settings → Pages → Unpublish**) once Cloudflare is live, so there's only one copy of the site.
- [ ] **Make the repo private** (**Settings → General → Danger Zone → Change repository visibility**), once Cloudflare is live and GitHub Pages is off. On a free account a private repo can't serve GitHub Pages, so doing this sooner takes the mock-up offline. Cloudflare and Pages CMS both work with private repos.

## 4. Put the site on Cloudflare (still on the old domain setup)

- [x] Cloudflare → **Workers & Pages → Create**, connect GitHub, pick `sagehalldance/website`, and set the build command to `sh scripts/build.sh` (the deploy command stays `npx wrangler deploy`). Cloudflare now sets these sites up as a **Worker**, and the screen doesn't ask for an output folder. `wrangler.jsonc` in the repo sets it to `dist`, so only the public site is published. Done Oct 21: the Worker is named `website`.
- [x] Open <https://website.sagehalldance.workers.dev> and check the site works: the schedule, `/admin` and a theme link such as `?theme=fall`. Also check that repo files like `/AGENTS.md` and `/.git/config` return "not found". Checked Oct 21 on desktop and phone.
- [x] **Add the domain to Cloudflare:** dashboard → **Add a domain** → `sagehalldance.com` → Free plan. Done Oct 21, and it shows as "Pending" until the nameservers change. The records are trimmed to four:

  | Record | Value | Notes |
  | --- | --- | --- |
  | A `sagehalldance.com` | `157.173.212.97` | Old site. DNS only (grey cloud) until the domain moves to the Worker |
  | CNAME `www` | `sagehalldance.com` | DNS only, same reason |
  | TXT `sagehalldance.com` | `v=spf1 -all` | The domain sends no email, so spoofed mail gets rejected |
  | TXT `_dmarc` | `v=DMARC1; p=reject` | Same reason |

  The Hostinger mail records were deleted (2 MX, SPF, `autoconfig`, `autodiscover`, and 3 `hostingermail-*` DKIM CNAMEs) because nobody uses email. For email later, see *Email (later)* below. The scan can miss records, so compare this list with the friend's screenshot from step 1.
- [ ] **The friend changes the nameservers** in Hostinger (Domains → sagehalldance.com → Nameservers): replace `ns1.dns-parking.com` and `ns2.dns-parking.com` with **`carol.ns.cloudflare.com`** and **`terin.ns.cloudflare.com`**. DNSSEC is already off (checked Oct 21), so nothing else needs changing in Hostinger. After they save, click **I updated my nameservers** in Cloudflare (Domains → sagehalldance.com → Overview), which just makes it check sooner. Cloudflare emails when the domain is **Active**, usually within an hour, at most a day. The old site stays up throughout.
- [ ] **Merge the launch branch** (step 3), so the live version has no mock-up note or season switch.
- [ ] In the `website` Worker → **Settings → Domains & Routes → Add → Custom domain**, add `sagehalldance.com`, then `www.sagehalldance.com`. This only works once the domain is Active. It replaces the old A and `www` records, and sagehalldance.com shows the new site within minutes.

## 5. Reconnect the staff editor

- [x] Go to app.pagescms.org and sign in with the Sage Hall GitHub account. Install the Pages CMS app on the `website` repo. Done Oct 20.
- [ ] Open the repo → **Collaborators**, and invite each staff member by email. Re-invite anyone who was invited before the move.
- [ ] Do a test edit, such as a word in the announcement. Save, and check it shows on sagehalldance.com within a minute or two.
- [ ] Upload one test photo under **Dancers of the Week & photos**. Then check the repo's **Actions** tab: "Shrink uploaded photos" should run and finish green. Delete the test photo afterwards.

## 6. Transfer the domain to Sage Hall

The site is already live at this point; this step moves who owns the domain.

- [ ] **The friend, in Hostinger:** turn off the domain lock, then copy the **transfer (EPP/auth) code** and send it to you.
- [ ] **Cloudflare → Domain Registration → Transfer Domains:** select sagehalldance.com, enter the code and pay for the transfer, which includes a year of renewal.
- [ ] Approve the confirmation email if one arrives. Transfers take up to 5 days, and the site stays up the whole time.
- [ ] Turn on **auto-renew** in Cloudflare so the domain never lapses.

## 7. Wrap up

- [ ] Once the domain shows in Cloudflare's Domain Registration list, the friend can cancel the old hosting and server.
- [ ] Set the default look under **Site settings → Site theme** (spring, summer, fall or winter).
- [ ] Confirm the facts on the README's "Before showing this to Sage Hall" list: prices, venue addresses, the Fairgrounds address (450 vs 490 S 500 W) and the about-section facts.
- [ ] Keep a note of which email owns the GitHub and Cloudflare accounts, and turn on two-factor sign-in for both.

## Email (later)

Nobody uses @sagehalldance.com email today. Set it up only after the domain is Active on Cloudflare.

- **Forwarding only (free):** Cloudflare → sagehalldance.com → **Email → Email Routing**. For example, forward `info@` to the shared Gmail. Cloudflare adds its own MX and SPF records and replaces `v=spf1 -all`. Replies come from the Gmail address.
- **Send and receive as @sagehalldance.com (paid):** Google Workspace, Microsoft 365 or Zoho. Add the provider's MX, SPF and DKIM records in Cloudflare. Set `_dmarc` to `v=DMARC1; p=none` while testing, then back to `p=reject` once mail flows.
