(function(){
  const $ = (id) => document.getElementById(id);
  const shell = document.querySelector('.app-shell');

  function setTheme(theme){
    document.documentElement.setAttribute('data-theme', theme);
    try{ localStorage.setItem('textforge-theme', theme); }catch(e){}
    const btn = $('themeToggle');
    if(btn) btn.textContent = theme === 'dark' ? '☀️ Light' : '🌙 Dark';
  }
  setTheme(document.documentElement.getAttribute('data-theme') || 'light');
  if(!shell) return;

  let currentTool = 'humanizer';
  const input = $('inputText');
  const output = $('outputText');
  const status = $('statusText');
  const toneSelect = $('toneSelect');
  const strengthSelect = $('strengthSelect');
  const caseSelect = $('caseSelect');

  toneSelect.value = shell.dataset.defaultTone || 'professional';
  strengthSelect.value = shell.dataset.defaultStrength || 'strong';
  $('settingsTone').value = shell.dataset.defaultTone || 'professional';
  $('settingsStrength').value = shell.dataset.defaultStrength || 'strong';

  try{
    if(localStorage.getItem('textforge-sidebar') === 'collapsed') shell.classList.add('sidebar-collapsed');
  }catch(e){}

  function setStatus(msg){ status.textContent = msg || ''; }
  function setTool(btn){
    document.querySelectorAll('.tool-pill').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    currentTool = btn.dataset.tool;
    $('selectedToolName').textContent = btn.dataset.name;
    $('selectedToolDesc').textContent = btn.dataset.description;
    setStatus('Selected: ' + btn.dataset.name);
  }

  document.querySelectorAll('.tool-pill').forEach(btn=>btn.addEventListener('click',()=>setTool(btn)));
  document.querySelectorAll('.cat-btn').forEach(btn=>{
    btn.addEventListener('click',()=>{
      document.querySelectorAll('.cat-btn').forEach(b=>b.classList.remove('active'));
      btn.classList.add('active');
      const cat = btn.dataset.category;
      document.querySelectorAll('.tool-group').forEach(g=>g.classList.toggle('active', g.dataset.category === cat));
      const first = document.querySelector(`.tool-group[data-category="${CSS.escape(cat)}"] .tool-pill`);
      if(first) setTool(first);
      if(window.innerWidth < 820) document.querySelector('.sidebar').classList.remove('open');
    });
  });

  $('toolSearch').addEventListener('input', e=>{
    const q=e.target.value.toLowerCase().trim();
    document.querySelectorAll('.tool-pill').forEach(b=>{
      const show = !q || b.textContent.toLowerCase().includes(q) || b.dataset.description.toLowerCase().includes(q);
      b.style.display = show ? '' : 'none';
    });
    if(q){
      document.querySelectorAll('.tool-group').forEach(g=>g.classList.add('active'));
    }else{
      const activeCat = document.querySelector('.cat-btn.active')?.dataset.category;
      document.querySelectorAll('.tool-group').forEach(g=>g.classList.toggle('active', g.dataset.category === activeCat));
    }
  });

  async function runTool(){
    const text = input.value.trim();
    if(!text){ setStatus('Add some text first.'); input.focus(); return; }
    setStatus('Processing...');
    $('runTool').disabled = true;
    $('runTool').textContent = 'Working...';
    const started = performance.now();
    try{
      const res = await fetch('/api/process', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({tool_id:currentTool, text, params:{tone:toneSelect.value, strength:strengthSelect.value, case:caseSelect.value}, save:true})
      });
      const data = await res.json();
      if(!data.ok) throw new Error(data.error || 'Processing failed');
      output.value = data.output;
      updateMetrics(data.stats);
      const ms = Math.max(100, Math.round(performance.now() - started));
      setStatus('Done in ' + ms + 'ms. Output is ready.');
    }catch(err){ setStatus(err.message); }
    finally{ $('runTool').disabled = false; $('runTool').textContent = 'Run Tool'; }
  }
  $('runTool').addEventListener('click', runTool);
  input.addEventListener('keydown', e=>{ if((e.ctrlKey || e.metaKey) && e.key === 'Enter') runTool(); });

  function localWords(t){ return (t.toLowerCase().match(/[a-z][a-z'-]*/g)||[]).filter(w=>w.length>2); }
  function localMetrics(a,b){
    const ws = localWords(b); const sents = (b.match(/[.!?]+\s|\n+/g)||[]).length + (b.trim()?1:0);
    const sa = new Set(localWords(a)); const sb = new Set(localWords(b));
    const inter = [...sa].filter(x=>sb.has(x)).length; const uni = new Set([...sa,...sb]).size || 1;
    const sim = Math.round(inter*1000/uni)/10;
    return {similarity:sim, originality_lift:Math.max(0, Math.round((100-sim)*10)/10), phrase_overlap:sim, readability:70, words:ws.length, sentences:sents, reading_time:Math.max(1, Math.ceil(ws.length/220)), characters:b.length};
  }
  function updateMetrics(m){
    m = m || localMetrics(input.value, output.value);
    $('mSimilarity').textContent = (m.similarity||0)+'%'; $('barSimilarity').style.width = Math.min(100,m.similarity||0)+'%';
    $('mLift').textContent = (m.originality_lift||0)+'%'; $('barLift').style.width = Math.min(100,m.originality_lift||0)+'%';
    $('mPhrase').textContent = (m.phrase_overlap||0)+'%'; $('barPhrase').style.width = Math.min(100,m.phrase_overlap||0)+'%';
    $('mReadability').textContent = m.readability||0; $('barReadability').style.width = Math.min(100,m.readability||0)+'%';
    $('mWords').textContent = m.words||0; $('mSentences').textContent = m.sentences||0; $('mReading').textContent = m.reading_time||0; $('mChars').textContent = m.characters||0;
  }
  $('compareBtn').addEventListener('click', ()=>{ updateMetrics(localMetrics(input.value, output.value)); setStatus('Analytics refreshed.'); });

  $('copyOutput').addEventListener('click', async()=>{ await navigator.clipboard.writeText(output.value); setStatus('Copied to clipboard.'); });
  $('useAsInput').addEventListener('click',()=>{ input.value = output.value; output.value=''; updateMetrics(localMetrics('', '')); setStatus('Output moved to input.'); });
  $('clearInput').addEventListener('click',()=>{ input.value=''; output.value=''; updateMetrics(localMetrics('', '')); setStatus('Cleared.'); });
  $('sampleBtn').addEventListener('click',()=>{
    input.value = 'TextForge Studio is a comprehensive writing platform that helps users improve their content, rewrite paragraphs, generate marketing copy, create study notes, and export polished documents. It is designed for students, freelancers, marketers, and business owners who need fast and professional text tools.';
    setStatus('Sample added. Press Ctrl + Enter to run.');
  });
  $('fileUpload').addEventListener('change', async(e)=>{
    const f=e.target.files[0]; if(!f) return;
    const fd = new FormData(); fd.append('file', f); setStatus('Reading file...');
    try{
      const res = await fetch('/api/upload', {method:'POST', body:fd}); const data=await res.json();
      if(!data.ok) throw new Error(data.error || 'Upload failed');
      input.value = data.text; setStatus('File imported: '+data.filename);
    }catch(err){ setStatus(err.message); }
  });
  $('exportBtn').addEventListener('click', async()=>{
    const text = output.value || input.value; if(!text.trim()){ setStatus('Nothing to export.'); return; }
    const fmt = $('exportFormat').value; setStatus('Preparing export...');
    try{
      const res = await fetch('/api/export', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({text, format:fmt, title:$('selectedToolName').textContent})});
      if(!res.ok) throw new Error('Export failed');
      const blob = await res.blob(); const url = URL.createObjectURL(blob); const a=document.createElement('a');
      a.href=url; a.download='textforge-output.'+fmt; document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url);
      setStatus('Export downloaded.');
    }catch(err){ setStatus(err.message); }
  });

  $('settingsToggle').addEventListener('click',()=> $('settingsPop').classList.toggle('open'));
  document.addEventListener('click',e=>{ if(!e.target.closest('.menu-wrap')) $('settingsPop').classList.remove('open'); });
  $('themeToggle').addEventListener('click',()=>{
    const next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    setTheme(next); setStatus((next === 'dark' ? 'Dark' : 'Light') + ' mode enabled.');
  });
  $('collapseSidebar').addEventListener('click',()=>{
    shell.classList.toggle('sidebar-collapsed');
    try{ localStorage.setItem('textforge-sidebar', shell.classList.contains('sidebar-collapsed') ? 'collapsed' : 'open'); }catch(e){}
  });
  $('saveSettings').addEventListener('click', async()=>{
    const data={default_tone:$('settingsTone').value, default_strength:$('settingsStrength').value, brand_name:$('settingsBrand').value};
    const res=await fetch('/api/settings',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
    setStatus(res.ok?'Settings saved.':'Could not save settings.');
  });
  $('clearHistory').addEventListener('click', async()=>{
    if(!confirm('Clear your saved history?')) return;
    const res=await fetch('/api/clear-history',{method:'POST'});
    if(res.ok){ document.querySelector('.history-list').innerHTML='<p class="empty-history">No saved history yet.</p>'; setStatus('History cleared.'); }
  });
  $('historyToggle').addEventListener('click',()=> $('historyPanel').classList.add('open'));
  $('closeHistory').addEventListener('click',()=> $('historyPanel').classList.remove('open'));
  document.querySelectorAll('.history-item').forEach(item=>item.addEventListener('click',async()=>{
    const res=await fetch('/api/history/'+item.dataset.id); const data=await res.json();
    if(data.ok){ input.value=data.item.input_text; output.value=data.item.output_text; updateMetrics(JSON.parse(data.item.stats_json)); $('historyPanel').classList.remove('open'); setStatus('History item loaded.'); }
  }));
  $('openSidebar')?.addEventListener('click',()=>document.querySelector('.sidebar').classList.add('open'));
  $('closeSidebar')?.addEventListener('click',()=>document.querySelector('.sidebar').classList.remove('open'));
  updateMetrics(localMetrics('', ''));
})();
