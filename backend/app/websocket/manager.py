from collections import defaultdict
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self) -> None:
        self.connections: dict[str, list[WebSocket]] = defaultdict(list)

    async def connect(self, trip_id: str, websocket: WebSocket) -> None:
        await websocket.accept()
        self.connections[trip_id].append(websocket)

    def disconnect(self, trip_id: str, websocket: WebSocket) -> None:
        if websocket in self.connections[trip_id]:
            self.connections[trip_id].remove(websocket)

    async def broadcast(self, trip_id: str, payload: dict) -> None:
        for ws in self.connections[trip_id]:
            await ws.send_json(payload)


manager = ConnectionManager()
