from config import PIDGIN_TOKENS



def has_any(text: str, charset: set) -> bool:
    return any(ch in charset for ch in text.lower())

def likely_pidgin(text: str) -> bool:
    tl = text.lower()
    hits = sum(1 for tok in PIDGIN_TOKENS if tok in tl)
    return hits >= 2

def localize_ack(src_lang: str) -> str:
    if src_lang == "en": return "Got it. You said: "
    if src_lang == "ha": return "Na karɓa. Ka ce: "
    if src_lang == "pcm": return "I don hear you. You talk say: "
    if src_lang == "yo": return "Mo ti gba. O sọ pé: "
    if src_lang == "ig": return "Enwetara m. I kwuru na: "
    return "Got it. You said: "
