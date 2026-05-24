# TextForge Studio — Professional No-API Text Tools Website

Made by **Muneeb Haider**

TextForge Studio is a platform-neutral Python Flask web application for rewriting, polishing, analyzing, and exporting text. It is designed as a complete writing workspace that can be deployed on any Python-friendly hosting platform or run locally.

## What's New in This Version

- Professional non-neon UI with a cleaner SaaS-style layout
- Logo integrated across landing page, login, and dashboard
- Responsive design for desktop, tablet, and mobile
- Collapsible sidebar for a cleaner workspace
- Dark mode / light mode toggle
- Improved spacing, contrast, buttons, cards, and analytics panel
- Output area now has a separate tinted background
- Faster front-end status feedback with response time display
- Tool search and category navigation improvements
- 99 working text tools organized by category
- Stronger rewriting behavior for product-title and keyword-heavy text
- PDF, DOCX, TXT, and Markdown export
- TXT, MD, PDF, and DOCX import

## Included Categories

- Smart Writing
- Content Intelligence
- SEO & Blogging
- Student Tools
- Business Tools
- Social Media
- Document Tools

## Important Note

This project uses local Python logic and does not require external AI APIs. Because it does not connect to a web plagiarism database, it should be marketed as an originality assistant, rewriting workspace, or text transformation toolkit rather than a guaranteed plagiarism remover.

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

## Files

- `app.py` — Flask backend, login, upload/export routes, history, settings
- `text_engine.py` — all local text-processing algorithms and tool logic
- `templates/` — HTML pages
- `static/style.css` — complete professional responsive styling
- `static/app.js` — dashboard interactions, dark mode, sidebar collapse, tool execution
- `static/assets/logo.svg` — integrated website logo

## Customizing the Logo

Replace this file with your own logo if needed:

```text
static/assets/logo.svg
```

Keep the same filename to update the logo everywhere automatically.
