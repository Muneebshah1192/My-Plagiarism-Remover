import { rewriteText } from '../../shared/rewriterCore.mjs';

export async function handler(event) {
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 204,
      headers: corsHeaders(),
      body: ''
    };
  }

  if (event.httpMethod !== 'POST') {
    return json({ error: 'Only POST requests are allowed.' }, 405);
  }

  try {
    const body = JSON.parse(event.body || '{}');
    const text = String(body.text || '').slice(0, 15000);
    const mode = String(body.mode || 'professional');
    const intensity = String(body.intensity || 'strong');

    if (!text.trim()) {
      return json({ error: 'Please provide text to rewrite.' }, 400);
    }

    const result = rewriteText(text, { mode, intensity });
    return json(result, 200);
  } catch (error) {
    return json({ error: 'Rewrite failed. Check your input and try again.', detail: error.message }, 500);
  }
}

function corsHeaders() {
  return {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Content-Type': 'application/json'
  };
}

function json(payload, statusCode = 200) {
  return {
    statusCode,
    headers: corsHeaders(),
    body: JSON.stringify(payload)
  };
}
