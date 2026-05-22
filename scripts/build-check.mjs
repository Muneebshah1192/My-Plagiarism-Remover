import { access, stat } from 'node:fs/promises';

const required = [
  'public/index.html',
  'public/styles.css',
  'public/app.js',
  'public/engine.js',
  'netlify/functions/rewrite.mjs',
  'lib/engine.mjs'
];

for (const file of required) {
  await access(file);
  const info = await stat(file);
  if (!info.size) throw new Error(`${file} is empty`);
}

console.log('Build check passed. Netlify can publish the public folder.');
