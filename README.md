# TextForge Studio — Hybrid Subscription Pro

Made for: **Syed Muneeb**

TextForge Studio is a platform-neutral Flask web app for writing, rewriting, SEO, student, business, social media, and document text workflows. This upgraded version includes:

- User signup/login
- Simple math CAPTCHA on login and signup
- 1-day trial for new users
- Free and premium plan system
- Daily character limits
- Premium tool locking
- Admin dashboard with user stats
- Manual payment proof approval
- Configurable Stripe, Lemon Squeezy, Paddle, PayPal, Payoneer, Bank, and EasyPaisa display options
- EasyPaisa screenshot upload and admin approval workflow
- AdSense settings panel
- `ads.txt`, `robots.txt`, and `sitemap.xml`
- Algorithm mode without API
- Gemini API mode using the user's own API key
- Hybrid mode fallback: if API fails, built-in algorithm still runs
- TXT, MD, DOCX, and PDF import/export support

## Run Locally

```bash
pip install -r requirements.txt
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Production Start Command

```bash
gunicorn app:app
```

## Subscription Workflow

1. User signs up and receives a 1-day trial.
2. Free users are limited by the daily character setting in the admin panel.
3. Premium tools and Gemini API mode are locked after the trial unless the user upgrades.
4. Admin enables payment methods from `/admin`.
5. User opens `/subscribe` and pays through an enabled method.
6. For manual methods like EasyPaisa, user uploads proof.
7. Admin approves the proof in `/admin`.
8. User account automatically changes to premium for the configured duration.

## Payment Notes

This project does not store card details. Stripe, Lemon Squeezy, and Paddle are configured as checkout links that you paste in admin settings. EasyPaisa, Payoneer, PayPal, and bank methods are manual payment/proof workflows.

## Gemini API Mode

Users can paste their own Gemini / Google AI Studio API key in workspace settings. API mode is available to trial/premium users. If API mode fails, the app falls back to the local algorithm.

## AdSense Setup

From `/admin`, add:

- AdSense global script
- Publisher ID for `/ads.txt`
- Header ad HTML
- Tool area ad HTML
- Sidebar ad HTML
- Footer ad HTML

AdSense approval depends on Google's review. This website includes policy pages, guides, sitemap, robots.txt, and ad slots to make it more ready.

## Final Admin/UI Repair Notes

This build includes:

- Admin-only dashboard access through `/admin`.
- Admin account has unlimited usage and all premium tools unlocked.
- Admin panel is visible only for the configured admin user on the dashboard.
- User list, signup emails, payment proof approvals, subscription limits, ad settings, and payment methods are managed from the admin panel.
- Improved light/dark color system with readable text on every page.
- Fixed settings dropdown z-index so logout/settings appear above cards.
- Improved input/output text contrast and output panel tint.
- Manual EasyPaisa proof approval upgrades users to premium automatically.


## UI v2 Bright Professional Update
This build uses a bright gradient interface by default, improved dark mode contrast, larger readable typography, clearer sidebar cards, fixed dropdown z-index, and highly visible input/output text areas. Browser theme storage now uses a new key so old dark-mode cache does not force the previous heavy dark interface for returning testers.

## Multi-page UI upgrade
This version separates the workspace into professional pages:

- `/tools` — category index page
- `/tools/<category>` — clean category tool listing page
- `/tool/<tool_id>` — focused tool workspace with input, output, controls, analytics, history, export, and Algorithm/Gemini API mode

The main navigation includes a **Tools** dropdown that shows every category. Users choose a category first, then choose a tool, then work on a focused tool page instead of seeing everything on one crowded dashboard.

## Bright UI + Payment Patch
This build fixes the latest visual issues by replacing the previous heavy dashboard styling with a clearer light-blue/white gradient interface by default. Text contrast, card spacing, tool cards, pricing, subscription, admin pages, editor textareas, settings dropdowns, and mobile responsiveness were improved.

Payment defaults were updated:

- EasyPaisa: `0340-545-3639`, Account Holder: `Manza Zahoor`
- SadaPay: `03140895219`, Account Holder: `syed Muneeb Haider Shah`

The admin panel now also includes SadaPay, Mashreq Neo Bank, and Allied Bank toggles/details so you can configure them later.
