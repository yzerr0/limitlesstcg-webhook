import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

LIMITLESS_WEBHOOK_SECRET = os.getenv('LIMITLESS_WEBHOOK_SECRET', '')

class WebhookEvent(BaseModel):
    name: str
    tournamentId: str
    game: str

class WebhookPayload(BaseModel):
    secret: str
    event: WebhookEvent

@app.get("/health_check")
def health_check():
    return {"status": "OK"}

@app.post("/limitless/webhook")
def limitless_webhook(payload: WebhookPayload):
    if not LIMITLESS_WEBHOOK_SECRET or payload.secret != LIMITLESS_WEBHOOK_SECRET:
        raise HTTPException(status_code=401, detail="Invalid secret")
    
    # Process the webhook event
    event = payload.event
    
    # TODO: Enqueue ingestion job (DB insert, Redis queue, etc); Keep webhook fast

    return {"ok": True, "name": event.name, "tournamentId": event.tournamentId, "game": event.game}