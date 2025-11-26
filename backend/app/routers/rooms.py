from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.room_service import RoomService
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/api/rooms", tags=["rooms"])

class RoomCreate(BaseModel):
    room_name: str
    language: str = "javascript"

class RoomResponse(BaseModel):
    id: int
    room_id: str
    room_name: str
    language: str
    code_content: str
    
    class Config:
        from_attributes = True

@router.post("/create", response_model=RoomResponse)
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    """Create a new collaborative room."""
    try:
        new_room = RoomService.create_room(db, room.room_name, room.language)
        return new_room
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{room_id}", response_model=RoomResponse)
def get_room(room_id: str, db: Session = Depends(get_db)):
    """Get a room by room_id."""
    room = RoomService.get_room(db, room_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.get("/")
def get_all_rooms(db: Session = Depends(get_db)):
    """Get all rooms."""
    rooms = RoomService.get_all_rooms(db)
    return rooms

@router.put("/{room_id}/code")
def update_room_code(room_id: str, code_content: dict, db: Session = Depends(get_db)):
    """Update room code content."""
    room = RoomService.update_room_code(db, room_id, code_content.get("code", ""))
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

@router.post("/{room_id}/members/{user_id}")
def add_member(room_id: str, user_id: int, db: Session = Depends(get_db)):
    """Add a member to the room."""
    room = RoomService.add_member_to_room(db, room_id, user_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return {"message": "Member added successfully"}

@router.delete("/{room_id}/members/{user_id}")
def remove_member(room_id: str, user_id: int, db: Session = Depends(get_db)):
    """Remove a member from the room."""
    room = RoomService.remove_member_from_room(db, room_id, user_id)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    return {"message": "Member removed successfully"}

@router.delete("/{room_id}")
def delete_room(room_id: str, db: Session = Depends(get_db)):
    """Delete a room."""
    success = RoomService.delete_room(db, room_id)
    if not success:
        raise HTTPException(status_code=404, detail="Room not found")
    return {"message": "Room deleted successfully"}
