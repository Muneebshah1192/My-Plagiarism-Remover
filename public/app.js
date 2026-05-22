import { rewriteText } from './core/rewriterCore.mjs';

const inputText = document.querySelector('#inputText');
const outputText = document.querySelector('#outputText');
const modeSelect = document.querySelector('#modeSelect');
const intensitySelect = document.querySelector('#intensitySelect');
const rewriteBtn = document.querySelector('#rewriteBtn');
const sampleBtn = document.querySelector('#sampleBtn');
const clearBtn = document.querySelector('#clearBtn');
const copyBtn = document.querySelector('#copyBtn');
const downloadBtn = document.querySelector('#downloadBtn');
const fileInput = document.querySelector('#fileInput');
const notice = document.querySelector('#notice');
const tipsList = document.querySelector('#tipsList');

const metrics = {
  similarityMetric: document.querySelector('#similarityMetric'),
  liftMetric: document.querySelector('#liftMetric'),
  phraseMetric: document.querySelector('#phraseMetric'),
  readabilityMetric: document.querySelector('#readabilityMetric'),
  similarityBar: document.querySelector('#similarityBar'),
  liftBar: document.querySelector('#liftBar'),
  phraseBar: document.querySelector('#phraseBar'),
  readabilityBar: document.querySelector('#readabilityBar')
};

const sample = `Artificial intelligence has become very important in the modern world because it helps people complete difficult tasks quickly. Many students and companies use modern technology to improve productivity and make better decisions. However, AI writing must be reviewed carefully because good quality content needs originality, proper structure, and accurate information.`;

function setLoading(isLoading) {
  rewriteBtn.disabled = isLoading;
  rewriteBtn.textContent = isLoading ? 'Rewriting...' : 'Rewrite Text';
}

function updateMetrics(stats = {}) {
  const similarity = stats.estimatedSimilarity || 0;
  const lift = stats.originalityLift || 0;
  const phrase = stats.phraseOverlap || 0;
  const readability = stats.readability || 0;

  metrics.similarityMetric.textContent = `${similarity}%`;
  metrics.liftMetric.textContent = `${lift}%`;
  metrics.phraseMetric.textContent = `${phrase}%`;
  metrics.readabilityMetric.textContent = readability;

  metrics.similarityBar.style.width = `${Math.min(similarity, 100)}%`;
  metrics.liftBar.style.width = `${Math.min(lift, 100)}%`;
  metrics.phraseBar.style.width = `${Math.min(phrase, 100)}%`;
  metrics.readabilityBar.style.width = `${Math.min(readability, 100)}%`;
}

function updateTips(tips = []) {
  tipsList.innerHTML = '';
  tips.forEach((tip) => {
    const li = document.createElement('li');
    li.textContent = tip;
    tipsList.appendChild(li);
  });
}

async function callRewriteApi(text, mode, intensity) {
  try {
    const response = await fetch('/api/rewrite', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, mode, intensity })
    });
    if (!response.ok) throw new Error('API route failed');
    return await response.json();
  } catch (error) {
    return rewriteText(text, { mode, intensity });
  }
}

rewriteBtn.addEventListener('click', async () => {
  const text = inputText.value.trim();
  if (!text) {
    inputText.focus();
    outputText.textContent = 'Please paste text first.';
    outputText.classList.remove('empty');
    updateTips(['Paste at least one paragraph for a stronger rewrite.']);
    return;
  }

  setLoading(true);
  const result = await callRewriteApi(text, modeSelect.value, intensitySelect.value);
  outputText.textContent = result.rewritten || 'No output generated.';
  outputText.classList.remove('empty');
  notice.textContent = result.notice || 'Review output carefully before publishing.';
  updateMetrics(result.stats || {});
  updateTips(result.tips || []);
  setLoading(false);
});

sampleBtn.addEventListener('click', () => {
  inputText.value = sample;
  outputText.textContent = 'Sample added. Click Rewrite Text.';
  outputText.classList.remove('empty');
});

clearBtn.addEventListener('click', () => {
  inputText.value = '';
  outputText.textContent = 'Your rewritten result will appear here.';
  outputText.classList.add('empty');
  notice.textContent = 'This tool estimates text overlap only. It does not check the internet or guarantee plagiarism removal.';
  updateMetrics({});
  updateTips(['Paste text and click rewrite to get suggestions.']);
});

copyBtn.addEventListener('click', async () => {
  const text = outputText.textContent.trim();
  if (!text || outputText.classList.contains('empty')) return;
  await navigator.clipboard.writeText(text);
  copyBtn.textContent = 'Copied';
  setTimeout(() => (copyBtn.textContent = 'Copy'), 1200);
});

downloadBtn.addEventListener('click', () => {
  const text = outputText.textContent.trim();
  if (!text || outputText.classList.contains('empty')) return;
  const blob = new Blob([text], { type: 'text/plain;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'rewritten-text.txt';
  a.click();
  URL.revokeObjectURL(url);
});

fileInput.addEventListener('change', async (event) => {
  const file = event.target.files?.[0];
  if (!file) return;
  const text = await file.text();
  inputText.value = text;
});

updateMetrics({});
