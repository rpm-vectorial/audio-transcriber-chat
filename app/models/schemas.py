"""
Pydantic Schemas Module

This module defines the Pydantic models for request/response validation.
It includes schemas for transcriptions and chat messages.

Key components:
- Base schemas for common attributes
- Request schemas for data validation
- Response schemas for API responses
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
import re


class TranscriptionBase(BaseModel):
    """
    Base schema for transcription data.
    
    Attributes:
        filename (str): Name of the audio file
        content (str): Transcribed text content
    """
    filename: str = Field(..., min_length=1, max_length=255, description="Name of the uploaded audio file")
    content: str = Field(..., description="Transcribed text content")


class TranscriptionCreate(TranscriptionBase):
    """
    Schema for creating a new transcription.
    Inherits from TranscriptionBase.
    """
    pass


class TranscriptionResponse(TranscriptionBase):
    """
    Schema for transcription API response.
    
    Attributes:
        id (int): Primary key
        created_at (datetime): Timestamp of creation
    """
    id: int = Field(..., description="Unique identifier for the transcription")
    created_at: datetime = Field(..., description="Timestamp when the transcription was created")

    class Config:
        """Pydantic configuration for ORM mode."""
        from_attributes = True


class RealTimeTranscriptionRequest(BaseModel):
    audio_data: str = Field(..., description="Base64 encoded audio data")
    file_extension: str = Field(".webm", description="File extension for the audio data")
    save_to_db: bool = Field(False, description="Whether to save the transcription to the database")


class RealTimeTranscriptionResponse(BaseModel):
    transcription: str = Field(..., description="Transcribed text content")
    transcription_id: Optional[int] = Field(None, description="ID of the saved transcription if saved to database")


class ChatMessageBase(BaseModel):
    """
    Base schema for chat message data.
    
    Attributes:
        transcription_id (int): ID of the associated transcription
        content (str): Message content
    """
    transcription_id: int = Field(..., gt=0, description="ID of the transcription this message is associated with")
    content: str = Field(..., min_length=1, description="Message content")


class ChatMessageCreate(ChatMessageBase):
    """
    Schema for creating a new chat message.
    Inherits from ChatMessageBase.
    """
    role: str = Field("user", pattern="^(user|assistant)$", description="Role of the message sender")


class ChatMessageResponse(ChatMessageBase):
    """
    Schema for chat message API response.
    
    Attributes:
        id (int): Primary key
        role (str): Message role (user/assistant)
        created_at (datetime): Timestamp of creation
    """
    id: int = Field(..., description="Unique identifier for the message")
    role: str = Field(..., description="Role of the message sender (user or assistant)")
    created_at: datetime = Field(..., description="Timestamp when the message was created")

    class Config:
        """Pydantic configuration for ORM mode."""
        from_attributes = True


class ChatRequest(BaseModel):
    transcription_id: int = Field(..., gt=0, description="ID of the transcription to chat about")
    message: str = Field(..., min_length=1, description="User's message content")


class ChatResponse(BaseModel):
    answer: str = Field(..., description="Assistant's response to the user's message")


class ChatHistory(BaseModel):
    """
    Schema for chat history response.
    
    Attributes:
        transcription_id (int): ID of the associated transcription
        messages (List[ChatMessageResponse]): List of chat messages
    """
    transcription_id: int
    messages: List[ChatMessageResponse] 