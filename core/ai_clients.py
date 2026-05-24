import os
import requests
from .rewrite_engine import algorithm_rewrite, similarity_ratio, clean_punctuation

AI_REWRITE_PROMPT = """
You are Originality Studio Pro, a professional rewriting and text-improvement engine.

Your task: rewrite the user's text from scratch while preserving the factual meaning.

Rules:
1. Do not copy the original wording, sentence structure, or phrase order.
2. Rewrite every sentence naturally using different vocabulary and different structure.
3. Keep product names, brand names, numbers, and technical terms only when necessary.
4. Do not invent facts, claims, prices, certifications, citations, or guarantees.
5. Improve grammar, punctuation, clarity, and flow.
6. Remove repetitive wording, robotic phrasing, awkward AI-style wording, and biased/discriminatory phrasing.
7. Avoid keeping any 5+ word sequence from the input unless it is a proper noun, title, or required legal/technical phrase.
8. If the input is a product listing, turn it into polished product copy.
9. If the input is academic, make it formal, clear, and citation-friendly without pretending sources exist.
10. Return only the rewritten text. Do not explain the changes.
""".strip()


def get_config(user_settings=None):
    user_settings = user_settings or {}
    provider = (user_settings.get("provider") or os.getenv("DEFAULT_AI_PROVIDER") or "gemini").lower()
    model = user_settings.get("model") or os.getenv("GEMINI_MODEL" if provider == "gemini" else "OPENAI_MODEL")
    api_key = user_settings.get("api_key") or os.getenv("GEMINI_API_KEY" if provider == "gemini" else "OPENAI_API_KEY")
    return provider, model, api_key


def rewrite_with_ai(text, tone="professional", strength="maximum", user_settings=None):
    provider, model, api_key = get_config(user_settings)
    if not api_key:
        fallback = algorithm_rewrite(text, tone=tone, strength=strength)
        return fallback, "Algorithm fallback used because no API key is saved."

    instruction = (
        AI_REWRITE_PROMPT +
        f"\n\nTone: {tone}. Rewrite strength: {strength}. "
        "Use a complete rewrite, not a small synonym swap."
    )
    try:
        if provider == "openai":
            output = call_openai(api_key, model or "gpt-4o-mini", instruction, text)
        else:
            output = call_gemini(api_key, model or "gemini-1.5-flash", instruction, text)
        output = clean_punctuation(output)
        # If the model lazily copies, force local rewrite as a safety fallback.
        if not output or similarity_ratio(text, output) > 0.86 or output.strip().lower() == text.strip().lower():
            output = algorithm_rewrite(text, tone=tone, strength="maximum")
            return output, "AI response was too similar, so the stronger algorithm fallback was used."
        return output, "AI rewrite completed."
    except Exception as exc:
        fallback = algorithm_rewrite(text, tone=tone, strength="maximum")
        return fallback, f"AI request failed, algorithm fallback used: {str(exc)[:160]}"


def call_gemini(api_key, model, instruction, text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": instruction + "\n\nINPUT TEXT:\n" + text}
                ],
            }
        ],
        "generationConfig": {
            "temperature": 0.85,
            "topP": 0.9,
            "maxOutputTokens": 4096,
        },
    }
    res = requests.post(url, json=payload, timeout=35)
    res.raise_for_status()
    data = res.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]


def call_openai(api_key, model, instruction, text):
    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": instruction},
            {"role": "user", "content": text},
        ],
        "temperature": 0.85,
        "max_tokens": 4096,
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    res = requests.post(url, headers=headers, json=payload, timeout=35)
    res.raise_for_status()
    data = res.json()
    return data["choices"][0]["message"]["content"]
