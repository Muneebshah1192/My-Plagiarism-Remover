# Netlify Error Fix Guide

Your build log showed this error:

```txt
npm error Exit handler never called!
Error during npm install
```

That error happened before the website build started. The main cause was Netlify using Node 22 and npm 10.9.x, where npm can crash during dependency installation.

## What this fixed project changes

1. Pins Node to version 20.
2. Removes all external npm dependencies.
3. Removes the package lock problem.
4. Uses a simple build script instead of Vite.
5. Keeps Netlify Function support.

## Netlify settings to use

Build command:

```bash
npm run build
```

Publish directory:

```bash
dist
```

Environment variable, if Netlify still selects Node 22:

```txt
NODE_VERSION=20
```

## If your old deployment still fails

In Netlify:

1. Go to Site configuration.
2. Go to Build & deploy.
3. Open Environment variables.
4. Add `NODE_VERSION` with value `20`.
5. Clear cache and deploy again.

Also delete old `package-lock.json` from the GitHub repo if you are using the old version.
