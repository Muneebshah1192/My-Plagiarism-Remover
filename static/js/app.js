const $ = (q) => document.querySelector(q);
const $$ = (q) => [...document.querySelectorAll(q)];

function toast(message){
  const t=document.createElement('div'); t.className='toast'; t.textContent=message; document.body.appendChild(t);
  setTimeout(()=>t.remove(),3000);
}
function wordCount(text){ return (text.trim().match(/\b\S+\b/g)||[]).length; }
async function postJSON(url, data){
  const res = await fetch(url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
  const json = await res.json().catch(()=>({ok:false,error:'Invalid server response'}));
  if(!res.ok || !json.ok) throw new Error(json.error || 'Request failed');
  return json;
}

$$('form[data-auth]').forEach(form=>{
  form.addEventListener('submit', async e=>{
    e.preventDefault();
    const msg=form.querySelector('.form-msg'); msg.textContent='Please wait...';
    const data=Object.fromEntries(new FormData(form).entries());
    const type=form.dataset.auth;
    try{ await postJSON(`/api/${type}`, data); location.reload(); }
    catch(err){ msg.textContent=err.message; }
  });
});

const inputText=$('#inputText'), outputText=$('#outputText');
const toolHelp={
  algorithm_rewriter:'Rewrites text using the built-in Python algorithm. No API is required.',
  ai_rewriter:'Uses your saved API key for a deeper AI rewrite, with algorithm fallback if the AI output is too similar.',
  ai_style_cleaner:'Reduces robotic AI-style wording and makes the writing sound more natural.',
  grammar_polish:'Fixes basic grammar, punctuation, capitalization, and common mistakes.',
  bias_cleaner:'Replaces harmful, biased, or outdated wording with safer alternatives.',
  product_rewriter:'Turns product names and feature lists into polished e-commerce copy.',
  summarizer:'Creates a shorter summary of the most important points.',
  expander:'Expands short text into a clearer, more complete paragraph.',
  bullet_generator:'Converts text into clean bullet points.',
  title_generator:'Generates useful titles from your content.',
  keyword_extractor:'Extracts the most important keywords from your text.'
};
function updateCounts(){
  if($('#inputCount')) $('#inputCount').textContent=`${wordCount(inputText.value)} words`;
  if($('#outputCount')) $('#outputCount').textContent=`${wordCount(outputText.value)} words`;
}
inputText?.addEventListener('input', updateCounts);
outputText?.addEventListener('input', updateCounts);
$('#toolSelect')?.addEventListener('change', e=>{
  $('#toolHelp').textContent=toolHelp[e.target.value]||'';
  $('#engineLabel').textContent=e.target.value==='ai_rewriter'?'AI + fallback':'Algorithm';
});

$('#sampleBtn')?.addEventListener('click',()=>{
  inputText.value='LAURA GELLER Baked Icons Complete Full Face Palette, Medium | All-in-One Makeup Palette with Baked Foundations, Blush, Bronzer, Highlighter, Eyeshadows | Coverage for Mature Skin | Travel-Friendly';
  updateCounts();
});
$('#clearBtn')?.addEventListener('click',()=>{ inputText.value=''; outputText.value=''; updateCounts(); setMetrics({similarity:0,originality_lift:0,phrase_overlap:0,readability:0}); });
$('#swapBtn')?.addEventListener('click',()=>{ if(outputText.value.trim()){ inputText.value=outputText.value; outputText.value=''; updateCounts(); }});
$('#copyBtn')?.addEventListener('click',async()=>{ if(outputText.value.trim()){ await navigator.clipboard.writeText(outputText.value); toast('Copied output text.'); }});
$('#downloadBtn')?.addEventListener('click',()=>{
  const text=outputText.value.trim(); if(!text) return toast('No output to download.');
  const blob=new Blob([text],{type:'text/plain;charset=utf-8'});
  const a=document.createElement('a'); a.href=URL.createObjectURL(blob); a.download='originality-studio-output.txt'; a.click(); URL.revokeObjectURL(a.href);
});
$('#fileInput')?.addEventListener('change',async e=>{
  const file=e.target.files[0]; if(!file) return;
  if(file.size>1024*1024) return toast('File is too large. Keep it under 1MB.');
  inputText.value=await file.text(); updateCounts(); toast('File imported.');
});

function setMetrics(m){
  const sim=Number(m.similarity||0), lift=Number(m.originality_lift||0), overlap=Number(m.phrase_overlap||0), read=Number(m.readability||0);
  $('#mSimilarity') && ($('#mSimilarity').textContent=`${sim}%`);
  $('#mLift') && ($('#mLift').textContent=`${lift}%`);
  $('#mOverlap') && ($('#mOverlap').textContent=`${overlap}%`);
  $('#mReadability') && ($('#mReadability').textContent=`${read}`);
  $('#barSimilarity') && ($('#barSimilarity').style.width=`${Math.min(100,sim)}%`);
  $('#barLift') && ($('#barLift').style.width=`${Math.min(100,lift)}%`);
  $('#barOverlap') && ($('#barOverlap').style.width=`${Math.min(100,overlap)}%`);
  $('#barReadability') && ($('#barReadability').style.width=`${Math.min(100,read)}%`);
}

$('#runBtn')?.addEventListener('click',async()=>{
  const text=inputText.value.trim(); if(!text) return toast('Please enter text first.');
  const btn=$('#runBtn'), old=btn.textContent; btn.disabled=true; btn.textContent='Processing...';
  $('#noteText').textContent='Working on your text...';
  try{
    const data=await postJSON('/api/tool',{
      tool:$('#toolSelect').value,
      tone:$('#toneSelect').value,
      strength:$('#strengthSelect').value,
      text
    });
    outputText.value=data.output||''; setMetrics(data.metrics||{}); updateCounts(); $('#noteText').textContent=data.note||'Done.'; toast('Tool completed.');
  }catch(err){ $('#noteText').textContent=err.message; toast(err.message); }
  finally{ btn.disabled=false; btn.textContent=old; }
});

$('#logoutBtn')?.addEventListener('click',async()=>{ await postJSON('/api/logout',{}); location.reload(); });

function openModal(id){ const el=$('#'+id); if(el){el.classList.add('show'); el.setAttribute('aria-hidden','false');} }
function closeModal(id){ const el=$('#'+id); if(el){el.classList.remove('show'); el.setAttribute('aria-hidden','true');} }
$$('[data-close]').forEach(b=>b.addEventListener('click',()=>closeModal(b.dataset.close)));
$$('.modal').forEach(m=>m.addEventListener('click',e=>{ if(e.target===m) closeModal(m.id); }));

$('#settingsBtn')?.addEventListener('click',async()=>{
  openModal('settingsModal'); $('#settingsMsg').textContent='Loading settings...';
  try{
    const res=await fetch('/api/settings'); const data=await res.json();
    if(data.ok){
      $('#providerInput').value=data.settings.provider||'gemini';
      $('#modelInput').value=data.settings.model||'';
      $('#apiKeyInput').placeholder=data.settings.has_key?`Saved: ${data.settings.masked_key}`:'Paste API key here';
      $('#settingsMsg').textContent=data.settings.has_key?'API key is saved. Leave blank to keep it.':'No API key saved yet.';
    }
  }catch{ $('#settingsMsg').textContent='Could not load settings.'; }
});
$('#saveSettingsBtn')?.addEventListener('click',async()=>{
  $('#settingsMsg').textContent='Saving...';
  try{
    const data=await postJSON('/api/settings',{provider:$('#providerInput').value,model:$('#modelInput').value,api_key:$('#apiKeyInput').value});
    $('#settingsMsg').textContent=data.message||'Saved.'; $('#apiKeyInput').value=''; toast('Settings saved.');
  }catch(err){ $('#settingsMsg').textContent=err.message; }
});

$('#historyBtn')?.addEventListener('click',async()=>{ openModal('historyModal'); await loadHistory(); });
async function loadHistory(){
  const box=$('#historyList'); if(!box) return; box.innerHTML='<p class="muted">Loading...</p>';
  try{
    const res=await fetch('/api/history'); const data=await res.json();
    if(!data.ok) throw new Error(data.error||'History failed');
    if(!data.history.length){ box.innerHTML='<p class="muted">No history yet.</p>'; return; }
    box.innerHTML=data.history.map(h=>`<div class="history-item"><strong><span>${h.tool.replaceAll('_',' ')}</span><span>${h.score_similarity}% similar</span></strong><p><b>Input:</b> ${escapeHTML(h.input_preview||'')}</p><p><b>Output:</b> ${escapeHTML(h.output_preview||'')}</p><p>${new Date(h.created_at).toLocaleString()}</p></div>`).join('');
  }catch(err){ box.innerHTML=`<p class="muted">${escapeHTML(err.message)}</p>`; }
}
$('#clearHistoryBtn')?.addEventListener('click',async()=>{ await postJSON('/api/history/clear',{}); await loadHistory(); toast('History cleared.'); });
function escapeHTML(s){ return String(s).replace(/[&<>'"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c])); }
updateCounts();
