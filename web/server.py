from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from pathlib import Path
from app.main import run_agent

app = FastAPI()

@app.get("/")
async def get():
    html = Path("web/index.html").read_text()
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    while True:
        user_msg = await ws.receive_text()
        await ws.send_text("🤖 Thinking...")

        try:
            reply = await run_agent(user_msg)
            await ws.send_text(reply)
        except Exception as e:
            await ws.send_text(f"❌ Error: {str(e)}")
