import re
import math
import random
from collections import Counter, defaultdict
from datetime import datetime

STOPWORDS = set('''a an the and or but if while with without of to in for on at by from into onto over under between among about as is are was were be been being am i you he she it we they them this that these those there here not no do does did done can could should would may might must will shall very really just more most much many some any each every all other another such than then so because since although though however therefore thus also only own same too'''.split())

SYNONYMS = {
    'use': ['apply', 'employ', 'make use of'], 'uses': ['applies', 'employs'], 'using': ['applying', 'employing'], 'used': ['applied', 'employed'],
    'make': ['create', 'produce', 'build', 'develop'], 'makes': ['creates', 'produces', 'builds'], 'made': ['created', 'produced', 'developed'],
    'help': ['support', 'assist', 'guide'], 'helps': ['supports', 'assists', 'guides'], 'helping': ['supporting', 'assisting'],
    'improve': ['enhance', 'refine', 'strengthen'], 'improves': ['enhances', 'refines'], 'improved': ['enhanced', 'refined'],
    'best': ['high-quality', 'strong', 'effective'], 'good': ['strong', 'clear', 'effective'], 'bad': ['weak', 'poor', 'unclear'],
    'important': ['essential', 'valuable', 'meaningful'], 'main': ['primary', 'core', 'central'], 'big': ['major', 'large', 'significant'],
    'small': ['compact', 'minor', 'limited'], 'easy': ['simple', 'straightforward'], 'difficult': ['challenging', 'complex'],
    'text': ['content', 'writing', 'copy'], 'content': ['material', 'writing', 'copy'], 'article': ['write-up', 'piece', 'post'],
    'website': ['platform', 'site', 'web app'], 'tool': ['utility', 'feature', 'module'], 'tools': ['utilities', 'features', 'modules'],
    'function': ['feature', 'capability', 'operation'], 'features': ['capabilities', 'functions', 'tools'],
    'proper': ['well-structured', 'polished', 'complete'], 'professional': ['business-ready', 'polished', 'expert-level'],
    'beautiful': ['clean', 'attractive', 'refined'], 'amazing': ['impressive', 'powerful', 'high-impact'],
    'quality': ['standard', 'finish', 'caliber'], 'high': ['strong', 'premium', 'advanced'],
    'write': ['compose', 'draft', 'prepare'], 'writing': ['composition', 'drafting', 'content creation'],
    'rewrite': ['rephrase', 'rework', 'reshape'], 'rewriting': ['rephrasing', 'reworking'], 'remove': ['reduce', 'clean', 'replace'],
    'plagiarism': ['text overlap', 'copied wording', 'source similarity'], 'similar': ['alike', 'close', 'matching'], 'same': ['identical', 'unchanged', 'matching'],
    'create': ['build', 'generate', 'prepare'], 'creating': ['building', 'generating', 'preparing'], 'generate': ['create', 'produce', 'draft'],
    'idea': ['concept', 'angle', 'direction'], 'ideas': ['concepts', 'angles', 'directions'],
    'method': ['approach', 'process', 'technique'], 'methods': ['approaches', 'techniques'],
    'fast': ['quick', 'rapid'], 'slow': ['gradual', 'delayed'], 'new': ['fresh', 'updated', 'modern'],
    'old': ['outdated', 'previous', 'earlier'], 'modern': ['current', 'contemporary', 'up-to-date'],
    'start': ['begin', 'launch'], 'end': ['finish', 'complete'], 'final': ['complete', 'finished', 'ready'],
    'work': ['operate', 'function', 'perform'], 'works': ['operates', 'functions', 'performs'], 'working': ['operating', 'functioning'],
    'need': ['require', 'want', 'expect'], 'needs': ['requires', 'expects'], 'provide': ['offer', 'deliver', 'supply'],
    'add': ['include', 'insert', 'attach'], 'added': ['included', 'inserted'], 'convert': ['transform', 'turn', 'change'],
    'change': ['adjust', 'modify', 'revise'], 'fix': ['correct', 'repair', 'resolve'], 'check': ['review', 'inspect', 'analyze'],
    'analysis': ['review', 'evaluation', 'assessment'], 'analyze': ['evaluate', 'review', 'inspect'],
    'student': ['learner', 'academic user'], 'business': ['company', 'commercial'], 'client': ['customer', 'buyer'],
    'customer': ['buyer', 'user', 'client'], 'sell': ['market', 'offer', 'monetize'], 'selling': ['marketing', 'offering'],
    'product': ['item', 'offer', 'solution'], 'products': ['items', 'offers', 'solutions'],
    'description': ['summary', 'overview', 'copy'], 'title': ['headline', 'name', 'caption'],
    'perfect': ['polished', 'well-finished', 'highly refined'], 'strong': ['powerful', 'effective', 'robust'],
    'clear': ['understandable', 'direct', 'well-defined'], 'simple': ['easy-to-read', 'straightforward', 'plain'],
    'complex': ['advanced', 'detailed', 'multi-layered'], 'detailed': ['in-depth', 'thorough', 'complete'],
    'real': ['practical', 'authentic', 'usable'], 'fake': ['unreliable', 'artificial', 'unsupported'],
    'increase': ['raise', 'boost', 'grow'], 'decrease': ['reduce', 'lower', 'cut'], 'reduce': ['lower', 'minimize', 'decrease'],
    'support': ['assist', 'back', 'help'], 'platform': ['workspace', 'system', 'web app'], 'dashboard': ['workspace', 'control panel'],
    'copy': ['duplicate', 'replicate', 'text'], 'copied': ['duplicated', 'repeated', 'matched'], 'upload': ['import', 'add'],
    'download': ['export', 'save'], 'format': ['structure', 'layout'], 'formatting': ['structure', 'layout'],
    'grammar': ['language accuracy', 'sentence quality'], 'punctuation': ['sentence marks', 'writing marks'],
    'properly': ['correctly', 'smoothly', 'accurately'], 'able': ['capable', 'ready'], 'option': ['choice', 'setting'],
    'different': ['varied', 'distinct', 'alternative'], 'multiple': ['several', 'many'], 'possible': ['available', 'workable'],
    'viral': ['attention-grabbing', 'shareable', 'high-impact'], 'hook': ['opening line', 'attention grabber'],
    'summary': ['short version', 'brief overview'], 'summarize': ['condense', 'shorten', 'briefly explain'],
    'long': ['extended', 'lengthy'], 'short': ['brief', 'compact'], 'read': ['review', 'go through'], 'reader': ['audience', 'viewer'],
    'audience': ['readers', 'viewers', 'target users'], 'topic': ['subject', 'theme'], 'keywords': ['search terms', 'key phrases'],
    'focus': ['emphasize', 'center on'], 'focuses': ['emphasizes', 'centers on'], 'safe': ['secure', 'careful', 'reliable'],
    'dangerous': ['risky', 'unsafe'], 'bias': ['unbalanced wording', 'loaded language'], 'clean': ['polish', 'refine', 'organize'],
    'cleaner': ['polisher', 'refiner'], 'smart': ['intelligent', 'advanced', 'well-designed'], 'advanced': ['high-level', 'powerful'],
    'basic': ['simple', 'entry-level'], 'premium': ['high-end', 'professional-grade'], 'industry': ['professional', 'commercial'],
    'level': ['standard', 'quality'], 'engine': ['system', 'processor'], 'backend': ['server-side logic', 'application core'],
    'frontend': ['user interface', 'client-side interface'], 'user': ['visitor', 'customer', 'member'], 'login': ['sign in'],
    'signup': ['create an account'], 'account': ['profile', 'user account'], 'history': ['past work', 'saved activity'],
}

PHRASE_REPLACEMENTS = [
    (r'\bin today\'s (?:world|digital world)\b', 'currently'),
    (r'\bit is important to note that\b', 'notably'),
    (r'\bin conclusion\b', 'to conclude'),
    (r'\bmoreover\b', 'also'),
    (r'\bfurthermore\b', 'in addition'),
    (r'\bleverage\b', 'use'),
    (r'\butilize\b', 'use'),
    (r'\bdelve into\b', 'explore'),
    (r'\bcutting-edge\b', 'modern'),
    (r'\bseamlessly\b', 'smoothly'),
    (r'\brobust\b', 'reliable'),
    (r'\bcomprehensive\b', 'complete'),
    (r'\bgame-changer\b', 'valuable improvement'),
    (r'\bunlock the power of\b', 'use'),
    (r'\bdesigned to\b', 'built to'),
    (r'\bthis article will\b', 'this guide will'),
    (r'\bwhen it comes to\b', 'for'),
    (r'\bdue to the fact that\b', 'because'),
    (r'\bin order to\b', 'to'),
    (r'\bat the end of the day\b', 'ultimately'),
]

BIAS_MAP = {
    r'\bmanpower\b': 'workforce', r'\bchairman\b': 'chairperson', r'\bguys\b': 'team',
    r'\bcrazy\b': 'unusual', r'\binsane\b': 'extreme', r'\blame\b': 'ineffective',
    r'\bnormal people\b': 'many people', r'\bold people\b': 'older adults', r'\bthe elderly\b': 'older adults',
    r'\bhandicapped\b': 'disabled', r'\bblind to\b': 'unaware of', r'\bdeaf to\b': 'unresponsive to',
}

POWER_WORDS = ['practical', 'clear', 'focused', 'useful', 'effective', 'trusted', 'ready-to-use', 'structured', 'modern', 'reliable']
TRANSITIONS = ['Additionally', 'As a result', 'For practical use', 'In many cases', 'From a user perspective', 'For better clarity']
EMOTIONS = {
    'positive': {'good','great','best','love','excellent','amazing','happy','success','win','beautiful','benefit','strong','useful','easy','fast'},
    'negative': {'bad','poor','hate','sad','angry','problem','issue','fail','wrong','difficult','hard','risk','weak','loss','slow'},
    'urgent': {'now','today','limited','urgent','quick','fast','soon','immediately','deadline','important'},
    'trust': {'safe','secure','trusted','reliable','verified','proof','guarantee','quality','professional'}
}

