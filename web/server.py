from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from pathlib import Path
import json
import traceback

from app.main import run_agent

app = FastAPI()


@app.get("/")
async def index():
    return HTMLResponse(Path("web/index.html").read_text())


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            user_msg = await ws.receive_text()

            # Tell frontend we are processing
            await ws.send_text(json.dumps({
                "type": "thinking"
            }))

            reply = await run_agent(user_msg)

            await ws.send_text(json.dumps({
                "type": "final",
                "content": reply
            }))

    except Exception as e:
        # ✅ LOG ERROR
        print("WebSocket error:", e)
        traceback.print_exc()

        # ❌ DO NOT close socket here
        # Browser will reconnect automatically if needed
        await ws.send_text(json.dumps({
            "type": "error",
            "content": "An error occurred. Please try again."
        }))