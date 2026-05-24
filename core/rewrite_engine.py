import re
import math
import random
import difflib
from collections import Counter
from html import escape

# A large, dependency-free rewriting engine. It cannot check the internet, but it does
# force real wording and structure changes instead of copying the input.

PROTECTED_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "have", "in", "is", "it", "its",
    "of", "on", "or", "that", "the", "this", "to", "was", "were", "with", "without", "your", "you", "we", "i"
}

PHRASE_BANK = {
    r"\ball[- ]?in[- ]?one\b": ["complete", "multi-purpose", "integrated"],
    r"\bhigh quality\b": ["premium", "well-made", "professional-grade"],
    r"\btop quality\b": ["premium-grade", "carefully crafted", "well-built"],
    r"\bbest quality\b": ["premium standard", "excellent standard", "refined quality"],
    r"\bcomplete full face palette\b": ["complete complexion palette", "full-face makeup collection", "all-in-one face kit"],
    r"\bfull face palette\b": ["complexion palette", "face-and-eye kit", "makeup palette"],
    r"\bmakeup palette\b": ["cosmetic palette", "beauty palette", "makeup kit"],
    r"\btravel[- ]?friendly\b": ["easy to carry", "portable", "made for travel"],
    r"\bmature skin\b": ["grown-up complexions", "mature complexions", "adult skin"],
    r"\bcoverage for\b": ["coverage suited to", "coverage made for", "a finish designed for"],
    r"\bdesigned to\b": ["created to", "built to", "developed to"],
    r"\bhelps to\b": ["supports", "helps", "makes it easier to"],
    r"\bis used to\b": ["is commonly used to", "helps users", "is useful for"],
    r"\bcan be used to\b": ["can help", "is useful for", "can support"],
    r"\bimportant for\b": ["valuable for", "essential for", "useful in"],
    r"\bplays an important role\b": ["has a major role", "contributes strongly", "is highly important"],
    r"\bin order to\b": ["to", "so users can", "for the purpose of"],
    r"\bdue to the fact that\b": ["because", "since", "as"],
    r"\bas a result\b": ["therefore", "because of this", "for that reason"],
    r"\bon the other hand\b": ["in contrast", "however", "from another angle"],
    r"\bin conclusion\b": ["overall", "to summarize", "in the final analysis"],
    r"\bmore and more\b": ["increasingly", "steadily more", "with growing frequency"],
    r"\bvery important\b": ["crucial", "highly significant", "essential"],
    r"\bvery good\b": ["excellent", "strong", "impressive"],
    r"\bproper\b": ["well-structured", "appropriate", "polished"],
    r"\baccording to\b": ["based on", "in line with", "following"],
    r"\beach and everything\b": ["every detail", "the complete process", "all key elements"],
    r"\bcopy[- ]?paste\b": ["direct duplication", "unchanged repetition", "verbatim copying"],
    r"\bplagiarism[- ]?free\b": ["more original", "rewritten for originality", "low-overlap"],
    r"\bai generated\b": ["machine-written", "automated-sounding", "AI-style"],
    r"\bblack racism\b": ["racially harmful wording", "biased language", "discriminatory phrasing"],
}

