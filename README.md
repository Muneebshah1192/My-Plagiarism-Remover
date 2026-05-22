# Originality Studio Pro — Netlify Edition

A professional Netlify-ready rewriting workspace with two modes:

1. **Algorithm Rewriter** — works without any API key. It uses local phrase replacement, synonym rewriting, structure recasting, AI-style cleanup, grammar/punctuation polishing, bias-cleaning replacements, and similarity scoring.
2. **AI Rewrite Assist** — optional server-side AI rewriting through a Netlify Function. Add `GEMINI_API_KEY` in Netlify environment variables. If no key is present, the app automatically falls back to the algorithm engine.

> Important: This is an ethical originality and editing assistant. It does not check the internet, does not guarantee plagiarism removal, and should not be sold as a tool to bypass plagiarism or AI detectors. Users should cite borrowed ideas.

## Features

- Premium responsive SaaS-style interface
- Algorithm Rewriter with no API key
- Optional AI Rewrite Assist using a server-side environment key
- Academic, professional, simple, creative, and e-commerce modes
- Light, balanced, strong, and maximum rewrite strengths
- Bias Cleaner for common harmful/outdated terms
- TXT/MD upload
- Copy button
- TXT and HTML download
- Similarity estimate
- Originality lift score
- Phrase overlap score
- Readability score
- Local rewrite history
- Netlify Functions endpoint: `/api/rewrite`
- Node 20 pinned to avoid Node/npm deployment issues

## Netlify deployment

Use these settings:

```txt
Build command: npm run build
Publish directory: public
Functions directory: netlify/functions
Node version: 20
```

The included `netlify.toml`, `.nvmrc`, and `.node-version` already configure this.

## Optional AI setup

In Netlify:

1. Go to **Site configuration**.
2. Open **Environment variables**.
3. Add:

```txt
GEMINI_API_KEY = your_google_ai_studio_key
```

Optional:

```txt
GEMINI_MODEL = gemini-2.5-flash
```

Redeploy the site after adding the key.

## Local testing

Install Netlify CLI if needed:

```bash
npm install -g netlify-cli
```

Run:

```bash
npm run dev
```

Then open the local Netlify URL shown in the terminal.

## How the two engines work

### Algorithm Rewriter

This engine is rule-based. It improves text using:

- phrase-level rewriting
- synonym substitution
- sentence recasting
- product-title expansion
- AI-style phrase cleanup
- grammar and punctuation cleanup
- inclusive language cleanup
- similarity and phrase overlap scoring

### AI Rewrite Assist

This mode sends the input to a server-side Netlify Function. The API key stays on the server and is not exposed in browser JavaScript. The prompt asks the AI to rewrite ethically, preserve meaning, improve grammar, and keep citation-friendly wording.

## Selling suggestion

Recommended product name:

**Originality Studio Pro — Netlify Rewriter & Writing Polish Tool**

Recommended description:

"A Netlify-ready web app that helps users rewrite and polish text with a no-key algorithm engine and optional server-side AI Rewrite Assist. Includes similarity analysis, phrase overlap score, readability score, document upload, and download tools."

Avoid claims like:

- 100% plagiarism remover
- guaranteed AI detector bypass
- remove plagiarism without citation

Those claims are not honest and can create problems for buyers.
