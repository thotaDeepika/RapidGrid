import sys

# 1. Create backend/routers/chat.py
chat_py = """# Real-time WebSocket Emergency Chat Router
from __future__ import annotations
import json
from typing import Dict, List, Set
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/api/chat", tags=["Realtime Emergency Chat"])

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.chat_history: Dict[str, List[Dict]] = {}

    async def connect(self, websocket: WebSocket, incident_id: str):
        await websocket.accept()
        if incident_id not in self.active_connections:
            self.active_connections[incident_id] = set()
            self.chat_history[incident_id] = []
        self.active_connections[incident_id].add(websocket)

    def disconnect(self, websocket: WebSocket, incident_id: str):
        if incident_id in self.active_connections:
            self.active_connections[incident_id].discard(websocket)

    async def broadcast(self, incident_id: str, message_data: Dict):
        if incident_id not in self.chat_history:
            self.chat_history[incident_id] = []
        self.chat_history[incident_id].append(message_data)

        if incident_id in self.active_connections:
            dead_sockets = set()
            for ws in list(self.active_connections[incident_id]):
                try:
                    await ws.send_json(message_data)
                except Exception:
                    dead_sockets.add(ws)
            for ws in dead_sockets:
                self.active_connections[incident_id].discard(ws)

manager = ConnectionManager()

class ChatMessagePayload(BaseModel):
    incident_id: str
    sender_role: str
    sender_name: str
    message: str

@router.get("/{incident_id}/messages")
async def get_chat_history(incident_id: str):
    history = manager.chat_history.get(incident_id, [])
    return {"messages": history}

@router.post("/{incident_id}/send")
async def send_chat_message(incident_id: str, payload: ChatMessagePayload):
    msg_data = {
        "incident_id": incident_id,
        "sender_role": payload.sender_role,
        "sender_name": payload.sender_name,
        "message": payload.message,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }
    await manager.broadcast(incident_id, msg_data)
    return {"status": "sent", "message": msg_data}
"""

with open("routers/chat.py", "w", encoding="utf-8") as f:
    f.write(chat_py)

# 2. Update backend/main.py to include chat router and WebSocket endpoint
main_py_file = "main.py"
with open(main_py_file, "r", encoding="utf-8") as f:
    m_content = f.read()

if "from routers import" in m_content and "chat" not in m_content:
    m_content = m_content.replace(
        "from routers import accessibility",
        "from routers import chat, accessibility"
    )

if "app.include_router(chat.router)" not in m_content:
    m_content = m_content.replace(
        "app.include_router(driver.router)",
        "app.include_router(driver.router)\napp.include_router(chat.router)"
    )

ws_endpoint_code = """
from fastapi import WebSocket, WebSocketDisconnect
@app.websocket("/ws/chat/{incident_id}")
async def websocket_chat_endpoint(websocket: WebSocket, incident_id: str):
    await chat.manager.connect(websocket, incident_id)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                payload = json.loads(data)
                msg_data = {
                    "incident_id": incident_id,
                    "sender_role": payload.get("sender_role", "citizen"),
                    "sender_name": payload.get("sender_name", "Anonymous"),
                    "message": payload.get("message", ""),
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                }
                await chat.manager.broadcast(incident_id, msg_data)
            except Exception as e:
                print("WS Error:", e)
    except WebSocketDisconnect:
        chat.manager.disconnect(websocket, incident_id)
"""

if "/ws/chat/" not in m_content:
    m_content += "\n" + ws_endpoint_code

with open(main_py_file, "w", encoding="utf-8") as f:
    f.write(m_content)

print("Backend WebSocket chat router and endpoint created successfully")
