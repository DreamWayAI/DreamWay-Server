
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

class PostRequest(BaseModel):
    text: str
    image: str
    topic: str

TELEGRAM_TOKEN = "7804300819:AAGXbE8s39Gx4mlL9akyJsqwzcbVCFSq6mU"
CHANNEL_ID = "@dreamway_ai"

@app.post("/generate")
async def generate(data: PromptRequest):
    return {"text": f"✨ Автогенерація: {data.prompt}"}

@app.post("/publish")
async def publish(data: PostRequest):
    try:
        text = f"📌 *{data.topic}*\n\n{data.text}"
        payload = {
            "chat_id": CHANNEL_ID,
            "caption": text,
            "parse_mode": "Markdown"
        }
        if data.image:
            payload["photo"] = data.image
            response = requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto", data=payload)
        else:
            payload = {
                "chat_id": CHANNEL_ID,
                "text": text,
                "parse_mode": "Markdown"
            }
            response = requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", data=payload)
        return {"success": response.status_code == 200}
    except Exception as e:
        return {"success": False, "error": str(e)}
