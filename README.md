# Originality Studio Pro

A professional Python web app for text rewriting, grammar polishing, AI-style cleanup, product copy rewriting, summaries, bullet points, titles, keyword extraction, and bias-aware wording cleanup.

## Main features

- User signup and login
- Dashboard with multiple working text tools
- Algorithm Rewriter that works without any API key
- AI Rewrite Assist with optional Gemini or OpenAI API key
- API settings from the three-dot menu in the dashboard
- History panel for recent generations
- TXT/MD upload
- TXT download
- Similarity estimate, originality lift, phrase overlap, readability score
- SQLite database included automatically
- Clean Python backend and premium responsive UI

## Tools included

1. Algorithm Rewriter
2. AI Rewrite Assist
3. AI-Style Cleaner
4. Grammar & Punctuation Polish
5. Bias Cleaner
6. Product Description Rewriter
7. Smart Summarizer
8. Text Expander
9. Bullet Point Generator
10. Title Generator
11. Keyword Extractor

## Important note

This app rewrites and improves text, but no tool can honestly guarantee perfect originality or check every source on the internet. Users should add citations when the original idea, fact, or research belongs to another source.

## Local setup

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

Install requirements:

```bash
pip install -r requirements.txt
```

Run:

```bash
python app.py
```

Open:

```text
http://127.0.0.1:5000
```

## Production run

```bash
gunicorn app:app
```

## Environment variables

Create a `.env` file using `.env.example` as a guide.

Required for production:

```env
SECRET_KEY=your-long-random-secret-key
```

Optional AI keys:

```env
GEMINI_API_KEY=your-key
OPENAI_API_KEY=your-key
DEFAULT_AI_PROVIDER=gemini
GEMINI_MODEL=gemini-1.5-flash
OPENAI_MODEL=gpt-4o-mini
```

Users can also add their own API key from the app's three-dot settings menu.

## Deploying from GitHub

This is a Python Flask application. Deploy it on any host that supports Python web apps, WSGI/Gunicorn, or Docker.

Common build/start settings:

```text
Install command: pip install -r requirements.txt
Start command: gunicorn app:app
```

For Docker hosting, use the included `Dockerfile`.

## First user becomes admin

The first account created in the app receives the `admin` role. Later users receive the `user` role.

## Custom branding

You can change app name in `.env`:

```env
APP_NAME=Your Brand Name
```

You can edit styles in:

```text
static/css/styles.css
```

You can edit tools and algorithms in:

```text
core/rewrite_engine.py
core/ai_clients.py
```
