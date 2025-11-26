from sqlalchemy.orm import Session
from app.models import Room, User, CodeEdit
from uuid import uuid4

class RoomService:
    """Service for managing collaborative rooms."""
    
    @staticmethod
    def create_room(db: Session, room_name: str, language: str = "javascript") -> Room:
        """Create a new collaborative room."""
        room_id = str(uuid4())[:8]
        room = Room(
            room_id=room_id,
            room_name=room_name,
            language=language
        )
        db.add(room)
        db.commit()
        db.refresh(room)
        return room
    
    @staticmethod
    def get_room(db: Session, room_id: str) -> Room:
        """Get room by room_id."""
        return db.query(Room).filter(Room.room_id == room_id).first()
    
    @staticmethod
    def get_all_rooms(db: Session) -> list:
        """Get all rooms."""
        return db.query(Room).all()
    
    @staticmethod
    def update_room_code(db: Session, room_id: str, code_content: str) -> Room:
        """Update room code content."""
        room = db.query(Room).filter(Room.room_id == room_id).first()
        if room:
            room.code_content = code_content
            db.commit()
            db.refresh(room)
        return room
    
    @staticmethod
    def add_member_to_room(db: Session, room_id: str, user_id: int) -> Room:
        """Add user to room."""
        room = db.query(Room).filter(Room.room_id == room_id).first()
        user = db.query(User).filter(User.id == user_id).first()
        if room and user and user not in room.members:
            room.members.append(user)
            db.commit()
            db.refresh(room)
        return room
    
    @staticmethod
    def remove_member_from_room(db: Session, room_id: str, user_id: int) -> Room:
        """Remove user from room."""
        room = db.query(Room).filter(Room.room_id == room_id).first()
        user = db.query(User).filter(User.id == user_id).first()
        if room and user and user in room.members:
            room.members.remove(user)
            db.commit()
            db.refresh(room)
        return room
    
    @staticmethod
    def delete_room(db: Session, room_id: str) -> bool:
        """Delete a room."""
        room = db.query(Room).filter(Room.room_id == room_id).first()
        if room:
            db.delete(room)
            db.commit()
            return True
        return False
