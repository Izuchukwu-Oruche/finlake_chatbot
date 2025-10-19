from config import SUPPORTED_TRANSLATE_BIDI
from config import translate

def translate_to_en(text: str, src_lang: str) -> str:
    if not text or src_lang == "en":
        return text
    if src_lang in SUPPORTED_TRANSLATE_BIDI:
        try:
            out = translate.translate_text(
                Text=text,
                SourceLanguageCode=src_lang,
                TargetLanguageCode="en"
            )
            return out.get("TranslatedText", text)
        except Exception as e:
            print("Translate->EN error:", e)
            return text


def translate_from_en(text: str, tgt_lang: str) -> str:
    if not text or tgt_lang == "en":
        return text
    if tgt_lang in SUPPORTED_TRANSLATE_BIDI:
        try:
            out = translate.translate_text(
                Text=text,
                SourceLanguageCode="en",
                TargetLanguageCode=tgt_lang
            )
            return out.get("TranslatedText", text)
        except Exception as e:
            print("Translate EN-> error:", e)
            return text

    # Light fallbacks for pcm/yo/ig
    if tgt_lang == "pcm": return text.replace("You said:", "You talk say:").replace("How much", "How much").replace("Please", "Abeg")
    if tgt_lang == "yo":  return text  # we mostly use PROMPTS[yo] directly
    if tgt_lang == "ig":  return text
    return text