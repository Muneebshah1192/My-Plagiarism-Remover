import { rewriteText, cleanSpacing, applyPatterns, AI_STYLE_PATTERNS, BIAS_PATTERNS, similarityScores, readability, createNotes } from '../../lib/engine.mjs';

const headers = {
  'Content-Type': 'application/json; charset=utf-8',
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'Content-Type',
  'Access-Control-Allow-Methods': 'POST, OPTIONS'
};

function json(statusCode, body) {
  return { statusCode, headers, body: JSON.stringify(body) };
}

function buildPrompt(text, options) {
  const modeGuide = {
    academic: 'formal academic wording, clear claims, careful structure, citation-friendly phrasing',
    professional: 'professional business wording, clean grammar, natural flow, concise structure',
    simple: 'simple clear wording, short sentences, easy vocabulary, clean punctuation',
    creative: 'natural expressive wording, varied sentence rhythm, fresh phrasing',
    ecommerce: 'conversion-friendly product copy, polished product description, clean feature wording'
  };
  const strengthGuide = {
    light: 'lightly rewrite while keeping most wording familiar',
    balanced: 'rewrite sentences and replace common phrases while preserving meaning',
    strong: 'substantially restructure sentences and replace repeated wording',
    maximum: 'deeply rephrase structure, wording, and flow while preserving factual meaning'
  };
  return `You are an ethical rewriting and editing assistant. Rewrite the user's text to improve originality, clarity, grammar, punctuation, and natural flow. Preserve factual meaning, names, numbers, product names, and important claims. Do not fabricate facts. Do not claim plagiarism is removed. Do not help bypass academic integrity systems. If ideas appear borrowed, keep the writing citation-friendly and remind that citations may be needed only if useful in the rewritten text. Neutralize biased or harmful wording when present.\n\nMode: ${modeGuide[options.mode] || modeGuide.professional}\nStrength: ${strengthGuide[options.strength] || strengthGuide.strong}\n\nReturn only the rewritten text, no intro, no bullet explanation.\n\nTEXT:\n${text}`;
}

async function aiRewrite(text, options) {
  const key = process.env.GEMINI_API_KEY || process.env.GOOGLE_API_KEY;
  if (!key) return null;
  const model = process.env.GEMINI_MODEL || 'gemini-2.5-flash';
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${encodeURIComponent(model)}:generateContent?key=${encodeURIComponent(key)}`;
  const payload = {
    contents: [{ role: 'user', parts: [{ text: buildPrompt(text, options) }] }],
    generationConfig: {
      temperature: options.strength === 'maximum' ? 0.75 : options.strength === 'strong' ? 0.55 : 0.35,
      topP: 0.92,
      maxOutputTokens: 4096
    }
  };
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!response.ok) {
    const msg = await response.text().catch(() => 'AI provider error');
    throw new Error(`Gemini request failed: ${response.status} ${msg.slice(0, 300)}`);
  }
  const data = await response.json();
  const out = data?.candidates?.[0]?.content?.parts?.map(p => p.text || '').join('\n').trim();
  if (!out) throw new Error('AI provider returned empty output.');
  let rewritten = cleanSpacing(out.replace(/^```[a-z]*\n?/i, '').replace(/```$/g, ''));
  rewritten = applyPatterns(rewritten, AI_STYLE_PATTERNS);
  if (options.biasClean) rewritten = applyPatterns(rewritten, BIAS_PATTERNS);
  const metrics = similarityScores(text, rewritten);
  return {
    rewritten,
    metrics: { ...metrics, readability: readability(rewritten) },
    notes: createNotes(metrics, options, true),
    engineUsed: 'ai'
  };
}

export async function handler(event) {
  if (event.httpMethod === 'OPTIONS') return { statusCode: 204, headers, body: '' };
  if (event.httpMethod !== 'POST') return json(405, { error: 'Method not allowed' });
  try {
    const body = JSON.parse(event.body || '{}');
    const text = String(body.text || '').slice(0, 30000);
    const options = {
      engine: body.engine || 'algorithm',
      mode: body.mode || 'professional',
      strength: body.strength || 'strong',
      biasClean: body.biasClean !== false
    };
    if (!text.trim()) return json(400, { error: 'Please provide text to rewrite.' });

    if (options.engine === 'ai') {
      try {
        const ai = await aiRewrite(text, options);
        if (ai) return json(200, ai);
      } catch (err) {
        const fallback = rewriteText(text, options);
        fallback.engineUsed = 'algorithm-fallback';
        fallback.notes.unshift('AI Rewrite Assist failed or is not configured, so the algorithm fallback was used. Check GEMINI_API_KEY and GEMINI_MODEL in Netlify environment variables.');
        fallback.debug = process.env.NODE_ENV === 'development' ? String(err.message || err) : undefined;
        return json(200, fallback);
      }
    }

    return json(200, rewriteText(text, options));
  } catch (error) {
    return json(500, { error: 'Rewrite failed.', detail: String(error.message || error) });
  }
}