SYNONYMS = {
    "complete": ["comprehensive", "full", "all-inclusive"],
    "full": ["complete", "entire", "whole"],
    "face": ["complexion", "facial", "beauty"],
    "palette": ["kit", "collection", "set"],
    "medium": ["mid-tone", "balanced", "moderate"],
    "makeup": ["cosmetics", "beauty", "cosmetic"],
    "foundation": ["base powder", "complexion base", "skin base"],
    "foundations": ["base powders", "complexion bases", "skin-base shades"],
    "blush": ["cheek colour", "cheek tint", "rosy shade"],
    "bronzer": ["warming powder", "sun-kissed powder", "bronzing shade"],
    "highlighter": ["glow enhancer", "radiance powder", "illuminator"],
    "eyeshadows": ["eye shades", "lid colours", "eye colours"],
    "coverage": ["finish", "concealing effect", "skin-evening result"],
    "travel": ["portable", "on-the-go", "trip-ready"],
    "friendly": ["convenient", "suitable", "easy-to-use"],
    "professional": ["polished", "expert-level", "business-ready"],
    "quality": ["standard", "finish", "craftsmanship"],
    "important": ["essential", "valuable", "significant"],
    "good": ["strong", "effective", "useful"],
    "best": ["top", "leading", "premium"],
    "create": ["produce", "build", "generate"],
    "make": ["create", "develop", "produce"],
    "making": ["creating", "building", "developing"],
    "use": ["utilize", "apply", "work with"],
    "using": ["applying", "working with", "utilizing"],
    "help": ["support", "assist", "make it easier"],
    "helps": ["supports", "helps", "makes it easier for"],
    "improve": ["enhance", "refine", "strengthen"],
    "improved": ["enhanced", "refined", "upgraded"],
    "remove": ["reduce", "clean", "eliminate"],
    "removing": ["reducing", "cleaning", "eliminating"],
    "replace": ["substitute", "change", "swap"],
    "text": ["content", "writing", "copy"],
    "content": ["material", "copy", "writing"],
    "website": ["web platform", "site", "online tool"],
    "tool": ["utility", "feature", "module"],
    "tools": ["utilities", "features", "modules"],
    "simple": ["clear", "straightforward", "easy"],
    "fast": ["quick", "rapid", "speedy"],
    "advanced": ["enhanced", "powerful", "sophisticated"],
    "algorithm": ["rule-based engine", "processing logic", "rewriting logic"],
    "backend": ["server side", "server engine", "application core"],
    "functionality": ["features", "working flow", "capability"],
    "functional": ["working", "usable", "operational"],
    "properly": ["correctly", "smoothly", "accurately"],
    "accurate": ["precise", "correct", "reliable"],
    "industry": ["professional", "commercial", "production"],
    "user": ["client", "visitor", "customer"],
    "users": ["clients", "visitors", "customers"],
    "sell": ["market", "offer", "commercialize"],
    "upload": ["add", "submit", "import"],
    "download": ["export", "save", "retrieve"],
    "login": ["sign in", "access", "authenticate"],
    "signup": ["register", "create an account", "join"],
    "grammar": ["language accuracy", "sentence correctness", "writing mechanics"],
    "punctuation": ["sentence marks", "writing punctuation", "text punctuation"],
    "summary": ["brief version", "condensed version", "short overview"],
    "convert": ["transform", "change", "turn"],
    "write": ["compose", "draft", "prepare"],
    "readable": ["clear", "easy to read", "smooth"],
    "beautiful": ["elegant", "polished", "attractive"],
    "modern": ["current", "fresh", "contemporary"],
    "safe": ["responsible", "careful", "reliable"],
    "bias": ["unfair language", "one-sided wording", "harmful phrasing"],
}

TONE_PHRASES = {
    "academic": {
        "start": ["The material can be reframed as follows:", "A clearer academic version is:", "In a more formal structure:"],
        "connectors": ["Furthermore", "In addition", "Consequently", "This indicates that"]
    },
    "professional": {
        "start": ["Here is a polished version:", "A more professional rewrite is:", "This can be expressed more clearly as:"],
        "connectors": ["Additionally", "As a result", "This helps", "The result is"]
    },
    "simple": {
        "start": ["In simple words:", "A clearer version is:", "This means:"],
        "connectors": ["Also", "So", "This helps", "Because of this"]
    },
    "creative": {
        "start": ["A fresher version is:", "A more engaging rewrite is:", "The idea can be presented like this:"],
        "connectors": ["Beyond that", "This creates", "At the same time", "Together"]
    },
    "ecommerce": {
        "start": ["A stronger product-style rewrite is:", "A polished product description is:", "The product can be presented as:"],
        "connectors": ["It also", "Designed for everyday use", "This makes it", "The result"]
    }
}

BIASED_REPLACEMENTS = {
    r"\bblacklist\b": "blocklist",
    r"\bwhitelist\b": "allowlist",
    r"\bmaster\b": "primary",
    r"\bslave\b": "secondary",
    r"\bcrazy\b": "unusual",
    r"\binsane\b": "extreme",
    r"\blame\b": "limited mobility",
    r"\bhandicapped\b": "disabled",
    r"\billegal immigrant\b": "undocumented immigrant",
    r"\bnormal people\b": "people without that condition",
    r"\bblack racism\b": "racially harmful wording",
}

AI_STYLE_REPLACEMENTS = {
    r"\bin today'?s digital (world|age|era)\b": "nowadays",
    r"\bleverage\b": "use",
    r"\butilize\b": "use",
    r"\brobust\b": "strong",
    r"\bseamless\b": "smooth",
    r"\bcutting-edge\b": "modern",
    r"\bgame-changing\b": "high-impact",
    r"\bunleash\b": "use",
    r"\bdelve into\b": "explore",
    r"\btapestry\b": "mix",
    r"\bnavigate the complexities\b": "handle",
    r"\belevate\b": "improve",
    r"\bempower\b": "help",
    r"\btransformative\b": "useful",
    r"\bfurthermore\b": "also",
    r"\bmoreover\b": "also",
    r"\bin conclusion\b": "overall",
}


