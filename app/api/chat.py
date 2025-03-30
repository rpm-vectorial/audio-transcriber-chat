from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.models import ChatMessage
from app.models.schemas import ChatMessageResponse, ChatRequest, ChatResponse
from app.services.chat_service import chat_with_transcription

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def create_chat_message(
    chat_request: ChatRequest,
    db: Session = Depends(get_db)
) -> ChatResponse:
    """
    Send a message to chat with a transcription.
    """
    try:
        assistant_response = await chat_with_transcription(
            db, 
            chat_request.transcription_id, 
            chat_request.message
        )
        return ChatResponse(answer=assistant_response)
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=str(e)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )


@router.get("/history/{transcription_id}", response_model=List[ChatMessageResponse])
def get_chat_history(transcription_id: int, db: Session = Depends(get_db)) -> List[ChatMessageResponse]:
    """
    Get the chat history for a specific transcription.
    """
    messages = (
        db.query(ChatMessage)
        .filter(ChatMessage.transcription_id == transcription_id)
        .order_by(ChatMessage.created_at)
        .all()
    )
    return messages 