TOOL_CATEGORIES = {
    'Smart Writing': ['humanizer','paragraph_rewriter','deep_rewriter','ai_style_cleaner','sentence_shortener','sentence_expander','tone_converter','professional_rewriter','simple_rewriter','active_voice','grammar_polish','clarity_enhancer','transition_adder','sentence_variety_improver'],
    'Content Intelligence': ['readability_analyzer','quality_score','repetition_detector','overused_words','weak_word_detector','sentence_variety_score','passive_voice_detector','tone_analysis','sentiment_analysis','keyword_extractor','content_brief','originality_risk_report','compare_similarity','ai_style_checker'],
    'SEO & Blogging': ['blog_outline','blog_intro','blog_post_builder','content_calendar','seo_brief','meta_title','meta_description','slug_generator','keyword_density','faq_builder','schema_faq_json','heading_optimizer','snippet_generator','search_intent'],
    'Student Tools': ['study_notes','important_points','mcq_generator','flashcards','definition_extractor','glossary_builder','thesis_statement','discussion_post','lesson_plan','essay_outline','citation_formatter','assignment_formatter','research_summary','quiz_generator'],
    'Business Tools': ['email_writer','cold_email','proposal_writer','meeting_notes','meeting_agenda','customer_reply','resume_bullets','cover_letter','linkedin_bio','job_description','client_brief','swot_analysis','product_description','invoice_note','terms_draft'],
    'Social Media': ['viral_hooks','youtube_script','short_video_script','youtube_titles','youtube_description','tiktok_hooks','instagram_caption','linkedin_post','facebook_ad','twitter_thread','cta_generator','hashtag_generator','carousel_outline','social_calendar'],
    'Document Tools': ['clean_formatting','markdown_converter','case_formatter','bullet_generator','outline_builder','executive_summary','pros_cons_list','timeline_extractor','title_generator','prompt_writer','prompt_improver','text_table','extract_action_items','content_repurposer'],
}

TOOL_INFO = {
    'humanizer': ('AI Humanizer', 'Rewrite robotic text into a more natural, human-style draft.'),
    'paragraph_rewriter': ('Paragraph Rewriter', 'Rewrite paragraphs with changed wording and structure.'),
    'deep_rewriter': ('Deep Rewriter', 'Aggressively restructures wording and sentence flow for a fresher draft.'),
    'ai_style_cleaner': ('AI-Style Cleaner', 'Reduce robotic phrases, repeated transitions, and generic wording.'),
    'transition_adder': ('Transition Improver', 'Add smoother transitions between ideas.'),
    'sentence_variety_improver': ('Sentence Variety Improver', 'Rewrite text with more varied sentence rhythm.'),
    'weak_word_detector': ('Weak Word Detector', 'Find vague, weak, or filler words.'),
    'sentence_variety_score': ('Sentence Variety Score', 'Analyze sentence length variation and rhythm.'),
    'content_brief': ('Content Brief Builder', 'Create a brief with audience, angle, keywords, and structure.'),
    'originality_risk_report': ('Originality Risk Report', 'Estimate repeated wording and high-overlap risk using local text analysis.'),
    'blog_post_builder': ('Blog Post Builder', 'Create a structured blog draft from a topic or notes.'),
    'content_calendar': ('Content Calendar', 'Generate a practical 7-day content plan.'),
    'seo_brief': ('SEO Content Brief', 'Generate SEO angle, headings, FAQs, and keyword suggestions.'),
    'schema_faq_json': ('FAQ Schema JSON', 'Create simple FAQ schema markup from your content.'),
    'glossary_builder': ('Glossary Builder', 'Extract terms and create simple explanations.'),
    'thesis_statement': ('Thesis Statement Generator', 'Create academic thesis statement options.'),
    'discussion_post': ('Discussion Post Writer', 'Create a student-style discussion forum post.'),
    'lesson_plan': ('Lesson Plan Builder', 'Create lesson objectives, activities, and assessment ideas.'),
    'cold_email': ('Cold Email Writer', 'Create a polite sales or outreach email.'),
    'meeting_agenda': ('Meeting Agenda Builder', 'Turn a topic into a clean meeting agenda.'),
    'job_description': ('Job Description Writer', 'Create a structured job post.'),
    'client_brief': ('Client Brief Builder', 'Create a concise client/project brief.'),
    'swot_analysis': ('SWOT Analysis', 'Create strengths, weaknesses, opportunities, and threats.'),
    'short_video_script': ('Short Video Script', 'Create a 30-60 second script for Reels, Shorts, or TikTok.'),
    'linkedin_post': ('LinkedIn Post Writer', 'Create a professional LinkedIn post.'),
    'facebook_ad': ('Facebook Ad Copy', 'Generate headline, primary text, and CTA.'),
    'social_calendar': ('Social Media Calendar', 'Generate a 7-day social posting plan.'),
    'executive_summary': ('Executive Summary', 'Create a concise executive summary.'),
    'pros_cons_list': ('Pros & Cons Generator', 'Create a balanced pros and cons list.'),
    'timeline_extractor': ('Timeline Extractor', 'Extract dates, steps, and milestones when available.'),
    'content_repurposer': ('Content Repurposer', 'Turn one text into posts, email, bullets, and summary.'),

    'sentence_shortener': ('Sentence Shortener', 'Make long writing concise.'),
    'sentence_expander': ('Sentence Expander', 'Add useful context and detail.'),
    'tone_converter': ('Tone Converter', 'Convert text into professional, friendly, academic, or persuasive tone.'),
    'professional_rewriter': ('Professional Rewriter', 'Make text polished and business-ready.'),
    'simple_rewriter': ('Simple Rewriter', 'Make difficult text easy to understand.'),
    'active_voice': ('Active Voice Converter', 'Reduce passive wording where possible.'),
    'grammar_polish': ('Grammar & Punctuation Polish', 'Clean spacing, capitalization, and sentence punctuation.'),
    'clarity_enhancer': ('Clarity Enhancer', 'Improve flow, remove clutter, and strengthen wording.'),
    'readability_analyzer': ('Readability Analyzer', 'Check reading level and writing stats.'),
    'quality_score': ('Writing Quality Score', 'Estimate clarity, structure, repetition, and readability.'),
    'repetition_detector': ('Repetition Detector', 'Find repeated words and phrases.'),
    'overused_words': ('Overused Word Detector', 'Find weak or repeated filler words.'),
    'passive_voice_detector': ('Passive Voice Detector', 'Find possible passive voice sentences.'),
    'tone_analysis': ('Tone Analysis', 'Analyze professional, emotional, urgent, and trust signals.'),
    'sentiment_analysis': ('Sentiment Analysis', 'Estimate positive/negative/neutral tone.'),
    'keyword_extractor': ('Keyword Extractor', 'Extract important words and phrases.'),
    'compare_similarity': ('Similarity Checker', 'Compare the input and output text overlap.'),
    'ai_style_checker': ('AI-Style Pattern Checker', 'Flag robotic phrases and overused AI-style wording.'),
    'blog_outline': ('Blog Outline Generator', 'Create a structured article outline.'),
    'blog_intro': ('Blog Intro Generator', 'Create a strong introduction.'),
    'meta_title': ('SEO Meta Title', 'Generate SEO-friendly title ideas.'),
    'meta_description': ('SEO Meta Description', 'Generate meta descriptions.'),
    'slug_generator': ('URL Slug Generator', 'Create clean SEO slugs.'),
    'keyword_density': ('Keyword Density Checker', 'Calculate keyword frequency.'),
    'faq_builder': ('FAQ Builder', 'Generate questions and answers from content.'),
    'heading_optimizer': ('Heading Optimizer', 'Generate improved headings.'),
    'snippet_generator': ('Featured Snippet Writer', 'Create concise answer snippets.'),
    'search_intent': ('Search Intent Classifier', 'Classify informational, commercial, transactional, or navigational intent.'),
    'study_notes': ('Study Notes Generator', 'Turn text into clean study notes.'),
    'important_points': ('Important Points Extractor', 'Extract key points.'),
    'mcq_generator': ('MCQ Generator', 'Create multiple-choice questions.'),
    'flashcards': ('Flashcard Creator', 'Create question-answer flashcards.'),
    'definition_extractor': ('Definition Extractor', 'Extract terms and definitions.'),
    'essay_outline': ('Essay Outline Builder', 'Create academic essay structure.'),
    'citation_formatter': ('Citation Formatter', 'Format simple APA/MLA/Harvard-style references from provided details.'),
    'assignment_formatter': ('Assignment Formatter', 'Format content into assignment structure.'),
    'research_summary': ('Research Summary', 'Summarize research-style content.'),
    'quiz_generator': ('Quiz Generator', 'Create short answer questions.'),
    'email_writer': ('Email Writer', 'Draft a professional email.'),
    'proposal_writer': ('Proposal Writer', 'Create a business/freelance proposal.'),
    'meeting_notes': ('Meeting Notes Formatter', 'Turn messy notes into meeting minutes.'),
    'customer_reply': ('Customer Support Reply', 'Create a polite support response.'),
    'resume_bullets': ('Resume Bullet Improver', 'Create achievement-focused resume bullets.'),
    'cover_letter': ('Cover Letter Builder', 'Draft a cover letter.'),
    'linkedin_bio': ('LinkedIn Bio Generator', 'Create a professional profile summary.'),
    'product_description': ('Product Description Rewriter', 'Create clean e-commerce product copy.'),
    'invoice_note': ('Invoice Note Writer', 'Create professional invoice/payment notes.'),
    'terms_draft': ('Terms / Policy Draft Helper', 'Draft simple website policy text.'),
    'viral_hooks': ('Viral Hook Generator', 'Generate attention-grabbing openings.'),
    'youtube_script': ('YouTube Script Writer', 'Generate structured video script.'),
    'youtube_titles': ('YouTube Title Generator', 'Generate title ideas.'),
    'youtube_description': ('YouTube Description Writer', 'Generate a clean video description.'),
    'tiktok_hooks': ('TikTok Hook Writer', 'Generate short hooks.'),
    'instagram_caption': ('Instagram Caption Generator', 'Generate caption ideas.'),
    'twitter_thread': ('X/Twitter Thread Writer', 'Create a thread outline.'),
    'cta_generator': ('CTA Generator', 'Generate calls-to-action.'),
    'hashtag_generator': ('Hashtag Generator', 'Generate hashtags.'),
    'carousel_outline': ('Carousel Post Outline', 'Create slide-by-slide carousel text.'),
    'clean_formatting': ('Clean Formatting', 'Remove messy spacing and improve layout.'),
    'markdown_converter': ('Markdown Converter', 'Convert text into clean Markdown.'),
    'case_formatter': ('Case Formatter', 'Convert to title, sentence, upper, or lower case.'),
    'bullet_generator': ('Bullet Point Generator', 'Turn text into bullets.'),
    'outline_builder': ('Outline Builder', 'Create a structured outline.'),
    'title_generator': ('Title Generator', 'Generate polished titles.'),
    'prompt_writer': ('Prompt Writer', 'Create a detailed prompt.'),
    'prompt_improver': ('Prompt Improver', 'Improve an existing prompt.'),
    'text_table': ('Text to Table', 'Convert lines into a simple Markdown table.'),
    'extract_action_items': ('Action Items Extractor', 'Extract tasks, owners, and deadlines when present.'),
}

