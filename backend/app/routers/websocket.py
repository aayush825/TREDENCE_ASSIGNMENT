from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.room_service import RoomService
import json
from typing import Dict, List
import asyncio

router = APIRouter(prefix="/ws", tags=["websocket"])

# Store active WebSocket connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, room_id: str):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)
    
    def disconnect(self, websocket: WebSocket, room_id: str):
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]
    
    async def broadcast(self, message: dict, room_id: str, exclude: WebSocket = None):
        """Broadcast message to all clients in a room."""
        if room_id in self.active_connections:
            disconnected = []
            for connection in self.active_connections[room_id]:
                if exclude and connection == exclude:
                    continue
                try:
                    await connection.send_json(message)
                except Exception:
                    disconnected.append(connection)
            
            # Clean up disconnected clients
            for connection in disconnected:
                self.disconnect(connection, room_id)

manager = ConnectionManager()

@router.websocket("/editor/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    """WebSocket endpoint for collaborative editing."""
    await manager.connect(websocket, room_id)
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Broadcast the message to all other users in the room
            broadcast_message = {
                "type": message.get("type", "code_change"),
                "data": message.get("data", {}),
                "timestamp": message.get("timestamp")
            }
            
            await manager.broadcast(broadcast_message, room_id, exclude=websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
        # Notify others that user disconnected
        await manager.broadcast({
            "type": "user_disconnected",
            "message": "A user has disconnected"
        }, room_id)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket, room_id)

@router.get("/rooms/{room_id}/connections")
def get_room_connections(room_id: str):
    """Get number of active connections in a room."""
    count = len(manager.active_connections.get(room_id, []))
    return {"room_id": room_id, "active_connections": count}