def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def split_sentences(text: str):
    # Keeps punctuation attached while splitting. Also handles bullets and product separators.
    text = normalize_text(text)
    if not text:
        return []
    chunks = []
    for block in re.split(r"\n+", text):
        block = block.strip()
        if not block:
            continue
        parts = re.split(r"(?<=[.!?])\s+|\s+[|•]+\s+|\s+-\s+", block)
        for part in parts:
            p = part.strip(" \t|•-")
            if p:
                chunks.append(p)
    return chunks


def preserve_case(original: str, replacement: str) -> str:
    if original.isupper():
        return replacement.upper()
    if original[:1].isupper():
        return replacement[:1].upper() + replacement[1:]
    return replacement


def choose(options, seed_val):
    if not options:
        return ""
    return options[seed_val % len(options)]


def apply_phrase_replacements(text: str, intensity: int = 2) -> str:
    out = text
    for idx, (pattern, repls) in enumerate(PHRASE_BANK.items()):
        def _sub(match):
            selected = choose(repls, len(match.group(0)) + idx + intensity)
            return preserve_case(match.group(0), selected)
        out = re.sub(pattern, _sub, out, flags=re.IGNORECASE)
    return out


def apply_synonyms(text: str, intensity: int = 2) -> str:
    # Replace many content words while protecting very short/common words and all-caps acronyms.
    def repl(match):
        word = match.group(0)
        base = word.lower()
        if base in PROTECTED_WORDS or len(base) <= 3 or word.isupper():
            return word
        if base in SYNONYMS:
            options = SYNONYMS[base]
            selected = choose(options, len(word) + intensity)
            return preserve_case(word, selected)
        # productive suffix-level transformations
        if base.endswith("tion") and len(base) > 7:
            return word
        return word
    return re.sub(r"\b[A-Za-z][A-Za-z'-]*\b", repl, text)



def lower_first_safe(value: str) -> str:
    if not value:
        return value
    # Do not damage brand/acronym starts like LAURA, NASA, AI, API.
    if len(value) > 1 and value[0].isupper() and value[1].isupper():
        return value
    return value[0].lower() + value[1:]


def is_listing_text(text: str) -> bool:
    lowered = text.lower()
    separators = text.count('|') + text.count(';') + text.count('•')
    product_words = ['palette', 'makeup', 'product', 'kit', 'collection', 'foundation', 'blush', 'bronzer', 'highlighter', 'eyeshadow', 'travel-friendly']
    return separators >= 2 or (len(text.split()) <= 70 and sum(w in lowered for w in product_words) >= 3)


def rewrite_listing_text(text: str) -> str:
    raw = normalize_text(text)
    pieces = [p.strip(' ,.|-•') for p in re.split(r"\s*[|,;\n]\s*", raw) if p.strip(' ,.|-•')]
    if len(pieces) < 3:
        return ''
    title = pieces[0]
    title2 = apply_phrase_replacements(title, 5)
    title2 = apply_synonyms(title2, 5)
    features = [apply_synonyms(apply_phrase_replacements(x, 5), 5) for x in pieces[1:]]
    feature_text = ', '.join(features[:-1]) + f", and {features[-1]}" if len(features) > 1 else features[0]
    return clean_punctuation(
        f"{title2} is a polished, customer-ready collection created for a complete and convenient routine. "
        f"The set brings together {feature_text}, giving the description a clearer structure and a more refined selling style. "
        f"Its portable format makes the product easier to present for everyday use, gifting, and travel."
    )

def clean_punctuation(text: str) -> str:
    text = re.sub(r"\bthat This\b", "that this", text)
    text = re.sub(r"\bassists visitors eliminate plagiarism\b", "helps visitors reduce text overlap", text, flags=re.IGNORECASE)
    text = re.sub(r"\bassists users eliminate plagiarism\b", "helps users reduce text overlap", text, flags=re.IGNORECASE)
    text = re.sub(r"\bmaterial standard\b", "content quality", text, flags=re.IGNORECASE)
    text = re.sub(r"\bcopy finish\b", "content quality", text, flags=re.IGNORECASE)
    text = re.sub(r"\bmakes it easier for (visitors|users|clients) eliminate plagiarism\b", r"makes it easier for \1 to reduce text overlap", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)
    text = re.sub(r"([,.!?;:])([A-Za-z])", r"\1 \2", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"\.{2,}", ".", text)
    text = re.sub(r"\s+\n", "\n", text)
    return text.strip()


