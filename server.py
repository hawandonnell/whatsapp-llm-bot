from fastapi import FastAPI

app = FastAPI()

@app.post("/webhook")
def webhook_handler(request: dict):
    print("Received webhook request:", request)
    
    return {"status": "success", "message": "Webhook received successfully"}

@app.get("/webhook")
def webhook_handler(hub):
    print("Received webhook request:", hub)
    
    return {"status": "success", "message": "Webhook received successfully"}