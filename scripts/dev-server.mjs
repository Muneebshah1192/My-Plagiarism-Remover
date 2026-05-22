import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { extname, join, normalize } from 'node:path';
import { dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { rewriteText } from '../public/core/rewriterCore.mjs';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const publicDir = join(root, 'public');
const port = process.env.PORT || 8888;

const mime = {
  '.html': 'text/html;charset=utf-8',
  '.css': 'text/css;charset=utf-8',
  '.js': 'text/javascript;charset=utf-8',
  '.mjs': 'text/javascript;charset=utf-8',
  '.json': 'application/json;charset=utf-8',
  '.txt': 'text/plain;charset=utf-8',
  '.svg': 'image/svg+xml'
};

function send(res, status, body, type = 'text/plain;charset=utf-8') {
  res.writeHead(status, { 'Content-Type': type, 'Cache-Control': 'no-store' });
  res.end(body);
}

async function readBody(req) {
  const chunks = [];
  for await (const chunk of req) chunks.push(chunk);
  return Buffer.concat(chunks).toString('utf8');
}

createServer(async (req, res) => {
  try {
    const url = new URL(req.url, `http://localhost:${port}`);

    if (url.pathname === '/api/rewrite' && req.method === 'POST') {
      const payload = JSON.parse(await readBody(req) || '{}');
      const result = rewriteText(String(payload.text || '').slice(0, 30000), {
        mode: payload.mode || 'professional',
        intensity: payload.intensity || 'balanced'
      });
      return send(res, 200, JSON.stringify(result), 'application/json;charset=utf-8');
    }

    let requested = url.pathname === '/' ? '/index.html' : url.pathname;
    requested = normalize(requested).replace(/^\.+/, '');
    const filePath = join(publicDir, requested);

    if (!filePath.startsWith(publicDir) || !existsSync(filePath)) {
      const html = await readFile(join(publicDir, 'index.html'), 'utf8');
      return send(res, 200, html, 'text/html;charset=utf-8');
    }

    const data = await readFile(filePath);
    return send(res, 200, data, mime[extname(filePath)] || 'application/octet-stream');
  } catch (error) {
    return send(res, 500, `Server error: ${error.message}`);
  }
}).listen(port, () => {
  console.log(`Originality Assistant running at http://localhost:${port}`);
});
