const STOP_WORDS = new Set(['a','an','the','and','or','but','if','then','is','are','was','were','be','been','being','to','of','in','on','for','with','as','by','at','from','this','that','these','those','it','its','into','about','your','you','we','our','their','they','he','she','his','her','them']);

const AI_STYLE_PATTERNS = [
  [/\bin today's (?:fast[- ]paced|digital) world\b/gi, 'currently'],
  [/\bit is important to note that\b/gi, 'notably'],
  [/\bdelve into\b/gi, 'examine'],
  [/\btapestry of\b/gi, 'range of'],
  [/\bleverage\b/gi, 'use'],
  [/\butilize\b/gi, 'use'],
  [/\bunlock the power of\b/gi, 'make better use of'],
  [/\bseamlessly\b/gi, 'smoothly'],
  [/\brobust\b/gi, 'reliable'],
  [/\bmoreover,?\b/gi, 'Also,'],
  [/\bfurthermore,?\b/gi, 'Additionally,'],
  [/\bin conclusion,?\b/gi, 'Overall,'],
  [/\bcutting[- ]edge\b/gi, 'modern'],
  [/\bgame[- ]changer\b/gi, 'useful improvement'],
  [/\bsynergy\b/gi, 'coordination'],
  [/\bholistic\b/gi, 'complete'],
  [/\bpivotal\b/gi, 'important'],
  [/\bparamount\b/gi, 'essential'],
  [/\bcrucial\b/gi, 'important'],
  [/\bembark on\b/gi, 'start'],
  [/\bjourney\b/gi, 'process'],
  [/\brealm\b/gi, 'area'],
  [/\blandscape\b/gi, 'field'],
  [/\bnot only ([^.,;]+) but also\b/gi, '$1 and'],
];

const BIAS_PATTERNS = [
  [/\bblacklist\b/gi, 'block list'],
  [/\bwhitelist\b/gi, 'allow list'],
  [/\bmaster\s*\/\s*slave\b/gi, 'primary/secondary'],
  [/\bmaster branch\b/gi, 'main branch'],
  [/\bcrazy\b/gi, 'unreasonable'],
  [/\binsane\b/gi, 'extreme'],
  [/\blame\b/gi, 'ineffective'],
  [/\bdumb\b/gi, 'unclear'],
  [/\bstupid\b/gi, 'poorly considered'],
];

const PHRASE_MAP = [
  ['complete full face palette', ['all-in-one face palette', 'complete complexion kit', 'full-routine makeup set']],
  ['full face palette', ['complexion-and-eye palette', 'complete face palette', 'all-in-one makeup palette']],
  ['baked icons', ['baked essentials', 'baked complexion collection', 'baked beauty edit']],
  ['baked foundations', ['baked complexion powders', 'baked base products', 'baked foundation shades']],
  ['medium', ['mid-tone', 'balanced mid shade', 'medium']],
  ['travel-friendly', ['easy to carry', 'travel-ready', 'made for daily use and trips']],
  ['coverage for mature skin', ['coverage suited to mature complexions', 'a smooth finish for mature skin', 'buildable coverage for mature-looking skin']],
  ['mature skin', ['mature complexions', 'grown-up skin', 'mature-looking skin']],
  ['bronzer', ['bronzing powder', 'warmth-adding powder', 'sun-kissed face powder']],
  ['highlighter', ['glow enhancer', 'radiance powder', 'illuminating powder']],
  ['eyeshadows', ['eye shades', 'eye colours', 'shadow shades']],
  ['blush', ['cheek colour', 'cheek tint', 'soft cheek powder']],
  ['professional', ['polished', 'business-ready', 'expert-level']],
  ['important', ['essential', 'valuable', 'meaningful']],
  ['good quality', ['high-quality', 'well-made', 'reliable']],
  ['best quality', ['premium quality', 'top-grade', 'high-standard']],
  ['easy to use', ['simple to operate', 'user-friendly', 'straightforward to use']],
  ['without any mistake', ['with fewer errors', 'with careful correction', 'with clean wording']],
  ['proper punctuation', ['clean punctuation', 'correct punctuation', 'well-managed punctuation']],
  ['proper grammar', ['accurate grammar', 'clean grammar', 'grammar-focused wording']],
  ['plagiarism remover', ['originality assistant', 'rewriting assistant', 'text originality tool']],
  ['ai remover', ['AI-style cleaner', 'AI-assisted rewrite mode', 'natural writing mode']],
  ['copy paste', ['unchanged repetition', 'direct duplication', 'same-text output']],
  ['real life', ['practical', 'real-world', 'production-ready']],
  ['industry level', ['professional-grade', 'client-ready', 'commercial-quality']],
  ['each and everything', ['all important details', 'the full content', 'every key point']],
  ['in order to', ['to', 'so it can', 'for the purpose of']],
  ['due to the fact that', ['because', 'since', 'as']],
  ['a large number of', ['many', 'numerous', 'a wide range of']],
  ['at this point in time', ['now', 'currently', 'at present']],
  ['has the ability to', ['can', 'is able to', 'is designed to']],
  ['make sure', ['ensure', 'confirm', 'check']],
  ['help users', ['support users', 'assist users', 'help people']],
  ['very important', ['essential', 'highly important', 'critical']],
  ['high quality', ['premium-quality', 'high-standard', 'well-crafted']],
  ['beautiful interface', ['polished interface', 'premium interface', 'clean modern interface']],
  ['uploaded text', ['submitted text', 'provided content', 'imported document text']],
  ['synonym text', ['rewritten wording', 'fresh phrasing', 'alternative wording']],
  ['grammar and punctuation', ['grammar, flow, and punctuation', 'sentence mechanics and punctuation', 'language accuracy']],
  ['same meaning', ['original meaning', 'core message', 'main idea']],
  ['keyword stuffing', ['overloaded keyword repetition', 'excessive keyword use', 'unnatural keyword density']],
  ['search engine optimization', ['SEO', 'search visibility improvement', 'search optimization']],
  ['user experience', ['UX', 'visitor experience', 'reader experience']],
  ['digital product', ['downloadable product', 'online product', 'commercial digital tool']],
  ['source citation', ['proper citation', 'reference to the source', 'source acknowledgement']],
  ['academic writing', ['scholarly writing', 'formal academic text', 'research-style writing']],
  ['product description', ['item description', 'commerce-focused description', 'shopper-friendly description']],
  ['social media', ['online platforms', 'social platforms', 'social channels']],
  ['better result', ['stronger result', 'improved output', 'higher-quality version']],
  ['rewrite text', ['rephrase the content', 'rework the wording', 'produce a revised version']],
  ['natural language', ['human-sounding wording', 'clear language', 'natural wording']],
  ['clear and concise', ['direct and easy to read', 'clear and focused', 'simple and precise']],
  ['black racism', ['biased or harmful wording', 'racially biased wording', 'discriminatory language']],
  ['racist language', ['discriminatory wording', 'biased phrasing', 'harmful group-based language']],
  ['hate speech', ['harmful abusive language', 'dehumanizing wording', 'targeted abusive language']],
];

const SYNONYMS = {
  // writing/tool/project words
  make: ['create','build','produce','develop'], made: ['created','built','prepared','developed'], making: ['creating','building','preparing','developing'],
  get: ['receive','obtain','generate','produce'], getting: ['receiving','generating','producing','creating'], give: ['provide','offer','deliver','supply'],
  add: ['include','insert','integrate','attach'], added: ['included','integrated','inserted','attached'], remove: ['reduce','replace','clean','eliminate'], removing: ['reducing','replacing','cleaning','eliminating'],
  convert: ['transform','rework','turn','rewrite'], change: ['adjust','revise','modify','reshape'],
  text: ['content','writing','copy','material'], document: ['file','written piece','draft','content'], uploaded: ['imported','submitted','provided','loaded'],
  proper: ['well-structured','accurate','polished','correct'], professional: ['polished','business-ready','client-ready','commercial-grade'], functional: ['working','usable','operational','practical'],
  working: ['operational','usable','functioning','production-ready'], real: ['practical','actual','real-world','usable'], life: ['world','use','deployment','environment'],
  industry: ['commercial','professional','production','market'], level: ['grade','standard','quality','class'],
  algorithm: ['rule-based engine','rewriting engine','local processor','text engine'], ai: ['AI-assisted','model-powered','intelligent','automated'],
  plagiarism: ['text overlap','duplicated wording','similar phrasing','source overlap'], similarity: ['overlap','matching','resemblance','duplication'], original: ['fresh','new','distinct','rewritten'], originality: ['uniqueness','distinctiveness','freshness','novelty'],
  grammar: ['language accuracy','sentence structure','writing mechanics','grammar quality'], punctuation: ['sentence marks','writing marks','punctuation flow','mechanics'],
  mistake: ['error','issue','problem','fault'], mistakes: ['errors','issues','problems','faults'],
  synonym: ['alternative wording','replacement term','fresh wording','rephrased expression'], synonyms: ['alternative terms','replacement words','fresh wording','rephrased expressions'],
  replace: ['substitute','swap','change','reword'], replacing: ['substituting','swapping','rewording','changing'],
  design: ['interface','layout','visual system','presentation'], designing: ['interface design','layout work','visual design','presentation'],
  beautiful: ['polished','attractive','premium','clean'], interface: ['dashboard','workspace','web page','UI'], website: ['web app','site','online tool','platform'],
  deploy: ['publish','host','launch','release'], deployed: ['published','hosted','launched','released'], netlify: ['Netlify'], vercel: ['Vercel'],
  client: ['customer','buyer','user','customer'], clients: ['customers','buyers','users','customers'], sell: ['market','offer','publish','sell'], gumroad: ['Gumroad'],

  // product/ecommerce
  palette: ['kit','collection','set','compact'], palettes: ['kits','collections','sets','compacts'], foundation: ['base product','complexion product','base powder','foundation'], foundations: ['base products','complexion powders','foundation shades','base powders'],
  blush: ['cheek colour','cheek powder','cheek tint','blush'], bronzer: ['bronzing powder','warmth powder','bronzer','sun-kissed powder'],
  highlighter: ['glow enhancer','radiance powder','illuminator','highlighter'], eyeshadows: ['eye colours','shadow shades','eye shades','eyeshadows'],
  coverage: ['finish','base coverage','complexion finish','coverage'], mature: ['grown-up','mature-looking','refined','mature'], skin: ['complexion','skin type','face','skin'],
  travel: ['portable','trip-ready','travel','on-the-go'], friendly: ['suitable','ready','convenient','easy'], complete: ['all-in-one','full','comprehensive','complete'],
  medium: ['mid-tone','balanced mid shade','medium','medium'], icons: ['essentials','signature items','hero pieces','icons'], baked: ['baked','pressed-baked','oven-baked','baked-finish'],

  // general academic/professional
  important: ['essential','valuable','significant','key'], simple: ['clear','straightforward','easy','plain'], detailed: ['thorough','complete','well-explained','in-depth'],
  improve: ['enhance','upgrade','refine','strengthen'], improved: ['enhanced','upgraded','refined','strengthened'], better: ['stronger','improved','clearer','more effective'],
  best: ['strongest','most suitable','highest-quality','most effective'], high: ['strong','advanced','premium','elevated'], quality: ['standard','finish','value','craftsmanship'],
  powerful: ['strong','effective','capable','high-performing'], strong: ['solid','effective','advanced','strong'], weak: ['limited','basic','less effective','weak'],
  analyze: ['examine','review','study','evaluate'], explain: ['describe','clarify','break down','explain'], show: ['display','present','show','demonstrate'],
  create: ['produce','build','generate','develop'], generate: ['produce','create','prepare','form'], output: ['result','rewritten version','final text','output'], input: ['source text','original text','submitted text','input'],
  sentence: ['line','statement','sentence','phrase'], sentences: ['lines','statements','sentences','phrases'], word: ['term','word','expression','phrase'], words: ['terms','words','expressions','phrases'],
  meaning: ['sense','message','idea','meaning'], idea: ['concept','point','message','idea'], ideas: ['concepts','points','messages','ideas'],
  use: ['apply','use','work with','utilize'], using: ['applying','using','working with','utilizing'],
  check: ['review','inspect','verify','check'], checker: ['review tool','scanner','checker','analyzer'],
  fast: ['quick','rapid','speedy','fast'], free: ['no-cost','free','open','free'], paid: ['premium','paid','commercial','paid'],
  online: ['web-based','internet-based','online','digital'], local: ['on-device','built-in','local','browser-based'],
  safe: ['responsible','secure','safe','careful'], ethical: ['responsible','fair','ethical','proper'],

  // transitions/AI style
  additionally: ['also','in addition','another point is','further'], therefore: ['as a result','so','for that reason','therefore'], however: ['still','yet','however','on the other hand'],
  because: ['since','as','because','for the reason that'], therefore: ['so','as a result','therefore','for that reason'],
};

function hashChoice(seedText, arr, offset = 0) {
  if (!arr || arr.length === 0) return seedText;
  let h = 0;
  const s = String(seedText) + ':' + offset;
  for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) >>> 0;
  return arr[h % arr.length];
}