def clean_spaces(text: str) -> str:
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\s+([,.;:!?])', r'\1', text)
    text = re.sub(r'([,.;:!?])([^\s\n])', r'\1 \2', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def sentence_split(text: str):
    text = clean_spaces(text)
    if not text:
        return []
    parts = re.split(r'(?<=[.!?])\s+|\n+', text)
    return [p.strip() for p in parts if p.strip()]

def words(text: str):
    return re.findall(r"[A-Za-z][A-Za-z'\-]*", text.lower())

def syllable_count(word):
    word = word.lower().strip()
    if not word:
        return 0
    groups = re.findall(r'[aeiouy]+', word)
    count = len(groups)
    if word.endswith('e') and count > 1:
        count -= 1
    return max(1, count)

def readability_score(text: str):
    sents = sentence_split(text)
    ws = words(text)
    if not ws or not sents:
        return 0
    syllables = sum(syllable_count(w) for w in ws)
    score = 206.835 - 1.015 * (len(ws)/max(1,len(sents))) - 84.6 * (syllables/max(1,len(ws)))
    return round(max(0, min(100, score)), 1)

def tokenize_set(text):
    return {w for w in words(text) if w not in STOPWORDS and len(w) > 2}

def jaccard_similarity(a, b):
    sa, sb = tokenize_set(a), tokenize_set(b)
    if not sa and not sb:
        return 0
    return round(100 * len(sa & sb) / max(1, len(sa | sb)), 1)

def ngrams(tokens, n=3):
    return set(tuple(tokens[i:i+n]) for i in range(max(0, len(tokens)-n+1)))

def phrase_overlap(a, b, n=3):
    wa = [w for w in words(a) if len(w) > 2]
    wb = [w for w in words(b) if len(w) > 2]
    ga, gb = ngrams(wa, n), ngrams(wb, n)
    if not ga or not gb:
        return 0
    return round(100 * len(ga & gb) / max(1, len(ga)), 1)

def metrics(original, output):
    ws = words(output)
    sents = sentence_split(output)
    sim = jaccard_similarity(original, output) if original and output else 0
    phr = phrase_overlap(original, output) if original and output else 0
    return {
        'words': len(ws),
        'characters': len(output),
        'sentences': len(sents),
        'reading_time': max(1, math.ceil(len(ws) / 220)) if ws else 0,
        'readability': readability_score(output),
        'similarity': sim,
        'phrase_overlap': phr,
        'originality_lift': round(max(0, 100 - sim), 1),
    }

def apply_phrase_replacements(text):
    out = text
    for pat, repl in PHRASE_REPLACEMENTS:
        out = re.sub(pat, repl, out, flags=re.I)
    return out

def preserve_case(src, repl):
    if src.isupper():
        return repl.upper()
    if src[:1].isupper():
        return repl[:1].upper() + repl[1:]
    return repl

def synonymize_text(text, strength='balanced'):
    rate = {'light': 0.25, 'balanced': 0.45, 'strong': 0.68, 'maximum': 0.90}.get(strength, 0.45)
    def repl(m):
        token = m.group(0)
        low = token.lower()
        if low in SYNONYMS and random.random() < rate:
            return preserve_case(token, random.choice(SYNONYMS[low]))
        return token
    return re.sub(r"\b[A-Za-z][A-Za-z'\-]*\b", repl, text)

def restructure_sentence(s, mode='professional', strength='balanced'):
    original = s.strip()
    s = apply_phrase_replacements(original)
    s = synonymize_text(s, strength)
    s = clean_spaces(s)
    # Split and reorder long clauses gently.
    if strength in ('strong','maximum') and len(words(s)) > 14:
        clauses = [c.strip() for c in re.split(r',\s+|;\s+|\s+and\s+', s) if c.strip()]
        if len(clauses) >= 2:
            lead = random.choice(['For a clearer result', 'In practical terms', 'For readers', 'From a professional angle'])
            s = f"{lead}, {clauses[-1].rstrip('.')} while {clauses[0][0].lower()+clauses[0][1:]}"
            if len(clauses) > 2:
                s += ', with ' + ', '.join(clauses[1:-1])
    # Pattern changes.
    patterns = [
        (r'^(.*?)\s+is\s+a\s+(.*?)\s+that\s+(.*)$', r'\1 works as \2 and \3'),
        (r'^(.*?)\s+helps\s+(.*?)\s+to\s+(.*)$', r'With \1, \2 can \3'),
        (r'^(.*?)\s+provides\s+(.*?)\s+for\s+(.*)$', r'For \3, \1 offers \2'),
        (r'^(.*?)\s+includes\s+(.*?)$', r'\1 comes with \2'),
    ]
    if strength in ('balanced','strong','maximum'):
        for pat, rep in patterns:
            new = re.sub(pat, rep, s, flags=re.I)
            if new != s:
                s = new
                break
    if mode in ('professional','business'):
        s = re.sub(r'\bI think\b', 'It is worth noting', s, flags=re.I)
        s = re.sub(r'\bvery\b', 'highly', s, flags=re.I)
    elif mode == 'simple':
        s = re.sub(r'\btherefore\b', 'so', s, flags=re.I)
        s = re.sub(r'\butilize\b', 'use', s, flags=re.I)
    elif mode == 'academic':
        s = re.sub(r'\bshows\b', 'indicates', s, flags=re.I)
        s = re.sub(r'\bproves\b', 'suggests', s, flags=re.I)
    return capitalize_sentence(clean_spaces(s))

def capitalize_sentence(s):
    s = s.strip()
    if not s:
        return s
    s = s[0].upper() + s[1:]
    if not re.search(r'[.!?]$', s):
        s += '.'
    return s

def rewrite_text(text, mode='professional', strength='strong'):
    sents = sentence_split(text)
    if not sents:
        return ''
    out = []
    for idx, s in enumerate(sents):
        rewritten = restructure_sentence(s, mode=mode, strength=strength)
        # If still very similar, add a second local pass.
        if jaccard_similarity(s, rewritten) > 72 and strength in ('strong','maximum'):
            rewritten = restructure_sentence(rewritten, mode=mode, strength='maximum')
        out.append(rewritten)
    result = ' '.join(out)
    if strength == 'maximum' and len(out) > 1:
        result = add_transitions(result)
    return grammar_polish(result)

def add_transitions(text):
    sents = sentence_split(text)
    out = []
    for i, s in enumerate(sents):
        if i and i % 2 == 0 and not re.match(r'^(Additionally|As a result|For practical use|In many cases)', s):
            s = random.choice(TRANSITIONS) + ', ' + s[0].lower() + s[1:]
        out.append(s)
    return ' '.join(out)

def grammar_polish(text):
    text = clean_spaces(text)
    if not text:
        return ''
    # Capitalize after sentence boundary.
    def cap(m):
        return m.group(1) + m.group(2).upper()
    text = re.sub(r'(^|[.!?]\s+)([a-z])', cap, text)
    text = re.sub(r'\bi\b', 'I', text)
    text = re.sub(r'\s+', ' ', text)
    # Ensure sentences end correctly.
    sents = sentence_split(text)
    return ' '.join(capitalize_sentence(s) for s in sents)

def simplify_text(text):
    mapping = {
        'approximately':'about','assistance':'help','commence':'start','terminate':'end','purchase':'buy','numerous':'many',
        'demonstrate':'show','individuals':'people','facilitate':'help','subsequently':'later','sufficient':'enough',
        'additional':'more','objective':'goal','requirement':'need','utilize':'use','implement':'use','obtain':'get'
    }
    out = text
    for k, v in mapping.items():
        out = re.sub(r'\b'+re.escape(k)+r'\b', v, out, flags=re.I)
    return grammar_polish(out)

def shorten_text(text):
    sents = sentence_split(text)
    shortened = []
    for s in sents:
        s = re.sub(r'\b(in order to|due to the fact that|it is important to note that|as a matter of fact)\b', '', s, flags=re.I)
        s = re.sub(r'\bvery|really|actually|basically|simply|just\b', '', s, flags=re.I)
        shortened.append(grammar_polish(s))
    return ' '.join(shortened)

def expand_text(text):
    sents = sentence_split(text)
    out = []
    for s in sents:
        out.append(s)
        key = extract_keywords(s, limit=2)
        if key:
            out.append(f"This matters because {', '.join(key)} can improve clarity, user understanding, and practical value.")
    return grammar_polish(' '.join(out))

def active_voice(text):
    sents = sentence_split(text)
    out = []
    for s in sents:
        ns = re.sub(r'\bwas\s+(\w+ed)\s+by\s+(.+)', r'\2 \1', s, flags=re.I)
        ns = re.sub(r'\bwere\s+(\w+ed)\s+by\s+(.+)', r'\2 \1', ns, flags=re.I)
        ns = re.sub(r'\bis\s+being\s+(\w+ed)\b', r'gets \1', ns, flags=re.I)
        out.append(capitalize_sentence(ns))
    return ' '.join(out)

def bias_cleaner(text):
    out = text
    for pat, repl in BIAS_MAP.items():
        out = re.sub(pat, repl, out, flags=re.I)
    return grammar_polish(out)

def extract_keywords(text, limit=12):
    freq = Counter(w for w in words(text) if w not in STOPWORDS and len(w) > 3)
    return [w for w, c in freq.most_common(limit)]

def top_phrases(text, n=2, limit=8):
    toks = [w for w in words(text) if w not in STOPWORDS and len(w) > 3]
    grams = Counter(' '.join(toks[i:i+n]) for i in range(max(0,len(toks)-n+1)))
    return [g for g, c in grams.most_common(limit)]

def summarize(text, ratio=0.35, max_sentences=5):
    sents = sentence_split(text)
    if len(sents) <= 2:
        return text
    freq = Counter(w for w in words(text) if w not in STOPWORDS)
    scores = []
    for i, s in enumerate(sents):
        score = sum(freq.get(w,0) for w in words(s)) / max(1, len(words(s)))
        if i == 0: score += 0.5
        scores.append((score, i, s))
    keep = max(1, min(max_sentences, math.ceil(len(sents) * ratio)))
    chosen = sorted(scores, reverse=True)[:keep]
    return ' '.join(s for _, i, s in sorted(chosen, key=lambda x: x[1]))

def bullet_points(text):
    sents = sentence_split(text)
    if not sents:
        return ''
    return '\n'.join('- ' + shorten_text(s).rstrip('.') for s in sents)

def outline(text):
    keys = extract_keywords(text, 6) or ['Introduction','Main Idea','Details','Conclusion']
    lines = ['# Outline', '', '## 1. Introduction', '- Define the topic and explain why it matters.']
    for i, k in enumerate(keys[:5], start=2):
        lines += [f'\n## {i}. {k.title()}', f'- Explain the role of {k}.', f'- Add examples, evidence, or practical steps.']
    lines += ['\n## Final Section', '- Summarize the main points and give a clear next step.']
    return '\n'.join(lines)

def title_case(s):
    minor = {'and','or','the','a','an','in','of','for','to','with','on','at'}
    toks = re.split(r'(\s+)', s.lower())
    out=[]
    for i,t in enumerate(toks):
        if t.isspace(): out.append(t); continue
        out.append(t if i>0 and t in minor else t.capitalize())
    return ''.join(out)

def generate_titles(text, style='professional'):
    keys = extract_keywords(text, 5)
    topic = ' '.join(keys[:3]).title() if keys else shorten_text(text)[:45].strip()
    if not topic:
        topic = 'Your Topic'
    templates = [
        f'How to Improve {topic} Without Making It Complicated',
        f'{topic}: A Practical Guide for Better Results',
        f'The Smart Way to Handle {topic}',
        f'{topic} Made Simple: Clear Steps and Useful Tips',
        f'Why {topic} Matters and How to Use It Better',
    ]
    return '\n'.join(f'{i+1}. {t}' for i,t in enumerate(templates))

def seo_meta_title(text):
    keys = extract_keywords(text, 4)
    topic = ' '.join(keys[:3]).title() if keys else 'Professional Writing Tool'
    return '\n'.join([
        f'{topic} | Complete Guide & Practical Tips',
        f'Best {topic} Strategies for Better Results',
        f'{topic}: Simple, Clear & Effective Guide'
    ])

def seo_meta_description(text):
    keys = extract_keywords(text, 5)
    topic = ', '.join(keys[:3]) if keys else 'your topic'
    desc = f'Learn about {topic} with clear explanations, practical steps, and useful examples designed to improve understanding and results.'
    return desc[:157]

def slugify(text):
    keys = extract_keywords(text, 6)
    base = ' '.join(keys[:5]) if keys else text[:80]
    slug = re.sub(r'[^a-z0-9]+','-', base.lower()).strip('-')
    return slug or 'new-page'

def keyword_density(text):
    ws = [w for w in words(text) if w not in STOPWORDS and len(w)>3]
    total = len(ws) or 1
    freq = Counter(ws)
    lines = ['Keyword | Count | Density', '---|---:|---:']
    for w,c in freq.most_common(15):
        lines.append(f'{w} | {c} | {round(c*100/total,2)}%')
    return '\n'.join(lines)

def faq_builder(text):
    keys = extract_keywords(text, 6)
    if not keys:
        keys = ['topic','process','benefit']
    lines = []
    for k in keys[:6]:
        lines.append(f'Q: What is {k}?\nA: {k.title()} is an important part of the topic and should be explained with simple examples, benefits, and practical use.\n')
    return '\n'.join(lines)

def heading_optimizer(text):
    keys = extract_keywords(text, 5)
    topic = ' '.join(keys[:2]).title() if keys else 'Main Topic'
    return '\n'.join([
        f'H1: {topic}: Complete Guide',
        f'H2: What Is {topic}?',
        f'H2: Why {topic} Matters',
        f'H2: Best Practices for {topic}',
        f'H2: Common Mistakes to Avoid',
        f'H2: Final Checklist'
    ])

def featured_snippet(text):
    s = summarize(text, 0.25, 2)
    return shorten_text(s)[:320]

def search_intent(text):
    q = text.lower()
    if any(x in q for x in ['buy','price','best','review','cheap','discount']): intent='Commercial / transactional'
    elif any(x in q for x in ['login','website','official','near me']): intent='Navigational / local'
    elif any(x in q for x in ['how','what','why','guide','tips','learn']): intent='Informational'
    else: intent='General informational'
    return f'Estimated search intent: {intent}\n\nRecommended content angle: Give a direct answer first, then add examples, steps, FAQs, and a clear call-to-action.'

def study_notes(text):
    keys = extract_keywords(text, 8)
    summ = summarize(text, 0.35, 5)
    return f'# Study Notes\n\n## Summary\n{summ}\n\n## Key Terms\n' + '\n'.join(f'- {k.title()}' for k in keys)

def important_points(text):
    sents = sentence_split(summarize(text, 0.45, 8))
    return '\n'.join(f'{i+1}. {s}' for i,s in enumerate(sents))

def mcq_generator(text):
    keys = extract_keywords(text, 8)
    if len(keys)<4: keys += ['concept','example','method','result']
    lines=[]
    for i,k in enumerate(keys[:5],1):
        options = random.sample(keys[:8], min(4,len(keys[:8])))
        if k not in options: options[0]=k
        random.shuffle(options)
        lines.append(f'{i}. Which term is most related to the main topic: {k.title()}?')
        for label,opt in zip('ABCD', options[:4]): lines.append(f'   {label}. {opt.title()}')
        lines.append(f'   Answer: {k.title()}\n')
    return '\n'.join(lines)

def flashcards(text):
    keys=extract_keywords(text,10)
    lines=[]
    for k in keys[:8]:
        lines.append(f'Q: What does "{k}" refer to in this content?\nA: It is a key idea in the topic. Explain it using the context and add one example.\n')
    return '\n'.join(lines)

def definition_extractor(text):
    defs=[]
    for s in sentence_split(text):
        m=re.search(r'\b([A-Z]?[A-Za-z][A-Za-z\s\-]{2,35})\s+(?:is|are|means|refers to)\s+(.+)',s,re.I)
        if m:
            defs.append(f'- **{m.group(1).strip().title()}**: {m.group(2).strip()}')
    if not defs:
        defs=[f'- **{k.title()}**: A key term related to the provided content.' for k in extract_keywords(text,8)]
    return '\n'.join(defs)

def essay_outline(text):
    topic = ' '.join(extract_keywords(text, 3)).title() or 'Essay Topic'
    return f'''# Essay Outline: {topic}

## Introduction
- Hook: Start with a clear statement about {topic}.
- Background: Briefly explain the context.
- Thesis: Present your main argument.

## Body Paragraph 1
- Main point
- Evidence or example
- Explanation

## Body Paragraph 2
- Main point
- Evidence or example
- Explanation

## Body Paragraph 3
- Counterargument or deeper analysis
- Response and explanation

## Conclusion
- Restate the thesis
- Summarize key points
- End with a strong final thought.'''

def citation_formatter(text):
    lines=[l.strip() for l in text.split('\n') if l.strip()]
    data=' '.join(lines)
    # Accept rough input: author, title, year, source.
    parts=[p.strip() for p in re.split(r'\||,', data) if p.strip()]
    author=parts[0] if len(parts)>0 else 'Author Lastname, Initials'
    title=parts[1] if len(parts)>1 else 'Title of work'
    year=next((p for p in parts if re.search(r'\b(19|20)\d{2}\b',p)), 'n.d.')
    source=parts[-1] if len(parts)>2 else 'Source'
    return f'''APA: {author}. ({year}). {title}. {source}.
MLA: {author}. "{title}." {source}, {year}.
Harvard: {author} ({year}) {title}. {source}.'''

def assignment_formatter(text):
    return f'''# Assignment

## Title
{generate_titles(text).splitlines()[0].split('. ',1)[-1] if text else 'Assignment Title'}

## Introduction
{summarize(text,0.18,2)}

## Main Discussion
{bullet_points(text)}

## Conclusion
{featured_snippet(text)}

## References
- Add sources used in this assignment here.'''

def email_writer(text, tone='professional'):
    subject = generate_titles(text).splitlines()[0].split('. ',1)[-1] if text else 'Project Update'
    return f'''Subject: {subject}

Dear [Recipient Name],

I hope you are doing well.

{grammar_polish(rewrite_text(text, 'professional', 'balanced')) if text else 'I am writing to share an update and request your feedback on the matter.'}

Please let me know if you would like any changes or additional details.

Best regards,
[Your Name]'''

def proposal_writer(text):
    topic=' '.join(extract_keywords(text,3)).title() or 'Project'
    return f'''# Proposal: {topic}

## Understanding
{summarize(text,0.25,2)}

## Proposed Solution
- Review the requirements carefully.
- Create a clear, practical solution.
- Deliver polished, ready-to-use work.

## Deliverables
- Final completed work
- Revisions if required
- Clean formatting and documentation

## Timeline
Estimated delivery: [Add timeline]

## Closing
I would be happy to help you complete this project with quality and attention to detail.'''

def meeting_notes(text):
    sents=sentence_split(text)
    actions=[s for s in sents if re.search(r'\b(need to|will|must|should|deadline|by\s+\w+day|assign|task)\b',s,re.I)]
    decisions=[s for s in sents if re.search(r'\b(decided|agreed|approved|confirmed|final)\b',s,re.I)]
    return f'''# Meeting Notes

## Summary
{summarize(text,0.35,4)}

## Decisions
{chr(10).join('- '+d for d in decisions) if decisions else '- No explicit decisions detected.'}

## Action Items
{chr(10).join('- '+a for a in actions) if actions else '- Review notes and add owners/deadlines manually.'}

## Next Steps
- Confirm responsibilities.
- Set deadlines.
- Share final notes with the team.'''

def customer_reply(text):
    return f'''Hi [Customer Name],

Thank you for reaching out. I understand your concern and I’m sorry for any inconvenience caused.

{grammar_polish(rewrite_text(text, 'professional', 'balanced')) if text else 'We are reviewing the issue and will help you with the next best solution.'}

Please share any extra details if available, and we will do our best to resolve this as quickly as possible.

Best regards,
Support Team'''

def resume_bullets(text):
    keys=extract_keywords(text,6)
    if not keys: keys=['project','quality','workflow']
    lines=[]
    for k in keys[:5]:
        lines.append(f'- Improved {k} by applying structured planning, clear execution, and measurable quality checks.')
    return '\n'.join(lines)

def cover_letter(text):
    role=' '.join(extract_keywords(text,2)).title() or 'the Role'
    return f'''Dear Hiring Manager,

I am excited to apply for {role}. My experience and interest align with the needs described, and I am confident in my ability to contribute with reliable work, clear communication, and a strong learning mindset.

{summarize(text,0.3,3)}

I would appreciate the opportunity to discuss how I can support your team.

Sincerely,
[Your Name]'''

def linkedin_bio(text):
    keys=extract_keywords(text,5)
    return f'''I am a motivated professional focused on {', '.join(keys[:3]) if keys else 'technology, writing, and practical problem solving'}. I enjoy building useful solutions, improving workflows, and creating clear results that help people work better. My strengths include communication, consistency, and a practical approach to solving real problems.'''

def product_description(text):
    special = compact_product_or_title_rewrite(text, 'professional', 'strong')
    if special:
        topic = compact_topic(text, 'Product')
        keys = extract_keywords(text, 8)
        focus = ', '.join(keys[:3]) if keys else 'customer value, quality, and usability'
        return f"""{topic}

{special}

Key benefits:
- Polished and reader-friendly product presentation
- Clearer structure for e-commerce pages and listings
- Stronger focus on {focus}
- Ready to use in product pages, ads, or social captions

Best for: shoppers who want a clear, reliable, and professional product overview."""
    topic=text.strip().split('\n')[0][:90] if text.strip() else 'Product'
    keys=extract_keywords(text,6)
    return f"""{topic}

Create a more polished experience with this practical, well-designed product. It is built for users who want {', '.join(keys[:3]) if keys else 'quality, convenience, and reliable performance'} in one simple solution.

Key benefits:
- Clean and user-friendly design
- Practical features for everyday use
- Reliable quality and a professional finish
- Suitable for personal, business, or creative needs

Perfect for customers who want a dependable product with a premium feel."""

def invoice_note(text):
    return f'''Thank you for your business. This invoice covers the completed work/services described below:

{bullet_points(text) if text else '- Professional services delivered as agreed.'}

Please process the payment by the due date. If you have any questions, feel free to contact us.'''

def terms_draft(text):
    name = text.strip().split('\n')[0][:50] if text.strip() else '[Website Name]'
    return f'''# Simple Terms Draft for {name}

## Use of Service
By using this website, users agree to use the tools responsibly and only for lawful purposes.

## User Content
Users are responsible for the text, files, and information they upload or process.

## Accuracy
The tools provide helpful writing assistance, but users should review all outputs before publishing or submitting them.

## Payments
Digital product purchases may be non-refundable unless stated otherwise.

## Contact
For support, contact: [your email].'''

def viral_hooks(text):
    topic=' '.join(extract_keywords(text,3)).title() or 'This Topic'
    hooks=[
        f'Nobody tells you this about {topic}...',
        f'If you are struggling with {topic}, watch this first.',
        f'This simple mistake is ruining your {topic}.',
        f'I tried {topic} so you do not have to.',
        f'Here is the fastest way to understand {topic}.',
        f'Before you start {topic}, remember this.',
    ]
    return '\n'.join(f'{i+1}. {h}' for i,h in enumerate(hooks))

def youtube_script(text):
    topic=' '.join(extract_keywords(text,3)).title() or 'Your Topic'
    return f'''# YouTube Script: {topic}

## Hook (0-10 seconds)
{viral_hooks(text).splitlines()[0].split('. ',1)[-1]}

## Intro
In this video, we will break down {topic} in a simple and practical way.

## Main Points
{bullet_points(summarize(text,0.55,6)) if text else '- Explain the problem\n- Show the solution\n- Give examples'}

## Example
Use a real-life example so viewers understand the idea quickly.

## Conclusion
If this helped you, save this video and share it with someone who needs it.'''

def youtube_description(text):
    topic=' '.join(extract_keywords(text,3)).title() or 'This Video'
    return f'''In this video, we explain {topic} in a clear, practical, and easy-to-understand way.

What you will learn:
{bullet_points(summarize(text,0.4,5)) if text else '- Key ideas\n- Useful examples\n- Practical steps'}

Subscribe for more helpful content.

# {hashtag_generator(text)}'''.replace('# #','#')

def instagram_caption(text):
    topic=' '.join(extract_keywords(text,2)).title() or 'today’s idea'
    return f'''{topic} can change the way you think, work, and create.

{featured_snippet(text) if text else 'Keep improving one small step at a time.'}

Save this post for later.\n\n{hashtag_generator(text)}'''

def twitter_thread(text):
    points=sentence_split(summarize(text,0.65,8))
    if not points: points=['Start with a clear idea.','Explain the value.','Give examples.','End with a practical takeaway.']
    lines=[]
    lines.append(f'1/{len(points)+1} {viral_hooks(text).splitlines()[0].split(". ",1)[-1]}')
    for i,p in enumerate(points,2):
        lines.append(f'{i}/{len(points)+1} {shorten_text(p)}')
    return '\n\n'.join(lines)

def cta_generator(text):
    topic=' '.join(extract_keywords(text,2)).title() or 'this'
    return '\n'.join([
        f'Try {topic} today and see the difference.',
        f'Start improving your {topic} now.',
        f'Download now and make your workflow easier.',
        f'Save time, improve quality, and get better results.',
        f'Click below to get started.'
    ])

def hashtag_generator(text):
    keys=extract_keywords(text,8)
    tags=['#'+re.sub(r'[^A-Za-z0-9]','',k.title()) for k in keys[:8]]
    if not tags: tags=['#Writing','#Content','#Productivity']
    return ' '.join(tags)

def carousel_outline(text):
    topic=' '.join(extract_keywords(text,3)).title() or 'Topic'
    points=sentence_split(summarize(text,0.55,6))
    slides=[f'Slide 1: {topic}\nHook: {viral_hooks(text).splitlines()[0].split(". ",1)[-1]}']
    for i,p in enumerate(points[:6],2): slides.append(f'Slide {i}: {shorten_text(p)}')
    slides.append(f'Slide {len(slides)+1}: Save this post and follow for more practical tips.')
    return '\n\n'.join(slides)

def markdown_converter(text):
    sents=sentence_split(text)
    if not sents: return ''
    title=generate_titles(text).splitlines()[0].split('. ',1)[-1]
    body='\n\n'.join(sents)
    return f'# {title}\n\n{body}\n\n## Key Points\n{bullet_points(text)}'

def case_formatter(text, case='title'):
    if case == 'upper': return text.upper()
    if case == 'lower': return text.lower()
    if case == 'sentence': return grammar_polish(text.lower())
    return title_case(text)

def prompt_writer(text):
    topic=text.strip() or 'your task'
    return f'''Act as an expert assistant. Your task is to help with: {topic}

Requirements:
- Use clear and professional language.
- Give structured output with headings and bullet points.
- Include practical examples where useful.
- Avoid vague statements.
- Make the final answer ready to use.

Output format:
1. Overview
2. Step-by-step solution
3. Examples
4. Final checklist'''

def prompt_improver(text):
    return f'''Improved Prompt:

{prompt_writer(text)}

Extra quality rules:
- Ask only necessary clarifying questions.
- Make reasonable assumptions if details are missing.
- Keep the response focused, polished, and actionable.'''

def text_table(text):
    lines=[l.strip(' -•\t') for l in text.split('\n') if l.strip()]
    if not lines:
        lines=sentence_split(text)
    table=['Item | Details','---|---']
    for i,l in enumerate(lines[:20],1):
        if ':' in l:
            a,b=l.split(':',1)
            table.append(f'{a.strip()} | {b.strip()}')
        else:
            table.append(f'{i} | {l}')
    return '\n'.join(table)

def action_items(text):
    sents=sentence_split(text)
    matches=[s for s in sents if re.search(r'\b(need to|must|should|will|task|todo|deadline|by|assign|finish|complete|send|create|review)\b',s,re.I)]
    if not matches: matches=sents[:5]
    return '\n'.join(f'- [ ] {shorten_text(m).rstrip(".")}' for m in matches)

def tone_analysis(text):
    ws=set(words(text))
    lines=[]
    for tone, bank in EMOTIONS.items():
        hit=len(ws & bank)
        lines.append(f'- {tone.title()}: {min(100, hit*20)}% signal ({", ".join(sorted(ws & bank)) or "no strong signal"})')
    return 'Tone signals:\n'+'\n'.join(lines)

def sentiment_analysis(text):
    ws=words(text)
    pos=sum(1 for w in ws if w in EMOTIONS['positive'])
    neg=sum(1 for w in ws if w in EMOTIONS['negative'])
    if pos>neg: label='Positive'
    elif neg>pos: label='Negative'
    else: label='Neutral'
    return f'Sentiment: {label}\nPositive words: {pos}\nNegative words: {neg}\nConfidence: {round(abs(pos-neg)/max(1,pos+neg)*100,1)}%'

def passive_voice_detector(text):
    sents=sentence_split(text)
    flagged=[s for s in sents if re.search(r'\b(is|are|was|were|be|been|being)\s+\w+ed\b',s,re.I)]
    return 'Possible passive voice sentences:\n' + ('\n'.join('- '+s for s in flagged) if flagged else 'No strong passive voice pattern found.')

def repetition_detector(text):
    freq=Counter(w for w in words(text) if w not in STOPWORDS and len(w)>3)
    repeated=[(w,c) for w,c in freq.most_common(20) if c>1]
    if not repeated: return 'No heavy repetition detected.'
    return 'Repeated words:\n'+'\n'.join(f'- {w}: {c} times' for w,c in repeated)

def overused_words(text):
    filler=['very','really','actually','basically','just','literally','amazing','perfect','important','things','stuff','nice','good','bad']
    freq=Counter(words(text))
    lines=[f'- {w}: {freq[w]}' for w in filler if freq[w]>0]
    return 'Overused/filler words:\n' + ('\n'.join(lines) if lines else 'No common filler words detected.')

def quality_score(text):
    m=metrics('',text)
    rep=sum(1 for w,c in Counter(words(text)).items() if c>3 and w not in STOPWORDS)
    readability=m['readability']
    sentence_bonus=20 if 8 <= (len(words(text))/max(1,len(sentence_split(text)))) <= 24 else 10
    score=max(0,min(100, int(readability*0.45 + sentence_bonus + max(0,30-rep*3))))
    return f'''Writing Quality Score: {score}/100

Readability: {readability}/100
Words: {m['words']}
Sentences: {m['sentences']}
Repeated-word penalty: {rep}

Suggestions:
- Keep sentences focused and varied.
- Remove repeated filler words.
- Add examples for stronger value.
- Use headings or bullets for long content.'''

def readability_analyzer(text):
    m=metrics('',text)
    avg=len(words(text))/max(1,len(sentence_split(text)))
    return f'''Readability Report

Score: {m['readability']}/100
Words: {m['words']}
Sentences: {m['sentences']}
Average sentence length: {round(avg,1)} words
Estimated reading time: {m['reading_time']} minute(s)

Tip: Scores above 60 are easier to read. Shorter sentences usually improve clarity.'''

def ai_style_checker(text):
    patterns=['delve','leverage','unlock','seamless','robust','cutting-edge','in today\'s world','game-changer','it is important to note','comprehensive','moreover','furthermore']
    found=[p for p in patterns if re.search(r'\b'+re.escape(p)+r'\b', text, re.I)]
    score=max(0,100-len(found)*12)
    return f'''Natural Writing Score: {score}/100

Robotic/overused patterns found:
{chr(10).join('- '+p for p in found) if found else '- None of the common robotic patterns were detected.'}

Suggestion: Use direct language, specific examples, and natural sentence variety.'''

# --- Extra professional no-API tools added for the upgraded interface ---
def compact_topic(text, fallback='Your Topic', limit=7):
    keys = extract_keywords(text, limit)
    if keys:
        return ' '.join(keys[:min(4, len(keys))]).title()
    cleaned = clean_spaces(text)
    return (cleaned[:70].strip(' .,!?:;') or fallback).title()

def compact_product_or_title_rewrite(text, tone='professional', strength='strong'):
    raw = clean_spaces(text)
    if not raw:
        return ''
    # Handles product titles / one-line keyword-heavy copy that normal sentence rewriting cannot transform well.
    separators = [p.strip(' -•') for p in re.split(r'\s*\|\s*|\s*/\s*|\s*,\s*', raw) if p.strip()]
    if len(separators) < 3 and len(sentence_split(raw)) > 1:
        return ''
    brand = separators[0][:90] if separators else raw[:90]
    features = []
    for part in separators[1:10]:
        cleaned = re.sub(r'\b(with|and|for|the|a|an)\b', '', part, flags=re.I).strip()
        if cleaned and cleaned.lower() not in {x.lower() for x in features}:
            features.append(cleaned)
    keys = extract_keywords(raw, 8)
    feature_line = ', '.join(features[:5]) if features else ', '.join(keys[:5])
    audience = 'people who want a polished, practical, and easy-to-use solution'
    if re.search(r'\bmature skin\b', raw, re.I): audience = 'mature skin routines and everyday beauty users'
    if re.search(r'\bstudent|assignment|study\b', raw, re.I): audience = 'students and academic users'
    if re.search(r'\bbusiness|client|marketing|sales\b', raw, re.I): audience = 'business users, creators, and client-facing teams'
    return grammar_polish(f"""{brand} is a refined, well-organized option designed for {audience}. It brings together {feature_line} in a clearer and more professional format, making the content easier to understand and more appealing to readers.

This version highlights the main value, removes the crowded keyword-style layout, and presents the information as polished copy that feels natural, structured, and ready to publish.""")

def deep_rewrite_text(text, mode='professional', strength='maximum'):
    special = compact_product_or_title_rewrite(text, mode, strength)
    if special:
        return special
    sents = sentence_split(text)
    if not sents:
        return ''
    rewritten=[]
    starters = {
        'professional':['From a practical perspective', 'In a clearer form', 'For a stronger result', 'Professionally written'],
        'academic':['In academic terms', 'This can be understood as', 'A clearer interpretation is', 'The main idea suggests'],
        'friendly':['Simply put', 'In an easier way', 'Here is the idea', 'Think of it this way'],
        'persuasive':['The key advantage is', 'What makes this valuable is', 'The strongest reason is', 'This matters because'],
        'simple':['In simple words', 'The main point is', 'This means', 'A simple way to say it is']
    }
    for i, sent in enumerate(sents):
        base = restructure_sentence(sent, mode, 'maximum')
        base = synonymize_text(base, 'maximum')
        if i % 2 == 0 and len(words(base)) > 8:
            lead = starters.get(mode, starters['professional'])[i % 4]
            base = f"{lead}, {base[0].lower()+base[1:]}"
        if jaccard_similarity(sent, base) > 65:
            keys = extract_keywords(sent, 6)
            idea = ', '.join(keys[:4]) if keys else shorten_text(sent)
            base = f"This section focuses on {idea}, presenting the idea with clearer wording, smoother structure, and a more original flow."
        rewritten.append(base)
    return grammar_polish(add_transitions(' '.join(rewritten)))

def clean_ai_style(text):
    special = compact_product_or_title_rewrite(text, 'professional', 'strong')
    if special:
        return special
    replacements = {
        r'\bin today\'s (digital )?world\b':'today', r'\bit is important to note that\b':'note that',
        r'\bdelve into\b':'explain', r'\bleverage\b':'use', r'\bunlock\b':'improve',
        r'\bseamless\b':'smooth', r'\brobust\b':'reliable', r'\bcutting-edge\b':'modern',
        r'\bgame-changer\b':'useful improvement', r'\bcomprehensive\b':'complete',
        r'\bfurthermore\b':'also', r'\bmoreover\b':'also', r'\bin conclusion\b':'overall'
    }
    out = text
    for pat, repl in replacements.items():
        out = re.sub(pat, repl, out, flags=re.I)
    out = rewrite_text(out, 'professional', 'strong')
    return grammar_polish(out)

def add_better_transitions(text):
    sents = sentence_split(text)
    if not sents: return ''
    transitions = ['First', 'Next', 'As a result', 'Another useful point is', 'In practical terms', 'Finally']
    return grammar_polish(' '.join((transitions[i % len(transitions)] + ', ' + s[0].lower()+s[1:] if i and not re.match(r'^(First|Next|Finally|Also|However|Therefore|As a result)', s) else s) for i,s in enumerate(sents)))

def improve_sentence_variety(text):
    sents = sentence_split(text)
    if not sents: return ''
    out=[]
    for i,s in enumerate(sents):
        if i % 3 == 0:
            out.append(shorten_text(s))
        elif i % 3 == 1:
            out.append(expand_text(s))
        else:
            out.append(rewrite_text(s, 'professional', 'balanced'))
    return grammar_polish(' '.join(out))

def weak_word_detector(text):
    weak=['very','really','just','actually','basically','things','stuff','nice','good','bad','amazing','perfect','important','maybe','probably','somewhat','quite']
    freq=Counter(words(text))
    hits=[f'- {w}: {freq[w]} time(s) → consider a more specific word.' for w in weak if freq[w]]
    return 'Weak or vague words found:\n' + ('\n'.join(hits) if hits else 'No common weak-word patterns detected.')

def sentence_variety_score(text):
    sents=sentence_split(text)
    lengths=[len(words(s)) for s in sents]
    if not lengths: return 'No sentences found.'
    avg=sum(lengths)/len(lengths)
    spread=max(lengths)-min(lengths) if len(lengths)>1 else 0
    score=min(100, int(45 + spread*3 + (10 if 10 <= avg <= 22 else 0)))
    return f'''Sentence Variety Score: {score}/100

Sentence lengths: {', '.join(map(str,lengths[:30]))}
Average length: {round(avg,1)} words
Variation range: {spread} words

Suggestion: Mix short, medium, and longer sentences to make the writing feel more natural.'''

def content_brief(text):
    topic=compact_topic(text)
    keys=extract_keywords(text,10)
    return f'''# Content Brief: {topic}

## Target Audience
- Readers interested in {topic.lower()}

## Core Angle
- Explain the topic clearly, show practical value, and give useful examples.

## Primary Keywords
{chr(10).join('- '+k for k in keys[:8]) if keys else '- Add primary keywords'}

## Suggested Structure
1. Hook and short introduction
2. Problem or context
3. Key points and examples
4. Practical steps
5. Conclusion and call-to-action'''

def originality_risk_report(text):
    ws=[w for w in words(text) if w not in STOPWORDS and len(w)>3]
    repeated=[(w,c) for w,c in Counter(ws).most_common(12) if c>2]
    phrases=top_phrases(text,2,10)
    risk=min(100, len(repeated)*8 + len(phrases)*3)
    return f'''Originality Risk Report

Estimated local risk: {risk}/100
Repeated words: {', '.join(f'{w}({c})' for w,c in repeated) if repeated else 'No heavy repetition detected'}
Repeated phrase patterns: {', '.join(phrases[:8]) if phrases else 'No repeated phrase pattern detected'}

Recommendations:
- Restructure long sentences instead of changing only words.
- Add your own examples, explanation, and source citation where needed.
- Use Deep Rewriter or AI-Style Cleaner for a stronger revision.'''

def blog_post_builder(text):
    topic=compact_topic(text)
    return f'''# {topic}: A Practical Guide

## Introduction
{viral_hooks(text).splitlines()[0].split('. ',1)[-1]}

{summarize(text,0.25,2)} This guide explains the idea in a clear, practical way so readers can understand the value quickly.

## Why It Matters
{featured_snippet(text)}

## Key Points
{bullet_points(summarize(text,0.5,5)) if text else '- Explain the main problem\n- Present the solution\n- Add useful examples'}

## Practical Steps
1. Define the goal clearly.
2. Break the topic into smaller parts.
3. Add examples, benefits, and use cases.
4. End with a clear next step.

## Conclusion
{topic} becomes easier to understand when the idea is organized, practical, and written for the reader's needs.'''

def content_calendar(text):
    topic=compact_topic(text)
    ideas=extract_keywords(text,10) or ['tips','guide','mistakes','benefits','examples','checklist','summary']
    return '\n'.join([f'Day {i+1}: {topic} - {ideas[i%len(ideas)].title()} angle | Format: post + short caption' for i in range(7)])

def seo_brief(text):
    topic=compact_topic(text)
    return f'''# SEO Content Brief: {topic}

Search intent: {search_intent(text)}

Primary keywords:
{chr(10).join('- '+k for k in extract_keywords(text,10))}

Recommended headings:
{heading_optimizer(text)}

FAQ opportunities:
{faq_builder(text)}'''

def schema_faq_json(text):
    keys=extract_keywords(text,5) or ['topic','benefit','process']
    items=[]
    for k in keys[:5]:
        items.append('{"@type":"Question","name":"What is '+k.title()+'?","acceptedAnswer":{"@type":"Answer","text":"'+k.title()+' is an important part of this topic and should be explained with clear examples and practical details."}}')
    return '{\n  "@context":"https://schema.org",\n  "@type":"FAQPage",\n  "mainEntity":[\n    '+',\n    '.join(items)+'\n  ]\n}'

def glossary_builder(text):
    keys=extract_keywords(text,12)
    return '# Glossary\n\n' + ('\n'.join(f'- **{k.title()}**: A key concept related to the topic that should be explained with a simple example.' for k in keys) if keys else '- Add text to generate glossary terms.')

def thesis_statement(text):
    topic=compact_topic(text)
    return '\n'.join([f'{i+1}. {topic} is important because it connects practical value, clear evidence, and real-world impact in a way that improves understanding.' for i in range(3)])

def discussion_post(text):
    topic=compact_topic(text)
    return f'''Discussion Post: {topic}

One important point about {topic.lower()} is that it becomes more useful when we connect the idea to real examples. {summarize(text,0.25,2)}

I think the strongest takeaway is that the topic should be explained clearly, with practical steps and supporting details.

Question for discussion: What example best shows the value of {topic.lower()}?'''

def lesson_plan(text):
    topic=compact_topic(text)
    return f'''# Lesson Plan: {topic}

## Objectives
- Understand the main idea of {topic}
- Identify key terms and examples
- Apply the idea through a short activity

## Warm-up
Ask students what they already know about {topic.lower()}.

## Main Activity
{bullet_points(summarize(text,0.4,4))}

## Assessment
- Short quiz
- One-paragraph explanation
- Practical example'''

def cold_email(text):
    topic=compact_topic(text,'your offer')
    return f'''Subject: Quick idea for {topic}

Hi [Name],

I noticed your work around [company/topic] and wanted to share a quick idea. I can help with {topic.lower()} by creating a cleaner, more practical solution that saves time and improves quality.

Would you be open to a short discussion this week?

Best regards,
[Your Name]'''

def meeting_agenda(text):
    topic=compact_topic(text,'Meeting')
    return f'''# Meeting Agenda: {topic}

1. Opening and objective
2. Current situation
3. Key discussion points
{chr(10).join('- '+k.title() for k in extract_keywords(text,5))}
4. Decisions needed
5. Action items and deadlines
6. Next meeting plan'''

def job_description(text):
    role=compact_topic(text,'Role')
    return f'''# Job Description: {role}

## Overview
We are looking for a motivated candidate to support {role.lower()} with quality, ownership, and clear communication.

## Responsibilities
- Manage daily tasks related to {role.lower()}
- Communicate progress clearly
- Improve workflows and deliver reliable results

## Requirements
- Strong communication skills
- Problem-solving mindset
- Relevant experience or willingness to learn

## Benefits
- Growth-focused work environment
- Practical experience
- Opportunity to contribute to meaningful projects'''

def client_brief(text):
    topic=compact_topic(text,'Project')
    return f'''# Client Brief: {topic}

## Goal
Create a clear, high-quality solution for {topic.lower()}.

## Background
{summarize(text,0.25,3)}

## Deliverables
- Final written output or project asset
- Clean formatting
- Revisions if needed

## Success Criteria
- Clear structure
- Professional quality
- Ready-to-use final delivery'''

def swot_analysis(text):
    topic=compact_topic(text)
    keys=extract_keywords(text,8)
    return f'''# SWOT Analysis: {topic}

## Strengths
- Clear value around {keys[0] if keys else topic}
- Useful for a defined audience

## Weaknesses
- Needs stronger examples and proof
- May require clearer positioning

## Opportunities
- Improve messaging and structure
- Create content, offers, or workflows around this topic

## Threats
- Similar content may already exist
- Weak differentiation can reduce impact'''

def short_video_script(text):
    topic=compact_topic(text)
    hook=viral_hooks(text).splitlines()[0].split('. ',1)[-1]
    return f'''# Short Video Script: {topic}

0-3 sec Hook:
{hook}

3-20 sec Main Point:
{featured_snippet(text)}

20-45 sec Value:
{bullet_points(summarize(text,0.45,4))}

45-60 sec CTA:
Save this and follow for more practical tips.'''

def linkedin_post(text):
    topic=compact_topic(text)
    return f'''{topic} is not just about doing more — it is about creating clearer, more useful results.

{summarize(text,0.3,3)}

What I would focus on:
{bullet_points(text)}

The best results come from clarity, consistency, and practical execution.

What would you add?'''

def facebook_ad(text):
    topic=compact_topic(text,'Your Offer')
    return f'''Headline: Make {topic} Easier

Primary Text: Looking for a simpler way to handle {topic.lower()}? This solution helps you save time, improve quality, and get clearer results without unnecessary complexity.

CTA: Learn More'''

def social_calendar(text):
    topic=compact_topic(text)
    formats=['Educational post','Short video','Carousel','Story poll','Case study','Behind-the-scenes','CTA post']
    return '\n'.join(f'Day {i+1}: {formats[i]} about {topic} | Goal: {goal}' for i,goal in enumerate(['awareness','engagement','saves','interaction','trust','connection','conversion']))

def executive_summary(text):
    topic=compact_topic(text,'Project')
    return f'''# Executive Summary: {topic}

{summarize(text,0.22,4)}

Key takeaway: The content should be presented with clear structure, practical value, and focused next steps.

Recommended next steps:
- Clarify the main goal
- Organize the key points
- Add proof, examples, or action items'''

def pros_cons_list(text):
    topic=compact_topic(text)
    keys=extract_keywords(text,8)
    return f'''# Pros and Cons: {topic}

## Pros
- Useful for {keys[0] if keys else 'the main goal'}
- Can improve clarity and decision-making
- Helps organize important information

## Cons
- May need more examples or evidence
- Can feel generic without specific details
- Requires review before publishing or submission'''

def timeline_extractor(text):
    sents=sentence_split(text)
    matches=[s for s in sents if re.search(r'\b(\d{4}|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|today|tomorrow|week|month|year|deadline|before|after|by)\b', s, re.I)]
    if not matches: matches=sents[:6]
    return '# Timeline / Milestones\n\n' + '\n'.join(f'- {shorten_text(s).rstrip(".")}' for s in matches)

def content_repurposer(text):
    return f'''# Repurposed Content Pack

## Short Summary
{summarize(text,0.2,2)}

## Social Caption
{instagram_caption(text)}

## Email Angle
{email_writer(text)}

## Bullet Version
{bullet_points(text)}

## Title Ideas
{generate_titles(text)}'''

def process_tool(tool_id, text, params=None):
    params=params or {}
    text=text or ''
    strength=params.get('strength','strong')
    tone=params.get('tone','professional')
    case=params.get('case','title')
    if tool_id in ('humanizer','paragraph_rewriter'):
        out=deep_rewrite_text(text, 'professional', strength)
    elif tool_id=='deep_rewriter': out=deep_rewrite_text(text, tone, 'maximum')
    elif tool_id=='ai_style_cleaner': out=clean_ai_style(text)
    elif tool_id=='professional_rewriter': out=rewrite_text(text, 'professional', strength)
    elif tool_id=='simple_rewriter': out=simplify_text(rewrite_text(text, 'simple', 'balanced'))
    elif tool_id=='sentence_shortener': out=shorten_text(text)
    elif tool_id=='sentence_expander': out=expand_text(text)
    elif tool_id=='tone_converter': out=rewrite_text(text, tone, strength)
    elif tool_id=='active_voice': out=active_voice(text)
    elif tool_id=='grammar_polish': out=grammar_polish(text)
    elif tool_id=='clarity_enhancer': out=shorten_text(rewrite_text(text, 'professional','balanced'))
    elif tool_id=='transition_adder': out=add_better_transitions(text)
    elif tool_id=='sentence_variety_improver': out=improve_sentence_variety(text)
    elif tool_id=='readability_analyzer': out=readability_analyzer(text)
    elif tool_id=='quality_score': out=quality_score(text)
    elif tool_id=='repetition_detector': out=repetition_detector(text)
    elif tool_id=='overused_words': out=overused_words(text)
    elif tool_id=='weak_word_detector': out=weak_word_detector(text)
    elif tool_id=='sentence_variety_score': out=sentence_variety_score(text)
    elif tool_id=='passive_voice_detector': out=passive_voice_detector(text)
    elif tool_id=='tone_analysis': out=tone_analysis(text)
    elif tool_id=='sentiment_analysis': out=sentiment_analysis(text)
    elif tool_id=='keyword_extractor': out='\n'.join(extract_keywords(text,20))
    elif tool_id=='content_brief': out=content_brief(text)
    elif tool_id=='originality_risk_report': out=originality_risk_report(text)
    elif tool_id=='compare_similarity': out=f"Estimated text overlap between input and output area is shown in analytics. Input self-similarity: 100%. Paste a rewritten version into output and compare using analytics."
    elif tool_id=='ai_style_checker': out=ai_style_checker(text)
    elif tool_id=='blog_outline': out=outline(text)
    elif tool_id=='blog_intro': out=f"{viral_hooks(text).splitlines()[0].split('. ',1)[-1]}\n\n{summarize(text,0.25,2)} This guide explains the idea in a clear, practical way so readers can understand the value quickly."
    elif tool_id=='blog_post_builder': out=blog_post_builder(text)
    elif tool_id=='content_calendar': out=content_calendar(text)
    elif tool_id=='seo_brief': out=seo_brief(text)
    elif tool_id=='meta_title': out=seo_meta_title(text)
    elif tool_id=='meta_description': out=seo_meta_description(text)
    elif tool_id=='slug_generator': out=slugify(text)
    elif tool_id=='keyword_density': out=keyword_density(text)
    elif tool_id=='faq_builder': out=faq_builder(text)
    elif tool_id=='schema_faq_json': out=schema_faq_json(text)
    elif tool_id=='heading_optimizer': out=heading_optimizer(text)
    elif tool_id=='snippet_generator': out=featured_snippet(text)
    elif tool_id=='search_intent': out=search_intent(text)
    elif tool_id=='study_notes': out=study_notes(text)
    elif tool_id=='important_points': out=important_points(text)
    elif tool_id=='mcq_generator': out=mcq_generator(text)
    elif tool_id=='flashcards': out=flashcards(text)
    elif tool_id=='definition_extractor': out=definition_extractor(text)
    elif tool_id=='glossary_builder': out=glossary_builder(text)
    elif tool_id=='thesis_statement': out=thesis_statement(text)
    elif tool_id=='discussion_post': out=discussion_post(text)
    elif tool_id=='lesson_plan': out=lesson_plan(text)
    elif tool_id=='essay_outline': out=essay_outline(text)
    elif tool_id=='citation_formatter': out=citation_formatter(text)
    elif tool_id=='assignment_formatter': out=assignment_formatter(text)
    elif tool_id=='research_summary': out=summarize(text,0.30,5)
    elif tool_id=='quiz_generator': out='\n'.join(f'{i+1}. Explain {k.title()} in your own words.' for i,k in enumerate(extract_keywords(text,8) or ['the main idea','the key benefit','the conclusion']))
    elif tool_id=='email_writer': out=email_writer(text)
    elif tool_id=='cold_email': out=cold_email(text)
    elif tool_id=='proposal_writer': out=proposal_writer(text)
    elif tool_id=='meeting_notes': out=meeting_notes(text)
    elif tool_id=='meeting_agenda': out=meeting_agenda(text)
    elif tool_id=='customer_reply': out=customer_reply(text)
    elif tool_id=='resume_bullets': out=resume_bullets(text)
    elif tool_id=='cover_letter': out=cover_letter(text)
    elif tool_id=='linkedin_bio': out=linkedin_bio(text)
    elif tool_id=='job_description': out=job_description(text)
    elif tool_id=='client_brief': out=client_brief(text)
    elif tool_id=='swot_analysis': out=swot_analysis(text)
    elif tool_id=='product_description': out=product_description(text)
    elif tool_id=='invoice_note': out=invoice_note(text)
    elif tool_id=='terms_draft': out=terms_draft(text)
    elif tool_id=='viral_hooks': out=viral_hooks(text)
    elif tool_id=='youtube_script': out=youtube_script(text)
    elif tool_id=='short_video_script': out=short_video_script(text)
    elif tool_id=='youtube_titles': out=generate_titles(text)
    elif tool_id=='youtube_description': out=youtube_description(text)
    elif tool_id=='tiktok_hooks': out='\n'.join(f'{i+1}. {h}' for i,h in enumerate([x.split('. ',1)[-1] for x in viral_hooks(text).splitlines()][:6]))
    elif tool_id=='instagram_caption': out=instagram_caption(text)
    elif tool_id=='linkedin_post': out=linkedin_post(text)
    elif tool_id=='facebook_ad': out=facebook_ad(text)
    elif tool_id=='twitter_thread': out=twitter_thread(text)
    elif tool_id=='cta_generator': out=cta_generator(text)
    elif tool_id=='hashtag_generator': out=hashtag_generator(text)
    elif tool_id=='carousel_outline': out=carousel_outline(text)
    elif tool_id=='social_calendar': out=social_calendar(text)
    elif tool_id=='clean_formatting': out=clean_spaces(text)
    elif tool_id=='markdown_converter': out=markdown_converter(text)
    elif tool_id=='case_formatter': out=case_formatter(text, case)
    elif tool_id=='bullet_generator': out=bullet_points(text)
    elif tool_id=='outline_builder': out=outline(text)
    elif tool_id=='executive_summary': out=executive_summary(text)
    elif tool_id=='pros_cons_list': out=pros_cons_list(text)
    elif tool_id=='timeline_extractor': out=timeline_extractor(text)
    elif tool_id=='title_generator': out=generate_titles(text)
    elif tool_id=='prompt_writer': out=prompt_writer(text)
    elif tool_id=='prompt_improver': out=prompt_improver(text)
    elif tool_id=='text_table': out=text_table(text)
    elif tool_id=='extract_action_items': out=action_items(text)
    elif tool_id=='content_repurposer': out=content_repurposer(text)
    else:
        out=rewrite_text(text, 'professional', strength)
    # Protection: if a rewriting-style tool returns almost the same, force a maximum pass.
    rewriting_tools={'humanizer','paragraph_rewriter','professional_rewriter','simple_rewriter','tone_converter','clarity_enhancer','deep_rewriter','ai_style_cleaner','sentence_variety_improver'}
    if tool_id in rewriting_tools and text.strip() and jaccard_similarity(text,out)>78:
        out=deep_rewrite_text(out, 'professional', 'maximum')
    return out
