import { rewriteText, similarityScores, readability, cleanSpacing } from './engine.js';

const $ = (id) => document.getElementById(id);
const els = {
  input: $('inputText'), output: $('outputText'), mode: $('mode'), strength: $('strength'), biasClean: $('biasClean'),
  rewriteBtn: $('rewriteBtn'), polishBtn: $('polishBtn'), swapBtn: $('swapBtn'), clearBtn: $('clearBtn'), sampleBtn: $('sampleBtn'),
  fileInput: $('fileInput'), copyBtn: $('copyBtn'), downloadTxtBtn: $('downloadTxtBtn'), downloadHtmlBtn: $('downloadHtmlBtn'),
  inputStats: $('inputStats'), outputStats: $('outputStats'), engineUsed: $('engineUsed'), notes: $('notes'), toast: $('toast'),
  similarity: $('similarity'), lift: $('lift'), phraseOverlap: $('phraseOverlap'), readability: $('readability'),
  similarityBar: $('similarityBar'), liftBar: $('liftBar'), phraseBar: $('phraseBar'), readabilityBar: $('readabilityBar'),
  historyList: $('historyList'), clearHistoryBtn: $('clearHistoryBtn')
};

let engine = 'algorithm';
let busy = false;

const sample = `LAURA GELLER Baked Icons Complete Full Face Palette, Medium | All-in-One Makeup Palette with Baked Foundations, Blush, Bronzer, Highlighter, Eyeshadows | Coverage for Mature Skin | Travel-Friendly`;

function words(text) {
  return (String(text || '').match(/[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?/g) || []).length;
}

function toast(message) {
  els.toast.textContent = message;
  els.toast.classList.add('show');
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => els.toast.classList.remove('show'), 2400);
}

function setBusy(value) {
  busy = value;
  els.rewriteBtn.disabled = value;
  els.rewriteBtn.querySelector('.btn-main').textContent = value ? 'Rewriting...' : 'Rewrite Text';
}

function options() {
  return { engine, mode: els.mode.value, strength: els.strength.value, biasClean: els.biasClean.checked };
}

function updateStats() {
  els.inputStats.textContent = `${words(els.input.value)} words`;
  els.outputStats.textContent = `${words(els.output.value)} words`;
  if (els.input.value.trim() && els.output.value.trim()) {
    const m = similarityScores(els.input.value, els.output.value);
    m.readability = readability(els.output.value);
    updateMetrics(m);
  }
}

function updateMetrics(m = {}) {
  const similarity = Number(m.estimatedSimilarity || 0);
  const lift = Number(m.originalityLift ?? Math.max(0, 100 - similarity));
  const phrase = Number(m.phraseOverlap || 0);
  const read = Number(m.readability || 0);
  els.similarity.textContent = `${similarity}%`;
  els.lift.textContent = `${lift}%`;
  els.phraseOverlap.textContent = `${phrase}%`;
  els.readability.textContent = `${read}`;
  els.similarityBar.style.width = `${Math.min(100, similarity)}%`;
  els.liftBar.style.width = `${Math.min(100, lift)}%`;
  els.phraseBar.style.width = `${Math.min(100, phrase)}%`;
  els.readabilityBar.style.width = `${Math.min(100, read)}%`;
}

function updateNotes(notes = []) {
  els.notes.innerHTML = '';
  notes.forEach(note => {
    const li = document.createElement('li');
    li.textContent = note;
    els.notes.appendChild(li);
  });
}

async function callRewriteAPI(text, opts) {
  const res = await fetch('/api/rewrite', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, ...opts })
  });
  if (!res.ok) throw new Error(`Server returned ${res.status}`);
  return res.json();
}

async function rewrite() {
  if (busy) return;
  const text = els.input.value.trim();
  if (!text) return toast('Paste or upload text first.');
  setBusy(true);
  const opts = options();
  try {
    let result;
    try {
      result = await callRewriteAPI(text, opts);
    } catch (apiError) {
      result = rewriteText(text, opts);
      result.engineUsed = 'browser-fallback';
      result.notes.unshift('Serverless function was unavailable, so browser fallback was used. Deploy on Netlify or run netlify dev for full server mode.');
    }
    els.output.value = result.rewritten || '';
    els.engineUsed.textContent = result.engineUsed === 'ai' ? 'AI Rewrite Assist' : result.engineUsed === 'algorithm-fallback' ? 'Algorithm fallback' : result.engineUsed === 'browser-fallback' ? 'Browser fallback' : 'Algorithm Rewriter';
    updateMetrics(result.metrics || {});
    updateNotes(result.notes || []);
    updateStats();
    saveHistory(text, result.rewritten, result.metrics, opts, result.engineUsed);
    toast('Rewrite completed. Review and edit the output before using it.');
  } catch (err) {
    console.error(err);
    toast('Rewrite failed. Browser fallback will be used.');
    const result = rewriteText(text, opts);
    els.output.value = result.rewritten;
    els.engineUsed.textContent = 'Browser fallback';
    updateMetrics(result.metrics);
    updateNotes(result.notes);
  } finally {
    setBusy(false);
  }
}

