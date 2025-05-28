import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.post("/webhook")
def webhook_handler(request: dict):
    return JSONResponse(content=request, status_code=200)

@app.get("/webhook")
def webhook_handler(hub):
    mode = hub.mode
    token = hub.verify_token
    challenge = hub.challenge

    if mode == 'subscribe' and os.getenv('VERIFY_TOKEN') == token:
        return JSONResponse(content=challenge, status_code=200)
    else:
        return JSONResponse(content="Verification failed", status_code=403)
    