def ok(body="OK", status=200, content_type="text/plain"):
    return {"statusCode": status, "headers": {"Content-Type": content_type}, "body": body}

def extract_user_text(msg: dict) -> Optional[str]:
    # Text message
    if "text" in msg and "body" in msg["text"]:
        return msg["text"]["body"]
    # Interactive replies
    if msg.get("type") == "interactive":
        i = msg.get("interactive") or {}
        if "button_reply" in i:
            return i["button_reply"].get("title") or i["button_reply"].get("id")
        if "list_reply" in i:
            return i["list_reply"].get("title") or i["list_reply"].get("id")
    return None