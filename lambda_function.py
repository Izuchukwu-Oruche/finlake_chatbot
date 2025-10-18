import json
from config import VERIFY_TOKEN

from http_utils import ok, extract_user_text




def lambda_handler(event, context):
    # —— HTTP API (v2.0) method (not httpMethod) ——
    method = (event.get("requestContext", {}).get("http", {}).get("method") or "").upper()

    # 1) Verification handshake (GET)
    if method == "GET":
        params = event.get("queryStringParameters") or {}
        mode = params.get("hub.mode")
        verify_token = params.get("hub.verify_token")
        challenge = params.get("hub.challenge", "")

        if mode == "subscribe" and verify_token == VERIFY_TOKEN:
            return ok(challenge, 200)
        return ok("Forbidden", 403)

    # 2) Incoming messages (POST)
    if method == "POST":
        try:
            body = json.loads(event.get("body") or "{}")
            for entry in body.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    for msg in value.get("messages", []):
                        from_id = msg.get("from")
                        user_text = extract_user_text(msg)
                        if not (from_id and user_text):
                            continue

                        # Detect language
                        lang = detect_language(user_text)

                        # Normalize to EN for downstream logic
                        user_text_en = translate_to_en(user_text, lang)

                        # Compose a simple localized acknowledgment
                        preface = localize_ack(lang)
                        reply_en = f"Got it. You said: {user_text_en}"

                        # Translate back to user's language (where supported)
                        if lang == "en":
                            final_reply = reply_en
                        else:
                            translated_content = translate_from_en(
                                f"You said: {user_text_en}", lang
                            )
                            if translated_content and translated_content != f"You said: {user_text_en}":
                                final_reply = translated_content
                            else:
                                final_reply = f"{preface}{user_text}"

                        _send_whatsapp_text(from_id, final_reply)

            return _ok("EVENT_RECEIVED", 200)
        except Exception as e:
            # Any prints show up in CloudWatch Logs automatically
            print("Error:", e)
            return _ok("EVENT_RECEIVED", 200)

    return _ok("Method Not Allowed", 405)
