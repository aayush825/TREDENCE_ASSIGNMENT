from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base
from datetime import datetime

# Association table for room members
room_members = Table(
    'room_members',
    Base.metadata,
    Column('room_id', Integer, ForeignKey('rooms.id'), primary_key=True),
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True)
)

class User(Base):
    """User model for storing user information."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    rooms = relationship("Room", secondary=room_members, back_populates="members")
    edits = relationship("CodeEdit", back_populates="user")

class Room(Base):
    """Room model for collaborative editing spaces."""
    __tablename__ = "rooms"
    
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(String(50), unique=True, index=True, nullable=False)
    room_name = Column(String(100), nullable=False)
    code_content = Column(Text, default="")
    language = Column(String(20), default="javascript")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    members = relationship("User", secondary=room_members, back_populates="rooms")
    edits = relationship("CodeEdit", back_populates="room", cascade="all, delete-orphan")

class CodeEdit(Base):
    """CodeEdit model to track changes in the code."""
    __tablename__ = "code_edits"
    
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    operation = Column(String(20), nullable=False)  # insert, delete, replace
    line_number = Column(Integer)
    column_number = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    room = relationship("Room", back_populates="edits")
    user = relationship("User", back_populates="edits")
