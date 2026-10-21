# Launching sagehalldance.com

The goal: Sage Hall owns everything (the code, the domain and the hosting) in accounts under a business email, with nothing left on the friend's personal Hostinger account or server. Staff keep editing exactly as they do now.

**Who's needed:** the owner (to create accounts), whoever is helping with the setup, and the friend who holds the current Hostinger account (for steps 4 and 6).
**Cost:** the domain only, about $10–11 a year at Cloudflare. Hosting is free.
**Downtime:** none if you follow the order below.

---

## 1. Before you start: email and backups

- [ ] **Find out whether anyone uses an @sagehalldance.com email address.** If so, find out where that email is hosted (Hostinger, Google Workspace, etc.).
- [ ] **Have the friend send you a copy of the domain's DNS records** from Hostinger (hPanel → Domains → sagehalldance.com → DNS / Nameservers). A screenshot is fine. You'll need the **MX**, **TXT** (SPF/DKIM/verification) and any **CNAME** records for email or other services. Skip this and email can break.
- [ ] **Back up the current website** from the friend's server, just in case.
- [ ] **Check the domain can be transferred.** It can't move within 60 days of being registered or transferred. The friend can see the date in Hostinger.

## 2. Create Sage Hall's accounts

Use a shared business email that the owner controls, such as sagehallutah@gmail.com, not anyone's personal address.

- [ ] **GitHub:** create an account (or a free organization) for Sage Hall.
- [ ] **Cloudflare:** create an account at dash.cloudflare.com.

## 3. Move the code to Sage Hall's GitHub

- [ ] Alejandro transfers the repository: GitHub → `alejandro-usu/sagehall` → **Settings → General → Danger Zone → Transfer ownership**, to the Sage Hall account. Old links redirect automatically.
- [ ] Merge the launch version into `main`. This turns off the season switch, removes the "mock-up" footer note and drops the GitHub-Pages-only automation step.
- [ ] In `admin/index.html`, change the one line `var CMS_REPO = "alejandro-usu/sagehall/main";` to the new owner, e.g. `"sagehall/sagehall/main"`.
- [ ] Turn off GitHub Pages for the repo (**Settings → Pages → Unpublish**) once Cloudflare is live, so there's only one copy of the site.

## 4. Put the site on Cloudflare (still on the old domain setup)

- [ ] Cloudflare → **Workers & Pages → Create → Pages → Connect to Git**, then pick the `sagehall` repo and these settings:

  | Setting | Value |
  | --- | --- |
  | Production branch | `main` |
  | Framework preset | None |
  | Build command | `sh scripts/build.sh` |
  | Build output directory | `dist` |

- [ ] Open the `*.pages.dev` address Cloudflare gives you and check the site works.
- [ ] **Add the domain to Cloudflare:** dashboard → **Add a domain** → `sagehalldance.com` → Free plan. Cloudflare imports the existing DNS records. **Compare them with the copy from step 1** and add any email records that are missing.
- [ ] In the Pages project → **Custom domains**, add `sagehalldance.com` and `www.sagehalldance.com`.
- [ ] **The friend changes the nameservers** in Hostinger (Domains → sagehalldance.com → Nameservers) to the two Cloudflare gives you. Within a few hours, sagehalldance.com shows the new site.
- [ ] Send a test email to and from any @sagehalldance.com address.

## 5. Reconnect the staff editor

- [ ] Go to app.pagescms.org and sign in with the Sage Hall GitHub account. Install the Pages CMS app on the `sagehall` repo.
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
