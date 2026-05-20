from fastapi import WebSocket
from typing import List, Dict
import json

class ConnectionManager:
    def __init__(self):
        # Simpan koneksi per channel_id
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, channel_id: str):
        await websocket.accept()
        if channel_id not in self.active_connections:
            self.active_connections[channel_id] = []
        self.active_connections[channel_id].append(websocket)
        print(f"✅ WebSocket connected: channel {channel_id} — total: {len(self.active_connections[channel_id])}")

    def disconnect(self, websocket: WebSocket, channel_id: str):
        if channel_id in self.active_connections:
            self.active_connections[channel_id].remove(websocket)
            print(f"❌ WebSocket disconnected: channel {channel_id}")

    async def broadcast_to_channel(self, channel_id: str, data: dict):
        if channel_id not in self.active_connections:
            return
        dead = []
        for connection in self.active_connections[channel_id]:
            try:
                await connection.send_text(json.dumps(data))
            except Exception:
                dead.append(connection)
        for d in dead:
            self.active_connections[channel_id].remove(d)

manager = ConnectionManager()
