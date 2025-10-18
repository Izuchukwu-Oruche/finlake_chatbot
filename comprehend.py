from config import DEFAULT_FALLBACK_LANG, HAUSA_DIAC, YORUBA_DIAC, IGBO_DIAC, comprehend
from helper import has_any, likely_pidgin


def detect_language(text: str) -> str:
    """
    Returns ISO-ish short code: 'en', 'ha', 'yo', 'ig', 'pcm' (pidgin), or fallback 'en'.
    We try Comprehend first; if score is low/unsupported, use heuristics.
    """
    text = (text or "").strip()
    if not text:
        return DEFAULT_FALLBACK_LANG

    # Heuristic fast-paths for scripts/diacritics
    if has_any(text, HAUSA_DIAC):
        return "ha"
    if has_any(text, YORUBA_DIAC):
        return "yo"
    if has_any(text, IGBO_DIAC):
        return "ig"
    if likely_pidgin(text):
        return "pcm"

    # Comprehend detection
    try:
        resp = comprehend.detect_dominant_language(Text=text)
        langs = resp.get("Languages", [])
        if not langs:
            return DEFAULT_FALLBACK_LANG
        top = max(langs, key=lambda l: l.get("Score", 0))
        code = top.get("LanguageCode", "en").lower()
        if code in ("en", "ha"):
            return code
        return code
    except Exception as e:
        print("Comprehend error:", e)
        return DEFAULT_FALLBACK_LANG