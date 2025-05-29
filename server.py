import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

from fastapi import Request, Query

@app.post("/webhook")
async def webhook_post_handler(request: Request):
    data = await request.json()
    return JSONResponse(content=data, status_code=200)

@app.get("/webhook")
def webhook_get_handler(
    token: str = Query(None, alias="hub.verify_token"),
    challenge: str = Query(None, alias="hub.challenge")
):
    if os.getenv('VERIFY_TOKEN') == token:
        return JSONResponse(content=challenge, status_code=200)
    else:
        return JSONResponse(content="Verification failed", status_code=403)
    