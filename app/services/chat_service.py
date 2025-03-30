"""
Chat Service Module

This module handles chat interactions with transcribed content using OpenAI's GPT-4.
It provides functions for managing chat history and generating responses.

Key components:
- Chat message processing
- OpenAI API integration
- Context management
- Response generation
"""

import os
import openai
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import logging

from app.models.models import Transcription, ChatMessage
from app.models.schemas import ChatMessageCreate, ChatMessageResponse

# Configure logging
logger = logging.getLogger(__name__)

# Create client using API key from environment
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def chat_with_transcription(
    db: Session, 
    transcription_id: int, 
    user_message: str
) -> str:
    """
    Process a user message and generate a response based on the transcription content.
    
    Args:
        db: Database session
        transcription_id: ID of the transcription to chat about
        user_message: User's question or message
        
    Returns:
        The assistant's response
    """
    # Get the transcription
    transcription = _get_transcription(db, transcription_id)
    
    # Get conversation history
    conversation_history = _get_conversation_history(db, transcription_id)
    
    # Save user message
    _save_message(db, transcription_id, "user", user_message)
    
    # Prepare messages for API call
    messages = _prepare_messages(transcription.content, conversation_history, user_message)
    
    # Get response from OpenAI
    assistant_message = await _get_chat_completion(messages)
    
    # Save assistant message
    _save_message(db, transcription_id, "assistant", assistant_message)
    
    return assistant_message


def _get_transcription(db: Session, transcription_id: int) -> Transcription:
    """
    Get a transcription by ID.
    
    Args:
        db: Database session
        transcription_id: ID of the transcription
        
    Returns:
        The transcription record
        
    Raises:
        ValueError: If transcription not found
    """
    transcription = db.query(Transcription).filter(Transcription.id == transcription_id).first()
    if not transcription:
        raise ValueError(f"Transcription with ID {transcription_id} not found")
    return transcription


def _get_conversation_history(db: Session, transcription_id: int, limit: int = 10) -> List[ChatMessage]:
    """
    Get the conversation history for a transcription.
    
    Args:
        db: Database session
        transcription_id: ID of the transcription
        limit: Maximum number of messages to return
        
    Returns:
        List of chat messages
    """
    return (
        db.query(ChatMessage)
        .filter(ChatMessage.transcription_id == transcription_id)
        .order_by(ChatMessage.created_at.desc())
        .limit(limit)
        .all()
    )


def _save_message(db: Session, transcription_id: int, role: str, content: str) -> ChatMessage:
    """
    Save a chat message to the database.
    
    Args:
        db: Database session
        transcription_id: ID of the transcription
        role: Message role ('user' or 'assistant')
        content: Message content
        
    Returns:
        The created message record
    """
    db_message = ChatMessage(
        transcription_id=transcription_id,
        role=role,
        content=content
    )
    db.add(db_message)
    db.commit()
    return db_message


def _prepare_messages(
    transcription_content: str, 
    conversation_history: List[ChatMessage], 
    current_message: str
) -> List[Dict[str, str]]:
    """
    Prepare messages for OpenAI API call.
    
    Args:
        transcription_content: Content of the transcription
        conversation_history: Previous messages
        current_message: Current user message
        
    Returns:
        List of messages formatted for OpenAI API
    """
    messages = [
        {
            "role": "system", 
            "content": f"You are an assistant helping with questions about a transcribed audio. Here is the transcription: {transcription_content}"
        }
    ]
    
    # Add previous messages in chronological order
    for msg in reversed(conversation_history):
        messages.append({"role": msg.role, "content": msg.content})
    
    # Add the current message
    messages.append({"role": "user", "content": current_message})
    
    return messages


async def _get_chat_completion(messages: List[Dict[str, str]]) -> str:
    """
    Get completion from OpenAI API.
    
    Args:
        messages: List of messages formatted for OpenAI API
        
    Returns:
        The assistant's response
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
    
    return response.choices[0].message.content 

async def get_chat_history(db: Session, transcription_id: int) -> List[ChatMessageResponse]:
    """
    Retrieves the chat history for a specific transcription.
    
    Args:
        db: SQLAlchemy database session
        transcription_id: ID of the transcription
        
    Returns:
        List[ChatMessageResponse]: List of chat messages in chronological order
        
    Note:
        Messages are returned in order of creation (oldest first).
    """
    messages = db.query(ChatMessage).filter(
        ChatMessage.transcription_id == transcription_id
    ).order_by(ChatMessage.created_at).all()
    
    return [ChatMessageResponse.from_orm(msg) for msg in messages]

async def create_chat_message(
    db: Session,
    message: ChatMessageCreate
) -> ChatMessageResponse:
    """
    Creates a new chat message and generates an AI response.
    
    This function:
    1. Saves the user's message
    2. Retrieves the transcription context
    3. Generates an AI response using GPT-4
    4. Saves the AI response
    
    Args:
        db: SQLAlchemy database session
        message: The chat message to create
        
    Returns:
        ChatMessageResponse: The created message with AI response
        
    Raises:
        Exception: If message creation or AI response generation fails
    """
    try:
        # Get transcription for context
        transcription = db.query(Transcription).filter(
            Transcription.id == message.transcription_id
        ).first()
        
        if not transcription:
            raise Exception("Transcription not found")
        
        # Create user message
        user_message = ChatMessage(
            transcription_id=message.transcription_id,
            role="user",
            content=message.content
        )
        db.add(user_message)
        db.commit()
        db.refresh(user_message)
        
        # Get chat history for context
        history = await get_chat_history(db, message.transcription_id)
        
        # Prepare conversation context
        messages = [
            {"role": "system", "content": f"You are a helpful assistant analyzing the following transcription:\n\n{transcription.content}"}
        ]
        
        # Add chat history
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})
        
        # Generate AI response
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        
        # Create assistant message
        assistant_message = ChatMessage(
            transcription_id=message.transcription_id,
            role="assistant",
            content=response.choices[0].message.content
        )
        db.add(assistant_message)
        db.commit()
        db.refresh(assistant_message)
        
        return ChatMessageResponse.from_orm(assistant_message)
        
    except Exception as e:
        logger.error(f"Error creating chat message: {str(e)}")
        raise Exception(f"Error creating chat message: {str(e)}")

async def get_transcription_context(db: Session, transcription_id: int) -> Optional[str]:
    """
    Retrieves the transcription content for context.
    
    Args:
        db: SQLAlchemy database session
        transcription_id: ID of the transcription
        
    Returns:
        Optional[str]: The transcription content or None if not found
    """
    transcription = db.query(Transcription).filter(
        Transcription.id == transcription_id
    ).first()
    
    return transcription.content if transcription else None 