import { rewriteText } from '../../public/core/rewriterCore.mjs';

export async function handler(event) {
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    const payload = JSON.parse(event.body || '{}');
    const text = String(payload.text || '').slice(0, 30000);
    const mode = String(payload.mode || 'professional');
    const intensity = String(payload.intensity || 'balanced');
    const result = rewriteText(text, { mode, intensity });

    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-store'
      },
      body: JSON.stringify(result)
    };
  } catch (error) {
    return {
      statusCode: 500,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ error: 'Rewrite failed', details: error.message })
    };
  }
}
