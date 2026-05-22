import { useMemo, useRef, useState } from 'react';
import { rewriteText } from '../shared/rewriterCore.mjs';

const sample = `Artificial intelligence is very important in the modern world because it helps people complete difficult tasks quickly. Many companies use AI tools to improve productivity, reduce manual work, and make better decisions. However, users should understand that AI writing must be reviewed carefully to maintain quality and originality.`;

function Badge({ children, tone = 'neutral' }) {
  return <span className={`badge badge-${tone}`}>{children}</span>;
}

function MetricCard({ label, value, sub, tone }) {
  return (
    <div className={`metric metric-${tone || 'default'}`}>
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{sub}</small>
    </div>
  );
}

function IconSpark() {
  return (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path d="M12 2L13.9 8.1L20 10L13.9 11.9L12 18L10.1 11.9L4 10L10.1 8.1L12 2Z" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M19 15L19.9 17.1L22 18L19.9 18.9L19 21L18.1 18.9L16 18L18.1 17.1L19 15Z" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export default function App() {
  const [input, setInput] = useState('');
  const [output, setOutput] = useState('');
  const [stats, setStats] = useState(null);
  const [tips, setTips] = useState([]);
  const [notice, setNotice] = useState('');
  const [mode, setMode] = useState('professional');
  const [intensity, setIntensity] = useState('strong');
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [status, setStatus] = useState('Ready');
  const fileRef = useRef(null);

  const inputWords = useMemo(() => input.trim() ? input.trim().split(/\s+/).length : 0, [input]);
  const outputWords = useMemo(() => output.trim() ? output.trim().split(/\s+/).length : 0, [output]);

  async function generateRewrite() {
    setLoading(true);
    setCopied(false);
    setStatus('Rewriting...');
    try {
      let payload;
      try {
        const response = await fetch('/api/rewrite', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: input, mode, intensity })
        });
        if (!response.ok) throw new Error('Function unavailable');
        payload = await response.json();
        setStatus('Serverless rewrite completed');
      } catch (_) {
        payload = rewriteText(input, { mode, intensity });
        setStatus('Local browser rewrite completed');
      }
      setOutput(payload.rewritten || '');
      setStats(payload.stats || null);
      setTips(payload.tips || []);
      setNotice(payload.notice || '');
    } finally {
      setLoading(false);
    }
  }

  async function copyOutput() {
    if (!output) return;
    await navigator.clipboard.writeText(output);
    setCopied(true);
    setTimeout(() => setCopied(false), 1200);
  }

  function downloadText() {
    if (!output) return;
    const blob = new Blob([output], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = 'originality-assistant-rewrite.txt';
    anchor.click();
    URL.revokeObjectURL(url);
  }

  async function handleFile(event) {
    const file = event.target.files?.[0];
    if (!file) return;
    const text = await file.text();
    setInput(text.slice(0, 15000));
  }

  function clearAll() {
    setInput('');
    setOutput('');
    setStats(null);
    setTips([]);
    setNotice('');
    setStatus('Ready');
  }

  const riskTone = stats?.estimatedSimilarity > 55 ? 'danger' : stats?.estimatedSimilarity > 32 ? 'warning' : 'success';

  return (
    <main className="app-shell">
      <div className="aurora aurora-one" />
      <div className="aurora aurora-two" />
      <section className="hero">
        <nav className="topbar">
          <div className="brand">
            <div className="brand-icon"><IconSpark /></div>
            <div>
              <strong>Originality Assistant Pro</strong>
              <span>Netlify Edition</span>
            </div>
          </div>
          <div className="nav-badges">
            <Badge tone="success">No API Key</Badge>
            <Badge tone="blue">Netlify Ready</Badge>
            <Badge tone="gold">Local Algorithm</Badge>
          </div>
        </nav>

        <div className="hero-grid">
          <div className="hero-copy">
            <p className="eyebrow">Ethical rewriter + similarity estimator</p>
            <h1>Rewrite text with a premium interface and stronger originality workflow.</h1>
            <p className="hero-text">
              Paste content, choose a rewrite style, and generate a cleaner version with lower direct wording overlap. Built for Netlify with a serverless function and browser fallback.
            </p>
            <div className="hero-actions">
              <button className="btn primary" onClick={() => setInput(sample)}>Use sample text</button>
              <button className="btn ghost" onClick={() => fileRef.current?.click()}>Upload .txt</button>
              <input ref={fileRef} type="file" accept=".txt,text/plain" hidden onChange={handleFile} />
            </div>
          </div>
          <div className="hero-card">
            <span className="live-dot" />
            <p>Rewrite engine status</p>
            <strong>{status}</strong>
            <div className="mini-grid">
              <span>Modes <b>4</b></span>
              <span>Strengths <b>4</b></span>
              <span>Internet check <b>No</b></span>
              <span>API cost <b>$0</b></span>
            </div>
          </div>
        </div>
      </section>

      <section className="workspace">
        <aside className="control-panel glass">
          <div className="panel-header">
            <span className="section-kicker">Rewrite Settings</span>
            <h2>Control the output style</h2>
          </div>

          <label className="field-label">Writing mode</label>
          <div className="segmented four">
            {['academic', 'professional', 'simple', 'creative'].map(item => (
              <button key={item} className={mode === item ? 'active' : ''} onClick={() => setMode(item)}>{item}</button>
            ))}
          </div>

          <label className="field-label">Rewrite strength</label>
          <div className="segmented two-lines">
            {['light', 'balanced', 'strong', 'maximum'].map(item => (
              <button key={item} className={intensity === item ? 'active' : ''} onClick={() => setIntensity(item)}>{item}</button>
            ))}
          </div>

          <div className="settings-note">
            <b>Best result:</b> use <span>Strong</span> or <span>Maximum</span>, then manually review facts, references, and meaning.
          </div>

          <div className="side-actions">
            <button className="btn primary wide" onClick={generateRewrite} disabled={loading || inputWords < 3}>
              {loading ? 'Rewriting...' : 'Rewrite Text'}
            </button>
            <button className="btn ghost wide" onClick={clearAll}>Clear</button>
          </div>
        </aside>

        <section className="editor-grid">
          <div className="editor-card glass">
            <div className="editor-head">
              <div>
                <span className="section-kicker">Input</span>
                <h2>Original Text</h2>
              </div>
              <Badge>{inputWords} words</Badge>
            </div>
            <textarea
              value={input}
              onChange={e => setInput(e.target.value.slice(0, 15000))}
              placeholder="Paste your paragraph, essay section, blog content, assignment draft, or product description here..."
            />
          </div>

          <div className="editor-card glass result-card">
            <div className="editor-head">
              <div>
                <span className="section-kicker">Output</span>
                <h2>Rewritten Text</h2>
              </div>
              <Badge tone={output ? 'success' : 'neutral'}>{outputWords} words</Badge>
            </div>
            <textarea value={output} readOnly placeholder="Your rewritten content will appear here..." />
            <div className="result-actions">
              <button className="btn soft" onClick={copyOutput} disabled={!output}>{copied ? 'Copied!' : 'Copy'}</button>
              <button className="btn soft" onClick={downloadText} disabled={!output}>Download TXT</button>
            </div>
          </div>
        </section>
      </section>

      <section className="insights glass">
        <div className="insight-title">
          <span className="section-kicker">Analysis</span>
          <h2>Similarity and quality report</h2>
          <p>This is an internal overlap estimate between the input and rewritten text, not a live plagiarism database scan.</p>
        </div>

        <div className="metrics-grid">
          <MetricCard label="Estimated similarity" value={stats ? `${stats.estimatedSimilarity}%` : '--'} sub="Lower is better" tone={riskTone} />
          <MetricCard label="Originality lift" value={stats ? `${stats.originalityLift}%` : '--'} sub="Estimated change" tone="success" />
          <MetricCard label="Phrase overlap" value={stats ? `${stats.phraseOverlap}%` : '--'} sub="2-3 word patterns" tone="warning" />
          <MetricCard label="Readability" value={stats ? `${stats.readability}/100` : '--'} sub="Clarity estimate" tone="blue" />
        </div>

        <div className="tips-grid">
          <div className="tip-box">
            <h3>Smart suggestions</h3>
            <ul>
              {(tips.length ? tips : ['Run the rewrite to receive suggestions.']).map((tip, index) => <li key={index}>{tip}</li>)}
            </ul>
          </div>
          <div className="tip-box muted">
            <h3>Honest limitation</h3>
            <p>{notice || 'This tool rewrites wording and estimates overlap. It does not compare your text with online sources, journals, or Turnitin-style databases.'}</p>
          </div>
        </div>
      </section>

      <footer className="footer">
        <p>Built for ethical rewriting, clarity improvement, and originality support. Always cite borrowed ideas.</p>
      </footer>
    </main>
  );
}