def restructure_sentence(sentence: str, tone: str = "professional", intensity: int = 2) -> str:
    s = sentence.strip()
    if not s:
        return s
    original_end = "." if not re.search(r"[.!?]$", s) else ""
    s = re.sub(r"^[\-*•\d.)\s]+", "", s).strip()

    # Product-title patterns: convert fragments into a real description.
    if ("|" in sentence or "," in sentence) and len(s.split()) <= 45:
        items = [p.strip(" ,.|-•") for p in re.split(r"\s*[|,;]\s*", s) if p.strip(" ,.|-•")]
        if len(items) >= 3:
            title = items[0]
            features = items[1:]
            result = f"{title} is presented as a polished {choose(['beauty collection', 'professional kit', 'cosmetic set'], len(title))} featuring {', '.join(features[:-1])}, and {features[-1]}. It is arranged for a cleaner routine, smoother use, and a more refined final look."
            return clean_punctuation(result)

    # Common template-based sentence transformations.
    templates = [
        (r"^(.+?) is (.+?)\.$", ["{a} can be described as {b}.", "In practical terms, {a} works as {b}.", "A clearer description is that {a} is {b}."]),
        (r"^(.+?) are (.+?)\.$", ["{a} can be presented as {b}.", "In a clearer form, {a} work as {b}.", "A clearer description is that {a} are {b}."]),
        (r"^(.+?) helps (.+?)\.$", ["{a} supports {b}.", "With {a}, users can {b} more smoothly.", "{a} makes it easier to {b}."]),
        (r"^(.+?) can (.+?)\.$", ["{a} is able to {b}.", "Users can rely on {a} to {b}.", "{a} may be used to {b}."]),
        (r"^(.+?) provides (.+?)\.$", ["{a} offers {b}.", "With {a}, users receive {b}.", "{a} is built to deliver {b}."]),
    ]
    for pattern, options in templates:
        m = re.match(pattern, s, flags=re.IGNORECASE)
        if m:
            selected = choose(options, len(s) + intensity)
            return clean_punctuation(selected.format(a=m.group(1).strip(), b=m.group(2).strip()))

    words = s.split()
    # Clause swapping for long sentences.
    if len(words) > 18 and "," in s:
        parts = [p.strip() for p in s.split(",") if p.strip()]
        if len(parts) >= 2:
            first = parts[0]
            rest = ", ".join(parts[1:])
            return clean_punctuation(f"{rest.capitalize()}, while {lower_first_safe(first)}.")
    if len(words) > 16:
        mid = len(words) // 2
        left = " ".join(words[:mid]).strip(" ,.;:")
        right = " ".join(words[mid:]).strip(" ,.;:")
        connector = choose(TONE_PHRASES.get(tone, TONE_PHRASES["professional"])["connectors"], len(s) + intensity)
        return clean_punctuation(f"{left}. {connector}, {right}.")

    starters = {
        "academic": ["This can be framed as", "A formal version states that", "The idea suggests that"],
        "professional": ["A polished version is", "This can be rewritten as", "A clearer version says"],
        "simple": ["Simply put", "In clear words", "This means"],
        "creative": ["A fresher way to say it is", "This idea can sound more engaging as", "A more vivid version is"],
        "ecommerce": ["For product copy", "A cleaner product line is", "A stronger listing phrase is"],
    }
    starter = choose(starters.get(tone, starters["professional"]), len(s) + intensity)
    # Avoid ugly prefix for very short labels; add context instead.
    if len(words) < 6:
        return clean_punctuation(f"{starter}: {lower_first_safe(s)}{original_end}")
    return clean_punctuation(f"{starter} that {lower_first_safe(s)}{original_end}")


