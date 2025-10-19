import re
from typing import Optional

AMOUNT_RE   = re.compile(r"(?:₦|NGN)?\s*([0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{1,2})?|[0-9]+(?:\.[0-9]{1,2})?)")
ACCOUNT_RE  = re.compile(r"\b\d{10}\b")
YES_TOKENS  = {"yes","y","yeah","yep","ok","okay","sure","confirm"}
NO_TOKENS   = {"no","n","nope","cancel","stop","abort"}

def parse_amount(text_en: str) -> Optional[str]:
    m = AMOUNT_RE.search(text_en)
    if not m: return None
    val = m.group(1).replace(",","")
    return val  # keep as string; your API can parse decimal

def parse_account(text_en: str) -> Optional[str]:
    m = ACCOUNT_RE.search(text_en)
    return m.group(0) if m else None

def detect_intent(text_en: str) -> Optional[str]:
    tl = text_en.lower()
    if any(x in tl for x in ["balance","how much do i have","check my account","account balance"]):
        return "BALANCE"
    if any(x in tl for x in ["transfer","send money","send to","pay "]) or (parse_amount(tl) and parse_account(tl)):
        return "TRANSFER"
    return None