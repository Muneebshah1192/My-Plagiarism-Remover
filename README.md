# Originality Assistant Pro — Netlify Edition

A premium-looking **React + Vite + Netlify Functions** web app for ethical rewriting, wording improvement, and similarity estimation.

This project uses a local JavaScript rewriting algorithm. It does **not** require OpenAI, Gemini, Google AI Studio, paid APIs, or any API key.

## What is included

- Modern SaaS-style responsive interface
- Netlify-ready deployment setup
- Serverless rewrite endpoint at `/api/rewrite`
- Browser fallback rewriting when running without Netlify Functions
- 4 writing modes: Academic, Professional, Simple, Creative
- 4 rewrite strengths: Light, Balanced, Strong, Maximum
- Similarity estimate between original and rewritten text
- Phrase overlap estimate
- Readability score
- Copy and TXT download buttons
- TXT upload support
- No database required
- No API key required

## Important ethical note

Do not market this as a guaranteed plagiarism bypass tool. No local rule-based tool can guarantee plagiarism removal, and plagiarism checkers compare against large private/public databases that this app does not access.

Recommended product positioning:

> Originality Assistant Pro helps users rewrite drafts for clarity, structure, and lower direct wording overlap. Users should review the output and cite any borrowed ideas or sources.

## Local setup

```bash
npm install
npm run dev
```

Open the local Vite URL shown in your terminal.

The app can run with browser fallback rewrite logic during normal Vite development.

## Netlify local development with functions

Install Netlify CLI if needed:

```bash
npm install -g netlify-cli
```

Then run:

```bash
npm run netlify-dev
```

This starts the frontend and Netlify Functions locally.

## Deploy to Netlify

### Option 1: GitHub + Netlify

1. Upload this folder to a GitHub repository.
2. Open Netlify.
3. Choose **Add new site** → **Import an existing project**.
4. Select your GitHub repository.
5. Netlify should use these settings from `netlify.toml`:
   - Build command: `npm run build`
   - Publish directory: `dist`
   - Functions directory: `netlify/functions`
6. Deploy.

### Option 2: Manual deploy

```bash
npm install
npm run build
```

Upload the generated `dist` folder to Netlify. For full serverless API support, Git-based deployment is recommended because it includes the `netlify/functions` folder.

## File structure

```txt
originality-assistant-netlify-pro/
├── netlify/
│   └── functions/
│       └── rewrite.mjs
├── public/
│   ├── _headers
│   └── _redirects
├── shared/
│   └── rewriterCore.mjs
├── src/
│   ├── App.jsx
│   ├── main.jsx
│   └── styles.css
├── index.html
├── netlify.toml
├── package.json
└── README.md
```

## Gumroad title ideas

- Originality Assistant Pro — Netlify Ready Rewriter Tool
- AI-Style Rewriter Web App Without API Keys
- Local Paraphrasing & Similarity Checker Web App

## Gumroad description

Originality Assistant Pro is a ready-to-deploy React and Netlify web app that helps users rewrite text for better clarity, improved structure, and lower direct wording overlap. It includes a premium responsive UI, local rewriting algorithm, similarity estimate, readability score, TXT upload, copy, and download features.

No paid AI API key is required.

## Customization ideas

- Add Stripe payments
- Add user accounts
- Add rewrite history
- Add PDF/DOCX export
- Add Gemini/OpenAI API as a premium optional mode
- Add admin dashboard
- Add daily usage limit
- Add multilingual dictionaries

## License

You may sell your customized version as a digital product. Replace this section with your own license terms before selling.