def force_difference(original: str, rewritten: str, tone: str, intensity: int) -> str:
    sim = similarity_ratio(original, rewritten)
    if sim < 0.72 and normalize_text(original).lower() != normalize_text(rewritten).lower():
        return rewritten
    # Stronger fallback: split into ideas and rebuild as bullet/paragraph hybrid.
    pieces = split_sentences(original)
    if not pieces:
        return rewritten
    transformed = []
    for i, p in enumerate(pieces):
        p = apply_phrase_replacements(p, intensity + 2)
        p = apply_synonyms(p, intensity + 3)
        p = restructure_sentence(p, tone, intensity + 3)
        transformed.append(p)
    result = " ".join(transformed)
    if similarity_ratio(original, result) > 0.85:
        result = " ".join([f"{choose(['In a refreshed form', 'Rewritten clearly', 'A more original version'], i)}: {lower_first_safe(x) if x else x}" for i, x in enumerate(transformed)])
    return clean_punctuation(result)


def algorithm_rewrite(text: str, tone: str = "professional", strength: str = "maximum") -> str:
    text = normalize_text(text)
    if not text:
        return ""
    strength_map = {"light": 1, "balanced": 2, "strong": 3, "maximum": 5}
    intensity = strength_map.get(strength, 5)

    if is_listing_text(text):
        listed = rewrite_listing_text(text)
        if listed:
            return force_difference(text, listed, tone, intensity)

    sentences = split_sentences(text)
    if not sentences:
        sentences = [text]

    rewritten = []
    for idx, sent in enumerate(sentences):
        s = apply_phrase_replacements(sent, intensity)
        # Multiple synonym passes for strong/max modes.
        passes = 1 if intensity <= 2 else 2 if intensity == 3 else 3
        for _ in range(passes):
            s = apply_synonyms(s, intensity + idx)
        s = restructure_sentence(s, tone, intensity + idx)
        s = apply_phrase_replacements(s, intensity + 1)
        s = apply_synonyms(s, intensity + 1)
        rewritten.append(clean_punctuation(s))

    joined = " ".join([x for x in rewritten if x])
    joined = clean_punctuation(joined)
    joined = force_difference(text, joined, tone, intensity)
    return clean_punctuation(joined)


def ai_style_cleaner(text: str) -> str:
    out = normalize_text(text)
    for pattern, repl in AI_STYLE_REPLACEMENTS.items():
        out = re.sub(pattern, repl, out, flags=re.IGNORECASE)
    out = algorithm_rewrite(out, tone="professional", strength="balanced")
    return out


def bias_cleaner(text: str) -> str:
    out = normalize_text(text)
    for pattern, repl in BIASED_REPLACEMENTS.items():
        out = re.sub(pattern, repl, out, flags=re.IGNORECASE)
    return clean_punctuation(out)


def grammar_polish(text: str) -> str:
    out = normalize_text(text)
    replacements = {
        r"\bi\b": "I",
        r"\bdont\b": "do not",
        r"\bdoesnt\b": "does not",
        r"\bcant\b": "cannot",
        r"\bwont\b": "will not",
        r"\bisnt\b": "is not",
        r"\barent\b": "are not",
        r"\bim\b": "I am",
        r"\bits\b": "its",
        r"\balot\b": "a lot",
        r"\brecieve\b": "receive",
        r"\bseperate\b": "separate",
        r"\bdefinately\b": "definitely",
        r"\boccured\b": "occurred",
        r"\bteh\b": "the",
    }
    for pat, rep in replacements.items():
        out = re.sub(pat, rep, out, flags=re.IGNORECASE)
    # Capitalize sentence starts.
    parts = re.split(r"(?<=[.!?])\s+", out)
    polished = []
    for p in parts:
        p = p.strip()
        if p:
            p = p[0].upper() + p[1:]
            if not re.search(r"[.!?]$", p):
                p += "."
            polished.append(p)
    return clean_punctuation(" ".join(polished))


def summarize_text(text: str, max_sentences: int = 3) -> str:
    sentences = split_sentences(text)
    if not sentences:
        return ""
    words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
    freq = Counter(w for w in words if w not in PROTECTED_WORDS)
    scored = []
    for s in sentences:
        score = sum(freq.get(w.lower(), 0) for w in re.findall(r"\b[a-zA-Z]{4,}\b", s)) / max(1, len(s.split()))
        scored.append((score, s))
    top = [s for _, s in sorted(scored, reverse=True)[:max_sentences]]
    return grammar_polish(" ".join(top))


def expand_text(text: str, tone: str = "professional") -> str:
    base = algorithm_rewrite(text, tone=tone, strength="balanced")
    add = {
        "professional": "This version improves clarity by presenting the core point in a more structured and reader-friendly way.",
        "academic": "This framing also improves logical flow by connecting the main idea with clearer explanatory language.",
        "simple": "It is easier to understand because the idea is broken into clear parts.",
        "creative": "The wording also feels more engaging because it gives the idea a smoother rhythm and stronger expression.",
        "ecommerce": "This makes the description more useful for customers who want to quickly understand the product value."
    }
    return clean_punctuation(f"{base} {add.get(tone, add['professional'])}")


