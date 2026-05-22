# Originality Assistant Pro — Netlify Fixed Version

A Netlify-ready originality assistant and ethical rewriting tool with a polished interface, local rewrite engine, and similarity scoring.

## Why this version fixes Netlify install errors

This build uses **zero npm dependencies**, so Netlify does not need to download React, Vite, or any package bundle. It also pins Node to version 20 through:

- `.nvmrc`
- `.node-version`
- `netlify.toml` build environment
- `package.json` engines

This avoids common Node 22 / npm install crashes such as `npm error Exit handler never called!`.

## Features

- Professional SaaS-style UI
- Works on Netlify
- No paid API required
- No npm dependencies
- Netlify Function endpoint: `/api/rewrite`
- Browser fallback engine
- Academic, Professional, Human Natural, Simple, and Creative modes
- Light, Balanced, Strong, and Maximum rewrite strengths
- Similarity estimate
- Originality lift score
- Phrase overlap score
- Readability score
- TXT upload
- TXT download
- Copy button

## Run locally

```bash
npm install
npm run dev
```

Open:

```txt
http://localhost:8888
```

## Deploy to Netlify

1. Upload this project to GitHub.
2. Go to Netlify.
3. Import the GitHub repository.
4. Use these settings:
   - Build command: `npm run build`
   - Publish directory: `dist`
5. Deploy.

Netlify should automatically read `netlify.toml`.

## Important note

This tool does not check the internet, Turnitin, Google Scholar, or academic databases. It estimates similarity between the original text and rewritten output. Always cite sources when ideas are borrowed.

Recommended selling name:

**Originality Assistant Pro — Netlify Ready Rewriter & Similarity Checker**

Do not honestly sell any local tool as a “100% plagiarism remover.” A safer promise is:

> Rewrite content for clearer structure, smoother wording, and reduced direct textual overlap.