function preserveCase(source, replacement) {
  if (!source) return replacement;
  if (source.toUpperCase() === source && source.length > 1) return replacement.toUpperCase();
  if (source[0] === source[0].toUpperCase()) return replacement.charAt(0).toUpperCase() + replacement.slice(1);
  return replacement;
}

function cleanSpacing(text) {
  return String(text || '')
    .replace(/\r\n/g, '\n')
    .replace(/[ \t]+/g, ' ')
    .replace(/\s+([,.;:!?])/g, '$1')
    .replace(/([,.;:!?])([^\s\n])/g, '$1 $2')
    .replace(/\s+\n/g, '\n')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

function sentenceSplit(paragraph) {
  const parts = paragraph.match(/[^.!?]+[.!?]+|[^.!?]+$/g);
  return parts ? parts.map(s => s.trim()).filter(Boolean) : [];
}

function wordCount(text) {
  return (String(text || '').match(/[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?/g) || []).length;
}

function applyPatterns(text, patterns) {
  let out = text;
  for (const [pattern, replacement] of patterns) out = out.replace(pattern, replacement);
  return out;
}

function applyPhraseMap(text, intensity = 2) {
  let out = text;
  for (const [phrase, replacements] of PHRASE_MAP) {
    const re = new RegExp('\\b' + phrase.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\b', 'gi');
    out = out.replace(re, match => preserveCase(match, hashChoice(match, replacements, intensity)));
  }
  return out;
}

function shouldProtectToken(token, prev, index) {
  const clean = token.replace(/[^A-Za-z0-9-]/g, '');
  if (!clean) return true;
  if (/^\d/.test(clean)) return true;
  if (clean.length <= 2) return true;
  if (/^[A-Z]{2,}$/.test(clean)) return true; // brands / acronyms
  if (/https?:|www\.|@/.test(token)) return true;
  if (index > 0 && /^[A-Z][a-z]+$/.test(clean) && prev && !/[.!?]$/.test(prev)) return true; // likely proper noun
  return false;
}

function applySynonyms(text, strength = 'balanced') {
  const ratio = strength === 'maximum' ? 0.95 : strength === 'strong' ? 0.72 : strength === 'balanced' ? 0.52 : 0.28;
  const tokens = text.split(/(\s+|[^A-Za-z0-9'-]+)/g).filter(t => t !== '');
  let out = '';
  let prev = '';
  let wordIndex = 0;
  for (const tok of tokens) {
    if (!/[A-Za-z]/.test(tok)) { out += tok; prev = tok; continue; }
    const clean = tok.replace(/^[^A-Za-z0-9']+|[^A-Za-z0-9']+$/g, '');
    const key = clean.toLowerCase();
    if (SYNONYMS[key] && !shouldProtectToken(tok, prev, wordIndex)) {
      const changeGate = ((wordIndex * 37 + key.length * 11) % 100) / 100;
      if (changeGate <= ratio && !STOP_WORDS.has(key)) {
        const replacement = hashChoice(key + wordIndex, SYNONYMS[key], strength.length);
        out += tok.replace(clean, preserveCase(clean, replacement));
      } else out += tok;
    } else out += tok;
    prev = tok;
    wordIndex++;
  }
  return out;
}

function recastSentence(sentence, mode = 'professional', strength = 'balanced') {
  let s = sentence.trim();
  if (!s) return s;
  const hadEnd = /[.!?]$/.test(s);
  s = s.replace(/[.!?]+$/, '');

  const templates = [];
  const lower = s.toLowerCase();
  if (/\b(is|are)\b/.test(lower) && /\b(that|which)\b/.test(lower)) {
    s = s.replace(/^(.+?)\s+(is|are)\s+(a|an|the)?\s*(.+?)\s+that\s+(.+)$/i, (m, subject, verb, art, object, rest) => {
      const loweredSubject = subject.charAt(0).toLowerCase() + subject.slice(1);
      return `Designed as ${art ? art + ' ' : ''}${object}, ${loweredSubject} ${rest}`;
    });
  }
  s = s.replace(/^This\s+(.+?)\s+(helps|allows|lets)\s+(.+?)\s+to\s+(.+)$/i, (m, thing, verb, who, action) => {
    return `With this ${thing}, ${who} can ${action}`;
  });
  s = s.replace(/^It\s+(includes|contains|offers|provides)\s+(.+)$/i, (m, verb, rest) => {
    const v = verb.toLowerCase() === 'contains' ? 'comes with' : verb.toLowerCase();
    return `The package ${v} ${rest}`;
  });
  s = s.replace(/^The\s+(.+?)\s+is\s+designed\s+to\s+(.+)$/i, (m, thing, rest) => {
    return `Designed for ${rest}, the ${thing}`;
  });

  if (strength === 'maximum' || strength === 'strong') {
    s = s.replace(/,\s*because\s+(.+)$/i, (m, reason) => `, mainly because ${reason}`);
    s = s.replace(/\bcan help\b/gi, 'can support');
    s = s.replace(/\bwill help\b/gi, 'is built to support');
    s = s.replace(/\bvery\s+/gi, 'highly ');
  }

  if (mode === 'academic') {
    s = s.replace(/\bI\b/g, 'the writer').replace(/\bwe\b/gi, 'the discussion');
    if (!/^(Overall|Furthermore|Additionally|In this context|From this perspective)/i.test(s) && wordCount(s) > 12) {
      templates.push(`In this context, ${s.charAt(0).toLowerCase()}${s.slice(1)}`);
    }
  } else if (mode === 'ecommerce') {
    if (/\b(product|palette|kit|collection|foundation|bronzer|blush|highlighter|eyeshadow|skin|coverage)\b/i.test(s) && wordCount(s) > 7) {
      templates.push(`Built for a polished routine, ${s.charAt(0).toLowerCase()}${s.slice(1)}`);
    }
  } else if (mode === 'simple') {
    s = s.replace(/\bapproximately\b/gi, 'about').replace(/\btherefore\b/gi, 'so').replace(/\butilize\b/gi, 'use');
  } else if (mode === 'creative') {
    if (wordCount(s) > 10) templates.push(`With a smoother flow, ${s.charAt(0).toLowerCase()}${s.slice(1)}`);
  }

  if (templates.length && (strength === 'strong' || strength === 'maximum')) s = hashChoice(s, templates, strength.length);
  s = s.charAt(0).toUpperCase() + s.slice(1);
  return s + (hadEnd ? sentence.match(/[.!?]$/)?.[0] || '.' : '.');
}

function isProductLike(text) {
  const t = String(text || '');
  const separators = (t.match(/[|,;•]/g) || []).length;
  const commerceWords = /(palette|foundation|bronzer|blush|highlighter|eyeshadow|cream|serum|product|coverage|skin|travel|friendly|medium|shade|baked|makeup|kit|collection)/i.test(t);
  return t.length < 500 && commerceWords && separators >= 2;
}

function titleCaseToReadable(text) {
  return text.replace(/\b([A-Z][A-Z]+)\b/g, m => m)
    .replace(/\b([A-Z][a-z]+)\b/g, (m, w, idx) => idx === 0 ? w : w.toLowerCase());
}

function rewriteProductText(text, options) {
  const parts = text.split(/[|•;]+|,(?=\s*[A-Za-z])/).map(p => p.trim()).filter(Boolean);
  const cleanParts = parts.map(p => cleanSpacing(applyPhraseMap(titleCaseToReadable(p), 3)));
  const brandChunk = cleanParts[0] || 'This product';
  const features = cleanParts.slice(1);
  const normalizedFeatures = features.map(f => {
    const lower = f.toLowerCase();
    if (/travel|portable|trip|carry/.test(lower)) return 'portable packaging for everyday routines and trips';
    if (/mature/.test(lower)) return 'a smooth, buildable finish for mature-looking complexions';
    return f.charAt(0).toLowerCase() + f.slice(1);
  });
  const featureSentence = normalizedFeatures.length
    ? `It brings together ${normalizedFeatures.join(', ').replace(/, ([^,]*)$/, ', and $1')}.`
    : '';
  let base = `${brandChunk} is presented as a polished, ready-to-use beauty solution for a cleaner daily routine. ${featureSentence} The wording is refined into a more natural product description while keeping the core details, shade information, and purpose clear for shoppers.`;
  base = applyPhraseMap(base, 4);
  base = applySynonyms(base, options.strength);
  return cleanSpacing(base);
}

function enhanceParagraph(paragraph, options) {
  let p = cleanSpacing(paragraph);
  if (!p) return '';
  p = applyPatterns(p, AI_STYLE_PATTERNS);
  if (options.biasClean) p = applyPatterns(p, BIAS_PATTERNS);
  if (isProductLike(p) && options.mode === 'ecommerce') return rewriteProductText(p, options);
  p = applyPhraseMap(p, options.strength === 'maximum' ? 4 : 2);
  p = applySynonyms(p, options.strength);
  const sentences = sentenceSplit(p);
  const recast = sentences.map(s => recastSentence(s, options.mode, options.strength));
  let out = recast.join(' ');
  if (options.strength === 'maximum') {
    out = out.replace(/\b(.{18,}?)\s+and\s+(.{18,}?)([.!?])/gi, '$1. Additionally, $2$3');
  }
  return cleanSpacing(out);
}

function polishText(text) {
  let out = cleanSpacing(text);
  out = out.replace(/\bi\b/g, 'I');
  out = out.replace(/\s+([.,!?;:])/g, '$1');
  out = out.replace(/([.!?])\s*([a-z])/g, (m, p, c) => `${p} ${c.toUpperCase()}`);
  out = out.replace(/\b([A-Za-z]+)\s+\1\b/gi, '$1');
  out = out.replace(/\s{2,}/g, ' ');
  out = out.replace(/\n /g, '\n');
  return out.trim();
}

function tokenize(text) {
  return (String(text || '').toLowerCase().match(/[a-z0-9]+/g) || []).filter(w => !STOP_WORDS.has(w));
}

function ngrams(tokens, n) {
  const out = [];
  for (let i = 0; i <= tokens.length - n; i++) out.push(tokens.slice(i, i+n).join(' '));
  return out;
}

function jaccard(a, b) {
  const A = new Set(a), B = new Set(b);
  if (!A.size && !B.size) return 0;
  let inter = 0;
  for (const x of A) if (B.has(x)) inter++;
  return inter / (A.size + B.size - inter || 1);
}

function similarityScores(original, rewritten) {
  const ot = tokenize(original), rt = tokenize(rewritten);
  const unigram = jaccard(ot, rt);
  const bigram = jaccard(ngrams(ot, 2), ngrams(rt, 2));
  const trigram = jaccard(ngrams(ot, 3), ngrams(rt, 3));
  const phraseOverlap = Math.round(((bigram * 0.55) + (trigram * 0.45)) * 100);
  const estimatedSimilarity = Math.round(((unigram * 0.45) + (bigram * 0.35) + (trigram * 0.20)) * 100);
  return {
    estimatedSimilarity,
    originalityLift: Math.max(0, 100 - estimatedSimilarity),
    phraseOverlap,
    originalWords: wordCount(original),
    rewrittenWords: wordCount(rewritten),
    changedWords: Math.max(0, wordCount(original) - Math.round(unigram * wordCount(original)))
  };
}

function readability(text) {
  const words = wordCount(text) || 1;
  const sentences = Math.max(1, sentenceSplit(text).length);
  const avg = words / sentences;
  let score = 100 - Math.abs(avg - 16) * 2.2;
  score = Math.max(35, Math.min(98, Math.round(score)));
  return score;
}

function createNotes(metrics, options, usedAI = false) {
  const notes = [];
  if (usedAI) notes.push('AI Rewrite Assist was used through the server-side provider. Review facts, citations, and meaning before publishing.');
  if (!usedAI && options.engine === 'ai') notes.push('AI provider was not configured, so the app used the advanced algorithm fallback. Add GEMINI_API_KEY in Netlify for true AI-assisted rewriting.');
  if (metrics.estimatedSimilarity > 55) notes.push('Similarity is still high. Try Maximum strength, E-commerce/Academic mode, or add your own examples and details.');
  if (metrics.phraseOverlap > 35) notes.push('Phrase overlap is noticeable. Review repeated phrases and add source citations where ideas came from another source.');
  if (options.biasClean) notes.push('Bias Cleaner checked for common harmful or outdated phrasing and replaced safer alternatives when detected.');
  notes.push('This tool rewrites wording and structure; it does not check the internet or guarantee plagiarism removal. Proper citations are still required.');
  return notes;
}

export function rewriteText(input, rawOptions = {}) {
  const options = {
    engine: rawOptions.engine || 'algorithm',
    mode: rawOptions.mode || 'professional',
    strength: rawOptions.strength || 'strong',
    biasClean: rawOptions.biasClean !== false,
  };
  const original = cleanSpacing(input || '');
  if (!original) {
    return { rewritten: '', metrics: similarityScores('', ''), readability: 0, notes: ['Add text to rewrite.'] };
  }
  const paragraphs = original.split(/\n{2,}/).map(p => p.trim()).filter(Boolean);
  let rewritten = paragraphs.map(p => enhanceParagraph(p, options)).join('\n\n');
  rewritten = polishText(rewritten);
  const metrics = similarityScores(original, rewritten);
  return {
    rewritten,
    metrics: { ...metrics, readability: readability(rewritten) },
    notes: createNotes(metrics, options, false),
    engineUsed: 'algorithm'
  };
}

export { cleanSpacing, applyPatterns, AI_STYLE_PATTERNS, BIAS_PATTERNS, similarityScores, readability, createNotes, wordCount };
