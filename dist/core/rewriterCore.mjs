const phraseRules = [
  [/in this essay\b/gi, 'throughout this discussion'],
  [/in this paper\b/gi, 'within this paper'],
  [/in this article\b/gi, 'in the article'],
  [/nowadays\b/gi, 'in the present era'],
  [/in today's world\b/gi, 'in the current digital landscape'],
  [/in the modern world\b/gi, 'in contemporary society'],
  [/with the passage of time\b/gi, 'over time'],
  [/due to the fact that\b/gi, 'because'],
  [/in order to\b/gi, 'to'],
  [/for the purpose of\b/gi, 'to'],
  [/a lot of\b/gi, 'many'],
  [/lots of\b/gi, 'many'],
  [/very important\b/gi, 'highly significant'],
  [/plays a vital role\b/gi, 'has a major influence'],
  [/plays an important role\b/gi, 'makes a meaningful contribution'],
  [/has become very important\b/gi, 'has gained considerable importance'],
  [/is very important\b/gi, 'is highly significant'],
  [/is important because\b/gi, 'matters because'],
  [/this means that\b/gi, 'this suggests that'],
  [/this shows that\b/gi, 'this demonstrates that'],
  [/it is important to note that\b/gi, 'notably'],
  [/it can be said that\b/gi, 'it can be argued that'],
  [/as we know\b/gi, 'as commonly understood'],
  [/in conclusion\b/gi, 'to conclude'],
  [/to sum up\b/gi, 'in summary'],
  [/on the other hand\b/gi, 'from another perspective'],
  [/at the same time\b/gi, 'simultaneously'],
  [/more and more\b/gi, 'an increasing number of'],
  [/day by day\b/gi, 'gradually'],
  [/people can\b/gi, 'individuals can'],
  [/people are able to\b/gi, 'individuals are able to'],
  [/helps people\b/gi, 'enables individuals to'],
  [/make better decisions\b/gi, 'reach more informed decisions'],
  [/complete difficult tasks\b/gi, 'handle complex tasks'],
  [/reduce manual work\b/gi, 'lower repetitive manual effort'],
  [/improve productivity\b/gi, 'increase productivity'],
  [/get good results\b/gi, 'achieve stronger outcomes'],
  [/good quality\b/gi, 'reliable quality'],
  [/high quality\b/gi, 'premium quality'],
  [/proper way\b/gi, 'structured approach'],
  [/main reason\b/gi, 'primary reason'],
  [/main purpose\b/gi, 'primary purpose'],
  [/important factor\b/gi, 'significant factor'],
  [/major problem\b/gi, 'serious challenge'],
  [/modern technology\b/gi, 'contemporary technology'],
  [/new technology\b/gi, 'emerging technology'],
  [/artificial intelligence\b/gi, 'AI technology'],
  [/AI writing\b/gi, 'AI-supported writing'],
  [/must be reviewed carefully\b/gi, 'needs careful review'],
  [/maintain quality\b/gi, 'preserve quality'],
  [/maintain originality\b/gi, 'support originality'],
  [/without any doubt\b/gi, 'undoubtedly'],
  [/in my opinion\b/gi, 'from my perspective'],
  [/for example\b/gi, 'for instance'],
  [/because of this\b/gi, 'therefore'],
  [/as a result\b/gi, 'consequently'],
  [/in addition\b/gi, 'furthermore'],
  [/try to\b/gi, 'attempt to'],
  [/need to\b/gi, 'should'],
  [/able to\b/gi, 'capable of'],
  [/can help\b/gi, 'can support'],
  [/can improve\b/gi, 'can strengthen'],
  [/can reduce\b/gi, 'can decrease'],
  [/can make\b/gi, 'can create'],
  [/is based on\b/gi, 'depends on'],
  [/depends on\b/gi, 'is shaped by'],
  [/there are many\b/gi, 'several'],
  [/there is a need for\b/gi, 'there is a requirement for'],
  [/is used to\b/gi, 'is applied to'],
  [/are used to\b/gi, 'are applied to'],
  [/useful for\b/gi, 'valuable for'],
  [/works as\b/gi, 'functions as'],
  [/in a better way\b/gi, 'more effectively'],
  [/each and everything\b/gi, 'every important detail'],
  [/100%\b/gi, 'highly'],
  [/copy paste\b/gi, 'direct copying'],
  [/remove plagiarism\b/gi, 'reduce textual overlap'],
  [/plagiarism remover\b/gi, 'originality assistant']
];

const synonyms = {
  important: ['significant', 'essential', 'meaningful', 'valuable', 'critical'],
  modern: ['contemporary', 'current', 'present-day', 'advanced'],
  world: ['society', 'environment', 'landscape', 'context'],
  help: ['support', 'assist', 'enable', 'guide'],
  helps: ['supports', 'assists', 'enables', 'guides'],
  helped: ['supported', 'assisted', 'enabled', 'guided'],
  improve: ['enhance', 'strengthen', 'refine', 'upgrade'],
  improves: ['enhances', 'strengthens', 'refines', 'upgrades'],
  improved: ['enhanced', 'strengthened', 'refined', 'upgraded'],
  productivity: ['efficiency', 'output', 'work performance', 'productive capacity'],
  reduce: ['decrease', 'minimize', 'lower', 'limit'],
  reduces: ['decreases', 'minimizes', 'lowers', 'limits'],
  reduced: ['decreased', 'minimized', 'lowered', 'limited'],
  manual: ['hands-on', 'human-performed', 'repetitive', 'non-automated'],
  work: ['effort', 'tasks', 'operations', 'activities'],
  decisions: ['choices', 'judgments', 'conclusions', 'evaluations'],
  decision: ['choice', 'judgment', 'conclusion', 'evaluation'],
  difficult: ['complex', 'challenging', 'demanding', 'hard'],
  task: ['activity', 'operation', 'assignment', 'process'],
  tasks: ['activities', 'operations', 'assignments', 'processes'],
  quickly: ['efficiently', 'rapidly', 'in less time', 'more quickly'],
  carefully: ['thoroughly', 'attentively', 'with care', 'critically'],
  understand: ['recognize', 'realize', 'grasp', 'know'],
  writing: ['content', 'drafting', 'written material', 'composition'],
  quality: ['standard', 'clarity', 'value', 'overall finish'],
  originality: ['uniqueness', 'freshness', 'authenticity', 'individuality'],
  many: ['several', 'numerous', 'multiple', 'various'],
  companies: ['organizations', 'businesses', 'firms', 'enterprises'],
  company: ['organization', 'business', 'firm', 'enterprise'],
  people: ['individuals', 'users', 'learners', 'professionals'],
  users: ['people', 'individuals', 'readers', 'customers'],
  use: ['apply', 'utilize', 'employ', 'adopt'],
  uses: ['applies', 'utilizes', 'employs', 'adopts'],
  using: ['applying', 'utilizing', 'employing', 'adopting'],
  create: ['develop', 'produce', 'build', 'generate'],
  creates: ['develops', 'produces', 'builds', 'generates'],
  created: ['developed', 'produced', 'built', 'generated'],
  make: ['create', 'develop', 'produce', 'form'],
  makes: ['creates', 'develops', 'produces', 'forms'],
  made: ['created', 'developed', 'produced', 'formed'],
  good: ['effective', 'reliable', 'strong', 'useful'],
  bad: ['weak', 'poor', 'limited', 'ineffective'],
  big: ['large', 'major', 'substantial', 'considerable'],
  small: ['minor', 'limited', 'compact', 'modest'],
  change: ['adjust', 'modify', 'revise', 'reshape'],
  changes: ['adjustments', 'modifications', 'revisions', 'shifts'],
  idea: ['concept', 'approach', 'strategy', 'viewpoint'],
  ideas: ['concepts', 'approaches', 'strategies', 'viewpoints'],
  problem: ['challenge', 'issue', 'concern', 'difficulty'],
  problems: ['challenges', 'issues', 'concerns', 'difficulties'],
  solution: ['approach', 'method', 'answer', 'remedy'],
  solutions: ['approaches', 'methods', 'answers', 'remedies'],
  result: ['outcome', 'effect', 'output', 'consequence'],
  results: ['outcomes', 'effects', 'outputs', 'consequences'],
  because: ['since', 'as', 'for the reason that'],
  therefore: ['consequently', 'as a result', 'for this reason'],
  however: ['nevertheless', 'even so', 'on the other hand'],
  also: ['additionally', 'furthermore', 'along with this'],
  easy: ['simple', 'straightforward', 'manageable', 'user-friendly'],
  hard: ['difficult', 'challenging', 'complex', 'demanding'],
  fast: ['quick', 'rapid', 'efficient', 'speedy'],
  slow: ['gradual', 'delayed', 'less immediate', 'slower'],
  text: ['content', 'writing', 'material', 'passage'],
  plagiarism: ['textual overlap', 'unoriginal similarity', 'content duplication', 'source overlap'],
  remove: ['reduce', 'minimize', 'lower', 'decrease'],
  project: ['product', 'tool', 'application', 'system'],
  website: ['web app', 'online platform', 'site', 'browser-based tool'],
  professional: ['polished', 'business-ready', 'industry-level', 'premium'],
  beautiful: ['clean', 'modern', 'attractive', 'elegant'],
  analyze: ['review', 'examine', 'evaluate', 'study'],
  explain: ['clarify', 'describe', 'break down', 'outline'],
  strong: ['powerful', 'solid', 'effective', 'robust'],
  weak: ['limited', 'less effective', 'underdeveloped', 'thin'],
  information: ['details', 'data', 'knowledge', 'insight'],
  technology: ['digital technology', 'technical system', 'innovation', 'tooling'],
  application: ['app', 'system', 'platform', 'tool'],
  system: ['platform', 'framework', 'setup', 'solution'],
  process: ['method', 'workflow', 'procedure', 'approach'],
  learning: ['education', 'study', 'knowledge-building', 'training'],
  student: ['learner', 'pupil', 'academic user', 'trainee'],
  students: ['learners', 'pupils', 'academic users', 'trainees'],
  research: ['study', 'investigation', 'analysis', 'inquiry'],
  academic: ['scholarly', 'educational', 'research-based', 'formal'],
  content: ['material', 'writing', 'copy', 'text'],
  original: ['unique', 'fresh', 'independent', 'distinct'],
  similar: ['related', 'comparable', 'close', 'matching'],
  different: ['distinct', 'separate', 'varied', 'alternative'],
  increase: ['raise', 'boost', 'expand', 'strengthen'],
  increasing: ['rising', 'growing', 'expanding', 'strengthening'],
  decrease: ['reduce', 'lower', 'minimize', 'cut'],
  develop: ['build', 'create', 'shape', 'produce'],
  development: ['growth', 'creation', 'progress', 'improvement'],
  advanced: ['high-level', 'sophisticated', 'modern', 'improved'],
  basic: ['simple', 'foundational', 'entry-level', 'core'],
  benefit: ['advantage', 'value', 'gain', 'positive outcome'],
  benefits: ['advantages', 'value', 'gains', 'positive outcomes'],
  effective: ['useful', 'successful', 'practical', 'reliable'],
  efficient: ['productive', 'time-saving', 'streamlined', 'optimized'],
  accurate: ['precise', 'reliable', 'correct', 'well-aligned'],
  include: ['contain', 'cover', 'feature', 'involve'],
  includes: ['contains', 'covers', 'features', 'involves'],
  including: ['covering', 'featuring', 'involving', 'containing'],
  need: ['require', 'demand', 'call for', 'depend on'],
  needs: ['requires', 'demands', 'calls for', 'depends on'],
  best: ['strongest', 'most suitable', 'most effective', 'top'],
  proper: ['structured', 'suitable', 'correct', 'well-organized'],
  design: ['layout', 'interface', 'visual structure', 'presentation'],
  page: ['screen', 'interface', 'webpage', 'view'],
  sell: ['offer', 'market', 'distribute', 'commercialize'],
  client: ['customer', 'buyer', 'user', 'end user'],
  clients: ['customers', 'buyers', 'users', 'end users'],
  relevant: ['related', 'connected', 'useful', 'applicable'],
  advanced: ['sophisticated', 'high-level', 'improved', 'modernized'],
  accurate: ['precise', 'reliable', 'well-aligned', 'correct'],
  original: ['fresh', 'independent', 'distinct', 'unique'],
  readable: ['clear', 'easy to follow', 'smooth', 'understandable']
};

const modeProfiles = {
  academic: {
    label: 'Academic',
    transitions: ['Moreover,', 'Furthermore,', 'From an academic perspective,', 'This indicates that', 'Consequently,', 'In addition,'],
    toneWords: [
      [/\bI think\b/gi, 'it can be argued'],
      [/\bwe can see\b/gi, 'it can be observed'],
      [/\ba lot\b/gi, 'a considerable amount'],
      [/\bthings\b/gi, 'factors'],
      [/\bshows\b/gi, 'demonstrates'],
      [/\bprove\b/gi, 'support']
    ]
  },
  professional: {
    label: 'Professional',
    transitions: ['Practically,', 'In business terms,', 'More importantly,', 'As a result,', 'This creates', 'Strategically,'],
    toneWords: [
      [/\bbad\b/gi, 'ineffective'],
      [/\bvery good\b/gi, 'highly effective'],
      [/\bthing\b/gi, 'factor'],
      [/\bstuff\b/gi, 'material'],
      [/\bget\b/gi, 'receive'],
      [/\bfix\b/gi, 'resolve']
    ]
  },
  simple: {
    label: 'Simple',
    transitions: ['Also,', 'Because of this,', 'In simple words,', 'Another point is that', 'So,', 'This means'],
    toneWords: [
      [/\butilize\b/gi, 'use'],
      [/\bdemonstrate\b/gi, 'show'],
      [/\bapproximately\b/gi, 'about'],
      [/\btherefore\b/gi, 'so'],
      [/\bsubsequently\b/gi, 'after that']
    ]
  },
  creative: {
    label: 'Creative',
    transitions: ['Interestingly,', 'At the same time,', 'Beyond that,', 'In a deeper sense,', 'This gives the idea', 'On a wider level,'],
    toneWords: [
      [/\bimportant\b/gi, 'meaningful'],
      [/\bproblem\b/gi, 'challenge'],
      [/\bsolution\b/gi, 'way forward'],
      [/\bresult\b/gi, 'outcome']
    ]
  },
  human: {
    label: 'Human',
    transitions: ['In practice,', 'What this really means is', 'Another way to look at it is', 'That is why', 'At the same time,'],
    toneWords: [
      [/\butilize\b/gi, 'use'],
      [/\bcommence\b/gi, 'start'],
      [/\bfacilitate\b/gi, 'help'],
      [/\bindividuals\b/gi, 'people'],
      [/\bapproximately\b/gi, 'around']
    ]
  }
};

const intensities = {
  light: { synonymRate: 0.28, restructureRate: 0.2, transitionRate: 0.1, splitRate: 0.08, combineRate: 0.06 },
  balanced: { synonymRate: 0.48, restructureRate: 0.48, transitionRate: 0.22, splitRate: 0.18, combineRate: 0.14 },
  strong: { synonymRate: 0.68, restructureRate: 0.74, transitionRate: 0.34, splitRate: 0.3, combineRate: 0.22 },
  maximum: { synonymRate: 0.84, restructureRate: 0.94, transitionRate: 0.5, splitRate: 0.42, combineRate: 0.3 }
};

const stopwords = new Set('a an the and or but if then than to of in on at for from by with about into through during before after above below under over between among is are was were be been being have has had do does did can could should would may might must will shall it this that these those i we you he she they them his her their our your as because while so such not no yes very just only also'.split(' '));

function normalizeInput(text) {
  return String(text || '')
    .replace(/\r/g, '')
    .replace(/[\t ]+/g, ' ')
    .replace(/\s+([,.!?;:])/g, '$1')
    .replace(/([,.!?;:])([^\s\n])/g, '$1 $2')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

function splitSentences(text) {
  const cleaned = normalizeInput(text);
  if (!cleaned) return [];
  const pieces = cleaned.match(/[^.!?]+[.!?]+|[^.!?]+$/g) || [cleaned];
  return pieces.map(s => s.trim()).filter(Boolean);
}

function capitalize(text) {
  if (!text) return text;
  return text.charAt(0).toUpperCase() + text.slice(1);
}

function preserveCase(original, replacement) {
  if (!original) return replacement;
  if (original.toUpperCase() === original) return replacement.toUpperCase();
  if (original[0] === original[0].toUpperCase()) return capitalize(replacement);
  return replacement;
}

function seededIndex(word, sentenceIndex, offset, length) {
  let hash = 2166136261;
  const source = `${word}:${sentenceIndex}:${offset}`;
  for (let i = 0; i < source.length; i++) {
    hash ^= source.charCodeAt(i);
    hash += (hash << 1) + (hash << 4) + (hash << 7) + (hash << 8) + (hash << 24);
  }
  return Math.abs(hash >>> 0) % length;
}

function applyPhraseRules(sentence, profile) {
  let output = sentence;
  for (const [pattern, replacement] of phraseRules) output = output.replace(pattern, replacement);
  for (const [pattern, replacement] of profile.toneWords) output = output.replace(pattern, replacement);
  return output;
}

function wordRewrite(sentence, intensity, sentenceIndex) {
  const profile = intensities[intensity] || intensities.balanced;
  let changed = 0;
  let examined = 0;
  const rewritten = sentence.replace(/\b[A-Za-z][A-Za-z'-]*\b/g, (word, offset) => {
    const lower = word.toLowerCase();
    if (!synonyms[lower] || stopwords.has(lower)) return word;
    examined++;
    const score = ((seededIndex(lower, sentenceIndex, offset, 1000) + 1) / 1000);
    if (score > profile.synonymRate) return word;
    const options = synonyms[lower];
    const selected = options[seededIndex(lower, sentenceIndex, offset + 19, options.length)];
    changed++;
    return preserveCase(word, selected);
  });
  return { text: rewritten, changed, examined };
}

function splitLongSentence(sentence, intensity, index) {
  const profile = intensities[intensity] || intensities.balanced;
  const words = sentence.split(/\s+/);
  if (words.length < 25) return [sentence];
  if (((index * 17 + sentence.length) % 100) / 100 > profile.splitRate) return [sentence];
  const connectors = [' because ', ' although ', ' while ', ' whereas ', ' and ', ' which '];
  for (const connector of connectors) {
    const pos = sentence.toLowerCase().indexOf(connector);
    if (pos > 35 && pos < sentence.length - 35) {
      const first = sentence.slice(0, pos).replace(/[.!?]*$/, '').trim() + '.';
      let second = sentence.slice(pos + connector.length).replace(/[.!?]*$/, '').trim();
      if (connector.trim() === 'which') second = 'This ' + second;
      else second = connector.trim()[0].toUpperCase() + connector.trim().slice(1) + ' ' + second;
      return [first, second + '.'];
    }
  }
  return [sentence];
}

function restructureSentence(sentence, index, intensity, mode) {
  const profile = intensities[intensity] || intensities.balanced;
  let s = sentence.trim();
  const ending = /[.!?]$/.test(s) ? s.slice(-1) : '.';
  s = s.replace(/[.!?]$/, '').trim();
  const chance = ((index * 37 + s.length * 13) % 100) / 100;
  if (chance > profile.restructureRate) return capitalize(s) + ending;

  const patterns = [
    { re: /^(.+?)\s+because\s+(.+)$/i, lead: 'because' },
    { re: /^(.+?)\s+since\s+(.+)$/i, lead: 'since' },
    { re: /^(.+?)\s+although\s+(.+)$/i, lead: 'although' },
    { re: /^(.+?)\s+when\s+(.+)$/i, lead: 'when' },
    { re: /^(.+?)\s+if\s+(.+)$/i, lead: 'if' }
  ];
  for (const item of patterns) {
    const match = s.match(item.re);
    if (match && match[1].length > 12 && match[2].length > 12) {
      return capitalize(`${item.lead} ${match[2].trim()}, ${match[1].trim()}`) + ending;
    }
  }

  const andMatch = s.match(/^(.{28,}?)\s+and\s+((?:it|they|this|that|these|those|users|people|companies|students|writers|researchers|the system|the tool)\b.{14,})$/i);
  if (andMatch && intensity !== 'light' && !andMatch[1].trim().endsWith(',')) {
    return capitalize(`${andMatch[1].trim()}. In addition, ${andMatch[2].trim()}`) + ending;
  }

  const commaParts = s.split(',').map(p => p.trim()).filter(Boolean);
  if (commaParts.length === 2 && commaParts[0].split(/\s+/).length > 4 && commaParts[1].split(/\s+/).length > 4) {
    return capitalize(`${commaParts[1]}, ${commaParts[0]}`) + ending;
  }

  if (/^there are\s+/i.test(s)) return capitalize(s.replace(/^there are\s+/i, 'several ')) + ending;
  if (/^there is\s+/i.test(s)) return capitalize(s.replace(/^there is\s+/i, 'one key point is ')) + ending;
  if (/^it is\s+/i.test(s)) return capitalize(s.replace(/^it is\s+/i, 'this is ')) + ending;
  if (/^the main reason is\s+/i.test(s)) return capitalize(s.replace(/^the main reason is\s+/i, 'the primary explanation is ')) + ending;

  const profileMode = modeProfiles[mode] || modeProfiles.professional;
  if (s.split(/\s+/).length > 11 && ((index + s.length) % 3 === 0)) {
    const transition = profileMode.transitions[index % profileMode.transitions.length];
    return `${transition} ${s.charAt(0).toLowerCase()}${s.slice(1)}${ending}`;
  }

  return capitalize(s) + ending;
}

function combineSentences(sentences, intensity, mode) {
  const profile = intensities[intensity] || intensities.balanced;
  if (sentences.length < 2 || profile.combineRate < 0.1) return sentences;
  const output = [];
  const profileMode = modeProfiles[mode] || modeProfiles.professional;

  for (let i = 0; i < sentences.length; i++) {
    const current = sentences[i];
    const next = sentences[i + 1];
    const currentWords = current.split(/\s+/).length;
    const nextWords = next ? next.split(/\s+/).length : 0;
    const shouldCombine = next && currentWords < 11 && nextWords < 13 && (((i + current.length) % 100) / 100) < profile.combineRate;
    if (shouldCombine) {
      const joiner = profileMode.label === 'Simple' ? 'and' : 'while';
      output.push(current.replace(/[.!?]$/, ` ${joiner} `) + next.charAt(0).toLowerCase() + next.slice(1));
      i++;
    } else {
      output.push(current);
    }
  }
  return output;
}

function sentencePolish(sentence) {
  return sentence
    .replace(/\s+/g, ' ')
    .replace(/\s+([,.!?;:])/g, '$1')
    .replace(/,\s*,/g, ',')
    .replace(/,\s*\./g, '.')
    .replace(/\.\s*\./g, '.')
    .replace(/\b(the the|and and|to to|of of|is is|can can)\b/gi, m => m.split(' ')[0])
    .replace(/\bi\b/g, 'I')
    .trim();
}

function paragraphize(sentences) {
  if (sentences.length <= 4) return sentences.join(' ');
  const paragraphs = [];
  for (let i = 0; i < sentences.length; i += 4) paragraphs.push(sentences.slice(i, i + 4).join(' '));
  return paragraphs.join('\n\n');
}

function words(text) {
  return normalizeInput(text).toLowerCase().match(/\b[a-z0-9]+\b/g) || [];
}

function unique(arr) { return [...new Set(arr)]; }

function ngrams(tokens, n) {
  const grams = [];
  for (let i = 0; i <= tokens.length - n; i++) grams.push(tokens.slice(i, i + n).join(' '));
  return grams;
}

function jaccard(a, b) {
  const A = new Set(a);
  const B = new Set(b);
  if (!A.size && !B.size) return 1;
  let intersection = 0;
  for (const x of A) if (B.has(x)) intersection++;
  const union = A.size + B.size - intersection;
  return union ? intersection / union : 0;
}

function levenshteinSimilarity(a, b) {
  a = normalizeInput(a).toLowerCase();
  b = normalizeInput(b).toLowerCase();
  if (!a && !b) return 1;
  const max = Math.max(a.length, b.length);
  if (!max) return 1;
  const prev = new Array(b.length + 1).fill(0).map((_, i) => i);
  const curr = new Array(b.length + 1).fill(0);
  for (let i = 1; i <= a.length; i++) {
    curr[0] = i;
    for (let j = 1; j <= b.length; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      curr[j] = Math.min(prev[j] + 1, curr[j - 1] + 1, prev[j - 1] + cost);
    }
    for (let j = 0; j <= b.length; j++) prev[j] = curr[j];
  }
  return 1 - prev[b.length] / max;
}

function readabilityScore(text) {
  const ws = words(text).length || 1;
  const sentenceCount = splitSentences(text).length || 1;
  const avg = ws / sentenceCount;
  let score = 100;
  if (avg > 30) score -= 32;
  else if (avg > 24) score -= 20;
  else if (avg > 18) score -= 8;
  else if (avg < 6) score -= 8;
  const longWords = (text.toLowerCase().match(/\b[a-z]{10,}\b/g) || []).length;
  score -= Math.min(24, Math.round((longWords / ws) * 100));
  return Math.max(42, Math.min(99, score));
}

function metrics(original, rewritten) {
  const ow = words(original);
  const rw = words(rewritten);
  const meaningfulO = ow.filter(w => !stopwords.has(w));
  const meaningfulR = rw.filter(w => !stopwords.has(w));
  const wordOverlap = jaccard(unique(meaningfulO), unique(meaningfulR));
  const bigramOverlap = jaccard(unique(ngrams(ow, 2)), unique(ngrams(rw, 2)));
  const trigramOverlap = jaccard(unique(ngrams(ow, 3)), unique(ngrams(rw, 3)));
  const charSimilarity = levenshteinSimilarity(original, rewritten);
  const weightedSimilarity = Math.max(0, Math.min(1, (wordOverlap * 0.32) + (bigramOverlap * 0.28) + (trigramOverlap * 0.26) + (charSimilarity * 0.14)));
  const estimatedRisk = Math.round(weightedSimilarity * 100);
  return {
    originalWords: ow.length,
    rewrittenWords: rw.length,
    wordOverlap: Math.round(wordOverlap * 100),
    phraseOverlap: Math.round(((bigramOverlap + trigramOverlap) / 2) * 100),
    charSimilarity: Math.round(charSimilarity * 100),
    estimatedSimilarity: estimatedRisk,
    originalityLift: Math.max(0, 100 - estimatedRisk),
    changedWords: Math.max(0, ow.length - Math.round(ow.length * wordOverlap)),
    readability: readabilityScore(rewritten)
  };
}

function makeTips(stats, intensity) {
  const tips = [];
  if (stats.estimatedSimilarity > 55) tips.push('Similarity is still high. Use Maximum mode and manually add your own examples, explanation, or source citation.');
  if (stats.phraseOverlap > 35) tips.push('Phrase overlap is noticeable. Restructure long sentences instead of changing only words.');
  if (stats.readability < 70) tips.push('Readability can be improved by splitting long sentences.');
  if (intensity === 'maximum') tips.push('Maximum mode changes more wording. Review meaning carefully before publishing.');
  if (!tips.length) tips.push('Good rewrite strength. Still verify facts and add citations where sources were used.');
  return tips;
}

export function rewriteText(input, options = {}) {
  const mode = options.mode || 'professional';
  const intensity = options.intensity || 'balanced';
  const ethicalNotice = options.ethicalNotice !== false;
  const text = normalizeInput(input);
  if (!text) {
    return { rewritten: '', stats: metrics('', ''), tips: ['Paste text first.'], notice: 'No input received.' };
  }
  if (words(text).length < 8) {
    return { rewritten: text, stats: metrics(text, text), tips: ['Add more text for a meaningful rewrite.'], notice: 'Very short text cannot be rewritten deeply without changing meaning.' };
  }

  const profile = modeProfiles[mode] || modeProfiles.professional;
  let changedWords = 0;
  let examinedWords = 0;
  let interim = [];

  splitSentences(text).forEach((sentence, index) => {
    let s = applyPhraseRules(sentence, profile);
    const wordResult = wordRewrite(s, intensity, index);
    changedWords += wordResult.changed;
    examinedWords += wordResult.examined;
    s = restructureSentence(wordResult.text, index, intensity, mode);
    splitLongSentence(s, intensity, index).forEach(part => interim.push(sentencePolish(part)));
  });

  interim = combineSentences(interim, intensity, mode).map(sentencePolish);
  let rewritten = paragraphize(interim);

  if ((intensities[intensity] || intensities.balanced).transitionRate > 0.3 && interim.length >= 3) {
    const closing = mode === 'academic'
      ? 'Overall, the revised version presents the same core idea with a more independent structure and clearer expression.'
      : mode === 'simple'
        ? 'Overall, the idea is now written in a clearer and more original way.'
        : mode === 'human'
          ? 'Overall, the message now sounds more natural while keeping the main meaning intact.'
          : 'Overall, the content now has a stronger structure, improved wording, and lower direct textual overlap.';
    if (!/overall,/i.test(rewritten) && rewritten.split(/\s+/).length > 45) rewritten += `\n\n${closing}`;
  }

  rewritten = sentencePolish(rewritten).replace(/\n\s+/g, '\n');
  const stats = metrics(text, rewritten);
  stats.replacedWords = changedWords;
  stats.examinedRewriteWords = examinedWords;

  return {
    rewritten,
    stats,
    tips: makeTips(stats, intensity),
    notice: ethicalNotice ? 'This tool estimates text overlap only. It does not check the internet or guarantee plagiarism removal. Use citations for borrowed ideas.' : ''
  };
}

export function compareTexts(original, rewritten) {
  return metrics(original, rewritten);
}
