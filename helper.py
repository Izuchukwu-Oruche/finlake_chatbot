from config import PIDGIN_TOKENS, PROMPTS
from translate import translate_from_en



def has_any(text: str, charset: set) -> bool:
    return any(ch in charset for ch in text.lower())

def likely_pidgin(text: str) -> bool:
    tl = text.lower()
    hits = sum(1 for tok in PIDGIN_TOKENS if tok in tl)
    return hits >= 2

def localize(key: str, lang: str, **kwargs) -> str:
    base = PROMPTS.get(lang) or PROMPTS["en"]
    s = base.get(key) or PROMPTS["en"].get(key, "")
    try:
        s = s.format(**kwargs)
    except Exception:
        pass
    # Push through Translate for Hausa to make phrasing more natural if we used EN defaults
    if lang=="ha" and PROMPTS.get("ha") is None:
        s = translate_from_en(s, "ha")
    return s
