"""
Database Models Module

This module defines the SQLAlchemy ORM models for the application.
It includes models for transcriptions and chat messages.

Key components:
- Transcription model for storing audio transcriptions
- ChatMessage model for storing chat history
"""

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import datetime

from app.db.database import Base


class Transcription(Base):
    """
    SQLAlchemy model for storing audio transcriptions.
    
    Attributes:
        id (int): Primary key
        filename (str): Name of the audio file
        content (str): Transcribed text content
        created_at (datetime): Timestamp of creation
    """
    
    __tablename__ = "transcriptions"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship with ChatMessage
    messages = relationship("ChatMessage", back_populates="transcription")


class ChatMessage(Base):
    """
    SQLAlchemy model for storing chat messages.
    
    Attributes:
        id (int): Primary key
        transcription_id (int): Foreign key to Transcription
        role (str): Message role (user/assistant)
        content (str): Message content
        created_at (datetime): Timestamp of creation
    """
    
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    transcription_id = Column(Integer, ForeignKey("transcriptions.id"))
    role = Column(String, nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship with Transcription
    transcription = relationship("Transcription", back_populates="messages") 