function polishOutput() {
  if (!els.output.value.trim()) return toast('Nothing to polish yet.');
  const polished = cleanSpacing(els.output.value)
    .replace(/\bi\b/g, 'I')
    .replace(/\s+([.,!?;:])/g, '$1')
    .replace(/([.!?])\s*([a-z])/g, (m, p, c) => `${p} ${c.toUpperCase()}`)
    .replace(/\b([A-Za-z]+)\s+\1\b/gi, '$1');
  els.output.value = polished;
  updateStats();
  toast('Output polished.');
}

function saveAs(filename, content, type = 'text/plain') {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  URL.revokeObjectURL(url);
}

function loadHistory() {
  try { return JSON.parse(localStorage.getItem('originalityStudioHistory') || '[]'); }
  catch { return []; }
}
function writeHistory(items) { localStorage.setItem('originalityStudioHistory', JSON.stringify(items.slice(0, 8))); }
function saveHistory(input, output, metrics, opts, engineUsed) {
  const items = loadHistory();
  items.unshift({ input: input.slice(0, 280), output: output.slice(0, 420), metrics, opts, engineUsed, time: new Date().toLocaleString() });
  writeHistory(items);
  renderHistory();
}
function renderHistory() {
  const items = loadHistory();
  els.historyList.innerHTML = '';
  if (!items.length) {
    els.historyList.innerHTML = '<p class="muted">No local history yet.</p>';
    return;
  }
  items.forEach((item, index) => {
    const card = document.createElement('div');
    card.className = 'history-item';
    card.innerHTML = `<p><strong>${item.opts?.mode || 'mode'}</strong> • ${item.opts?.strength || 'strength'} • ${item.engineUsed || 'engine'} • ${item.time}</p><p>${escapeHtml(item.output.slice(0, 180))}${item.output.length > 180 ? '...' : ''}</p>`;
    const btn = document.createElement('button');
    btn.className = 'ghost';
    btn.type = 'button';
    btn.textContent = 'Load output';
    btn.addEventListener('click', () => {
      els.output.value = item.output;
      updateStats();
      toast('Loaded from history.');
    });
    card.appendChild(btn);
    els.historyList.appendChild(card);
  });
}
function escapeHtml(text) {
  return String(text || '').replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
}

for (const btn of document.querySelectorAll('.engine-btn')) {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.engine-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    engine = btn.dataset.engine;
    els.engineUsed.textContent = engine === 'ai' ? 'AI mode selected' : 'Algorithm selected';
    if (engine === 'ai') toast('AI mode needs GEMINI_API_KEY on Netlify. Without it, fallback algorithm will run.');
  });
}

els.rewriteBtn.addEventListener('click', rewrite);
els.polishBtn.addEventListener('click', polishOutput);
els.swapBtn.addEventListener('click', () => {
  if (!els.output.value.trim()) return toast('No output to move.');
  els.input.value = els.output.value;
  els.output.value = '';
  updateStats();
  toast('Output moved to input.');
});
els.clearBtn.addEventListener('click', () => { els.input.value = ''; els.output.value = ''; updateStats(); updateMetrics(); updateNotes(['Paste text and choose an engine.']); });
els.sampleBtn.addEventListener('click', () => { els.input.value = sample; els.mode.value = 'ecommerce'; els.strength.value = 'maximum'; updateStats(); toast('Sample loaded.'); });
els.input.addEventListener('input', updateStats);
els.output.addEventListener('input', updateStats);
els.fileInput.addEventListener('change', async (e) => {
  const file = e.target.files?.[0];
  if (!file) return;
  const text = await file.text();
  els.input.value = text;
  updateStats();
  toast(`${file.name} loaded.`);
});
els.copyBtn.addEventListener('click', async () => {
  if (!els.output.value.trim()) return toast('Nothing to copy.');
  await navigator.clipboard.writeText(els.output.value);
  toast('Copied to clipboard.');
});
els.downloadTxtBtn.addEventListener('click', () => {
  if (!els.output.value.trim()) return toast('Nothing to download.');
  saveAs('rewritten-text.txt', els.output.value, 'text/plain;charset=utf-8');
});
els.downloadHtmlBtn.addEventListener('click', () => {
  if (!els.output.value.trim()) return toast('Nothing to download.');
  const html = `<!doctype html><html><head><meta charset="utf-8"><title>Rewritten Text</title><style>body{font-family:Arial,sans-serif;line-height:1.7;max-width:800px;margin:40px auto;padding:0 20px;color:#111}</style></head><body><h1>Rewritten Text</h1><p>${escapeHtml(els.output.value).replace(/\n\n/g, '</p><p>').replace(/\n/g, '<br>')}</p></body></html>`;
  saveAs('rewritten-text.html', html, 'text/html;charset=utf-8');
});
els.clearHistoryBtn.addEventListener('click', () => { writeHistory([]); renderHistory(); toast('History cleared.'); });

renderHistory();
updateStats();
updateMetrics();
