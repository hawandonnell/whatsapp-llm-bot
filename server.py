import os
import requests
from fastapi import FastAPI, Request, Query
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

GRAPH_API_TOKEN = os.getenv("GRAPH_API_TOKEN")

@app.post("/webhook")
async def webhook_post_handler(request: Request):
    data = await request.json()
    print("Incoming webhook message:", data)

    # Extract message from payload
    entry = data.get("entry", [{}])[0]
    changes = entry.get("changes", [{}])[0]
    value = changes.get("value", {})
    message = value.get("messages", [{}])[0] if value.get("messages") else None

    if message and message.get("type") == "text":
        business_phone_number_id = value.get("metadata", {}).get("phone_number_id")
        if business_phone_number_id:
            # Send a reply message
            reply_url = f"https://graph.facebook.com/v22.0/{business_phone_number_id}/messages"
            headers = {
                "Authorization": f"Bearer {GRAPH_API_TOKEN}",
                "Content-Type": "application/json"
            }
            reply_data = {
                "messaging_product": "whatsapp",
                "to": message.get("from"),
                "text": {"body": "Echo: " + message.get("text", {}).get("body", "")},
                "context": {
                    "message_id": message.get("id")
                }
            }
            requests.post(reply_url, headers=headers, json=reply_data)

            # Mark incoming message as read
            read_data = {
                "messaging_product": "whatsapp",
                "status": "read",
                "message_id": message.get("id")
            }
            requests.post(reply_url, headers=headers, json=read_data)

    return JSONResponse(content={"status": "ok"}, status_code=200)

@app.get("/webhook")
def webhook_get_handler(
    token: str = Query(None, alias="hub.verify_token"),
    challenge: str = Query(None, alias="hub.challenge")
):
    if os.getenv('VERIFY_TOKEN') == token:
        return JSONResponse(content=int(challenge), status_code=200)
    else:
        return JSONResponse(content="Verification failed", status_code=403)
