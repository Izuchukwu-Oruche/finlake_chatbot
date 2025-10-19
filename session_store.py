import time
from typing import Any, Dict
from config import ddb


def now_ttl(seconds=1800):  # 30 minutes
    return int(time.time()) + seconds

def get_session(user_id: str) -> Dict[str, Any]:
    resp = ddb.get_item(Key={"user_id": user_id})
    return resp.get("Item") or {"user_id": user_id, "intent": None, "slots": {}, "lang": None, "ttl": now_ttl()}

def save_session(sess: Dict[str, Any]):
    sess["ttl"] = now_ttl()
    ddb.put_item(Item=sess)

def clear_session(user_id: str):
    try: ddb.delete_item(Key={"user_id": user_id})
    except Exception as e: print("DDB delete error:", e)