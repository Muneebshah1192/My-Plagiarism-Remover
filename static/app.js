(function(){
  const $ = id => document.getElementById(id);
  const shell = document.querySelector('.app-shell');
  const publicToggle = $('publicNavToggle');
  const publicLinks = $('publicLinks');
  if(publicToggle && publicLinks){ publicToggle.addEventListener('click',()=> publicLinks.classList.toggle('open')); }

  function setTheme(theme){
    document.documentElement.setAttribute('data-theme', theme);
    try{ localStorage.setItem('textforge-theme-v4', theme); }catch(e){}
    const btn = $('themeToggle');
    if(btn) btn.textContent = theme === 'dark' ? '☀️ Light' : '🌙 Dark';
  }
  setTheme(document.documentElement.getAttribute('data-theme') || 'light');
  if(!shell) return;

  let currentTool = shell.dataset.currentTool || document.querySelector('.tool-card.active')?.dataset.tool || 'humanizer';
  let engineMode = shell.dataset.engineMode || 'algorithm';
  const isPremium = shell.dataset.isPremium === '1';
  const input = $('inputText');
  const output = $('outputText');
  const status = $('statusText');
  const toneSelect = $('toneSelect');
  const strengthSelect = $('strengthSelect');
  const caseSelect = $('caseSelect');

  function safeSet(id, value){ const el=$(id); if(el) el.value=value; }
  safeSet('settingsTone', shell.dataset.defaultTone || 'professional');
  safeSet('settingsStrength', shell.dataset.defaultStrength || 'strong');
  if(toneSelect) toneSelect.value = shell.dataset.defaultTone || 'professional';
  if(strengthSelect) strengthSelect.value = shell.dataset.defaultStrength || 'strong';
  try{ if(localStorage.getItem('textforge-sidebar') === 'collapsed') shell.classList.add('sidebar-collapsed'); }catch(e){}

  function setStatus(msg){ if(status) status.textContent = msg || ''; }
  function syncEngineButtons(){
    const engLabel = $('engineLabel');
    if(engLabel) engLabel.textContent = engineMode === 'api' ? 'Gemini API' : 'Algorithm';
    const toggle = $('engineToggle'); if(toggle) toggle.checked = engineMode === 'api';
    document.querySelectorAll('.mode-pill').forEach(b=>b.classList.toggle('active', b.dataset.mode === engineMode));
    const hint=$('modeHint'); if(hint) hint.textContent = engineMode === 'api' ? 'Gemini API mode is active. Add your key in settings.' : 'Built-in algorithm mode is active. No external API is used.';
  }
  syncEngineButtons();

  function setTool(btn){
    if(btn.dataset.premium === '1' && !isPremium){
      setStatus('This is a premium tool. Upgrade to unlock it.');
      window.location.href = '/subscribe';
      return;
    }
    document.querySelectorAll('.tool-card').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    currentTool = btn.dataset.tool;
    $('selectedToolName').textContent = btn.dataset.name;
    $('selectedToolDesc').textContent = btn.dataset.description;
    setStatus('Selected: ' + btn.dataset.name);
    document.querySelector('.main-panel')?.scrollIntoView({behavior:'smooth', block:'start'});
  }
  document.querySelectorAll('.tool-card').forEach(btn=>btn.addEventListener('click',()=>setTool(btn)));

  const search = $('toolSearch');
  if(search){ search.addEventListener('input', e=>{
    const q=e.target.value.toLowerCase().trim();
    document.querySelectorAll('.tool-card').forEach(b=>{
      const show = !q || b.dataset.name.toLowerCase().includes(q) || b.dataset.description.toLowerCase().includes(q);
      b.style.display = show ? '' : 'none';
    });
  });}

  function setEngineMode(mode){
    if(mode === 'api' && !isPremium){
      setStatus('Gemini API mode is available during trial or on premium plan.');
      window.location.href='/subscribe';
      return;
    }
    engineMode = mode;
    syncEngineButtons();
    setStatus((mode === 'api' ? 'Gemini API' : 'Algorithm') + ' mode selected.');
  }
  $('algoModeBtn')?.addEventListener('click', ()=>setEngineMode('algorithm'));
  $('apiModeBtn')?.addEventListener('click', ()=>setEngineMode('api'));
  $('engineToggle')?.addEventListener('change', e=>setEngineMode(e.target.checked ? 'api' : 'algorithm'));

  async function runTool(){
    const text = input.value.trim();
    if(!text){ setStatus('Add some text first.'); input.focus(); return; }
    setStatus('Processing with ' + (engineMode === 'api' ? 'Gemini API hybrid mode' : 'built-in algorithm') + '...');
    const run=$('runTool'); run.disabled = true; run.textContent = 'Working...';
    const started = performance.now();
    try{
      const params = {tone:toneSelect.value, strength:strengthSelect.value, case:caseSelect.value, engine_mode:engineMode, gemini_model:($('geminiModel')?.value||'gemini-1.5-flash')};
      const key = $('geminiKey')?.value?.trim();
      if(key) params.gemini_api_key = key;
      const res = await fetch('/api/process', {
        method:'POST', headers:{'Content-Type':'application/json'},
        body: JSON.stringify({tool_id:currentTool, text, params, save:true})
      });
      const data = await res.json();
      if(!data.ok){
        if(data.upgrade_required){ window.location.href='/subscribe'; return; }
        throw new Error(data.error || 'Processing failed');
      }
      output.value = data.output;
      updateMetrics(data.stats);
      if(data.usage){ const u=$('usageLive'); if(u) u.textContent=data.usage.used; }
      const ms = Math.max(50, Math.round(performance.now() - started));
      setStatus('Done in ' + ms + 'ms using ' + (data.engine_used || engineMode) + '. Output is ready.');
    }catch(err){ setStatus(err.message); }
    finally{ run.disabled = false; run.textContent = 'Run Tool'; }
  }
  $('runTool')?.addEventListener('click', runTool);
  input?.addEventListener('keydown', e=>{ if((e.ctrlKey || e.metaKey) && e.key === 'Enter') runTool(); });

  function localWords(t){ return (t.toLowerCase().match(/[a-z][a-z'-]*/g)||[]).filter(w=>w.length>2); }
  function localMetrics(a,b){
    const ws = localWords(b); const sents = (b.match(/[.!?]+\s|\n+/g)||[]).length + (b.trim()?1:0);
    const sa = new Set(localWords(a)); const sb = new Set(localWords(b));
    const inter = [...sa].filter(x=>sb.has(x)).length; const uni = new Set([...sa,...sb]).size || 1;
    const sim = Math.round(inter*1000/uni)/10;
    return {similarity:sim, originality_lift:Math.max(0, Math.round((100-sim)*10)/10), phrase_overlap:sim, readability:70, words:ws.length, sentences:sents, reading_time:Math.max(1, Math.ceil(ws.length/220)), characters:b.length};
  }
  function updateMetrics(m){
    m = m || localMetrics(input?.value || '', output?.value || '');
    const setTxt=(id,val)=>{ const el=$(id); if(el) el.textContent=val; };
    const setBar=(id,val)=>{ const el=$(id); if(el) el.style.width=Math.min(100,val||0)+'%'; };
    setTxt('mSimilarity', (m.similarity||0)+'%'); setBar('barSimilarity', m.similarity||0);
    setTxt('mLift', (m.originality_lift||0)+'%'); setBar('barLift', m.originality_lift||0);
    setTxt('mPhrase', (m.phrase_overlap||0)+'%'); setBar('barPhrase', m.phrase_overlap||0);
    setTxt('mReadability', m.readability||0); setBar('barReadability', m.readability||0);
    setTxt('mWords', m.words||0); setTxt('mSentences', m.sentences||0); setTxt('mReading', m.reading_time||0); setTxt('mChars', m.characters||0);
  }
  $('compareBtn')?.addEventListener('click', ()=>{ updateMetrics(localMetrics(input.value, output.value)); setStatus('Analytics refreshed.'); });
  $('copyOutput')?.addEventListener('click', async()=>{ await navigator.clipboard.writeText(output.value); setStatus('Copied to clipboard.'); });
  $('useAsInput')?.addEventListener('click',()=>{ input.value = output.value; output.value=''; updateMetrics(localMetrics('', '')); setStatus('Output moved to input.'); });
  $('clearInput')?.addEventListener('click',()=>{ input.value=''; output.value=''; updateMetrics(localMetrics('', '')); setStatus('Cleared.'); });
  $('sampleBtn')?.addEventListener('click',()=>{
    input.value = 'TextForge Studio is a comprehensive writing platform that helps users improve their content, rewrite paragraphs, generate marketing copy, create study notes, and export polished documents. It is designed for students, freelancers, marketers, and business owners who need fast and professional text tools.';
    setStatus('Sample added. Press Ctrl + Enter to run.');
  });
  $('fileUpload')?.addEventListener('change', async(e)=>{
    const f=e.target.files[0]; if(!f) return;
    const fd = new FormData(); fd.append('file', f); setStatus('Reading file...');
    try{ const res = await fetch('/api/upload', {method:'POST', body:fd}); const data=await res.json(); if(!data.ok) throw new Error(data.error || 'Upload failed'); input.value = data.text; setStatus('File imported: '+data.filename); }
    catch(err){ setStatus(err.message); }
  });
  $('exportBtn')?.addEventListener('click', async()=>{
    const text = output.value || input.value; if(!text.trim()){ setStatus('Nothing to export.'); return; }
    const fmt = $('exportFormat').value; setStatus('Preparing export...');
    try{ const res = await fetch('/api/export', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({text, format:fmt, title:($('selectedToolName')?.textContent || 'TextForge Output')})}); if(!res.ok) throw new Error('Export failed'); const blob = await res.blob(); const url = URL.createObjectURL(blob); const a=document.createElement('a'); a.href=url; a.download='textforge-output.'+fmt; document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url); setStatus('Export downloaded.'); }
    catch(err){ setStatus(err.message); }
  });

  $('settingsToggle')?.addEventListener('click',(e)=>{ e.stopPropagation(); const pop=$('settingsPop'); if(pop) pop.classList.toggle('open'); });
  document.addEventListener('click',e=>{ if(!e.target.closest('.menu-wrap') && $('settingsPop')) $('settingsPop').classList.remove('open'); });
  $('themeToggle')?.addEventListener('click',()=>{ const next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark'; setTheme(next); setStatus((next === 'dark' ? 'Dark' : 'Light') + ' mode enabled.'); });
  $('collapseSidebar')?.addEventListener('click',()=>{ shell.classList.toggle('sidebar-collapsed'); try{ localStorage.setItem('textforge-sidebar', shell.classList.contains('sidebar-collapsed') ? 'collapsed' : 'open'); }catch(e){} });
  $('saveSettings')?.addEventListener('click', async()=>{
    const data={default_tone:$('settingsTone').value, default_strength:$('settingsStrength').value, brand_name:$('settingsBrand').value, engine_mode:engineMode, gemini_model:$('geminiModel')?.value||'gemini-1.5-flash'};
    const key=$('geminiKey')?.value?.trim(); if(key) data.gemini_api_key=key;
    const res=await fetch('/api/settings',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
    setStatus(res.ok?'Settings saved.':'Could not save settings.');
  });
  $('clearHistory')?.addEventListener('click', async()=>{ if(!confirm('Clear your saved history?')) return; const res=await fetch('/api/clear-history',{method:'POST'}); if(res.ok){ const hl=document.querySelector('.history-list'); if(hl) hl.innerHTML='<p class="empty-history">No saved history yet.</p>';  setStatus('History cleared.'); } });
  $('historyToggle')?.addEventListener('click',()=> $('historyPanel').classList.add('open'));
  $('closeHistory')?.addEventListener('click',()=> $('historyPanel').classList.remove('open'));
  document.querySelectorAll('.history-item').forEach(item=>item.addEventListener('click',async()=>{ const res=await fetch('/api/history/'+item.dataset.id); const data=await res.json(); if(data.ok){ input.value=data.item.input_text; output.value=data.item.output_text; updateMetrics(JSON.parse(data.item.stats_json)); $('historyPanel').classList.remove('open'); setStatus('History item loaded.'); } }));
  $('openSidebar')?.addEventListener('click',()=>document.querySelector('.sidebar').classList.add('open'));
  $('closeSidebar')?.addEventListener('click',()=>document.querySelector('.sidebar').classList.remove('open'));
  updateMetrics(localMetrics('', ''));
})();
