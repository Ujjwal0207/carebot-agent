from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from pathlib import Path
import json
import traceback

from app.main import run_agent

app = FastAPI()


def _stream_text_chunks(text: str, chunk_size: int = 8):
    """
    Yield small chunks of the final response so the frontend
    can render them incrementally and feel like token streaming.

    NOTE: We are *not* changing how the LLM is called – only how
    we send the final string over the WebSocket.
    """
    for i in range(0, len(text), chunk_size):
        yield text[i : i + chunk_size]


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

            # --- STREAMING LAYER ----------------------------------------
            # We first send small chunks so the UI can update token-by-token,
            # then send a final message with the full text for safety.
            for chunk in _stream_text_chunks(reply):
                await ws.send_text(json.dumps({
                    "type": "stream",
                    "content": chunk,
                }))

            await ws.send_text(json.dumps({
                "type": "final",
                "content": reply,
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