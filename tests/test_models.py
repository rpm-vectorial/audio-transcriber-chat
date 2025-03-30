import pytest
from sqlalchemy.orm import Session
from app.models.models import Transcription, ChatMessage

def test_create_transcription(db_session: Session):
    """Test creating a transcription record."""
    transcription = Transcription(
        filename="test.mp3",
        content="Test transcription content"
    )
    db_session.add(transcription)
    db_session.commit()
    db_session.refresh(transcription)

    assert transcription.id is not None
    assert transcription.filename == "test.mp3"
    assert transcription.content == "Test transcription content"

def test_create_chat_message(db_session: Session):
    """Test creating a chat message."""
    # First create a transcription
    transcription = Transcription(
        filename="test.mp3",
        content="Test transcription content"
    )
    db_session.add(transcription)
    db_session.commit()

    # Create a chat message
    chat_message = ChatMessage(
        transcription_id=transcription.id,
        role="user",
        content="Test chat message"
    )
    db_session.add(chat_message)
    db_session.commit()
    db_session.refresh(chat_message)

    assert chat_message.id is not None
    assert chat_message.transcription_id == transcription.id
    assert chat_message.role == "user"
    assert chat_message.content == "Test chat message"

def test_transcription_chat_relationship(db_session: Session):
    """Test the relationship between Transcription and ChatMessage."""
    # Create a transcription
    transcription = Transcription(
        filename="test.mp3",
        content="Test transcription content"
    )
    db_session.add(transcription)
    db_session.commit()

    # Create multiple chat messages
    messages = [
        ChatMessage(
            transcription_id=transcription.id,
            role="user",
            content=f"Message {i}"
        )
        for i in range(3)
    ]
    for message in messages:
        db_session.add(message)
    db_session.commit()

    # Test the relationship
    assert len(transcription.messages) == 3
    assert all(msg.transcription_id == transcription.id for msg in transcription.messages) 