def product_rewrite(text: str) -> str:
    raw = normalize_text(text)
    listed = rewrite_listing_text(raw)
    if listed:
        return force_difference(raw, listed, "ecommerce", 5)
    return algorithm_rewrite(raw, tone="ecommerce", strength="maximum")


def bullet_generator(text: str) -> str:
    sentences = split_sentences(algorithm_rewrite(text, tone="professional", strength="balanced"))
    if not sentences:
        return ""
    bullets = []
    for s in sentences[:7]:
        bullets.append("• " + s.rstrip("."))
    return "\n".join(bullets)


def title_generator(text: str) -> str:
    text = normalize_text(text)
    words = [w for w in re.findall(r"\b[A-Za-z][A-Za-z'-]*\b", text) if w.lower() not in PROTECTED_WORDS]
    if not words:
        return "Improved Content Title"
    key = " ".join(words[:8])
    variants = [
        f"Professional {key.title()} Solution",
        f"Smart Guide to {key.title()}",
        f"Clear and Polished {key.title()} Overview",
        f"Modern {key.title()} Toolkit",
        f"Complete {key.title()} Resource",
    ]
    return "\n".join(variants)


def keyword_extractor(text: str, limit: int = 15) -> str:
    words = [w.lower() for w in re.findall(r"\b[A-Za-z][A-Za-z'-]{3,}\b", text) if w.lower() not in PROTECTED_WORDS]
    counts = Counter(words)
    return ", ".join([w for w, _ in counts.most_common(limit)])


def normalize_for_compare(text: str):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", " ", text.lower())).strip()


def similarity_ratio(a: str, b: str) -> float:
    na, nb = normalize_for_compare(a), normalize_for_compare(b)
    if not na and not nb:
        return 1.0
    if not na or not nb:
        return 0.0
    return difflib.SequenceMatcher(None, na, nb).ratio()


def ngram_overlap(a: str, b: str, n: int = 4) -> float:
    def grams(t):
        words = normalize_for_compare(t).split()
        return set(tuple(words[i:i+n]) for i in range(len(words)-n+1))
    ga, gb = grams(a), grams(b)
    if not ga:
        return 0.0
    return len(ga & gb) / max(1, len(ga))


def readability_score(text: str) -> int:
    sentences = max(1, len(split_sentences(text)))
    words = re.findall(r"\b\w+\b", text)
    syllables = 0
    for word in words:
        w = word.lower()
        groups = re.findall(r"[aeiouy]+", w)
        syllables += max(1, len(groups))
    if not words:
        return 0
    # Flesch approximation mapped to 0-100.
    score = 206.835 - 1.015 * (len(words) / sentences) - 84.6 * (syllables / len(words))
    return int(max(0, min(100, round(score))))


def metrics(original: str, output: str) -> dict:
    sim = similarity_ratio(original, output)
    overlap = ngram_overlap(original, output, n=4)
    return {
        "similarity": round(sim * 100, 1),
        "originality_lift": round(max(0, (1 - sim)) * 100, 1),
        "phrase_overlap": round(overlap * 100, 1),
        "readability": readability_score(output),
        "input_words": len(re.findall(r"\b\w+\b", original)),
        "output_words": len(re.findall(r"\b\w+\b", output)),
    }


def process_tool(tool: str, text: str, tone: str = "professional", strength: str = "maximum") -> str:
    tool = (tool or "algorithm_rewriter").lower()
    if tool == "algorithm_rewriter":
        return algorithm_rewrite(text, tone=tone, strength=strength)
    if tool == "ai_style_cleaner":
        return ai_style_cleaner(text)
    if tool == "grammar_polish":
        return grammar_polish(text)
    if tool == "bias_cleaner":
        return bias_cleaner(text)
    if tool == "summarizer":
        return summarize_text(text)
    if tool == "expander":
        return expand_text(text, tone=tone)
    if tool == "product_rewriter":
        return product_rewrite(text)
    if tool == "bullet_generator":
        return bullet_generator(text)
    if tool == "title_generator":
        return title_generator(text)
    if tool == "keyword_extractor":
        return keyword_extractor(text)
    return algorithm_rewrite(text, tone=tone, strength=strength)
