from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status, Request
from sqlalchemy.orm import Session
from typing import List
import base64

from app.db.database import get_db
from app.models.models import Transcription
from app.models.schemas import TranscriptionResponse, RealTimeTranscriptionRequest, RealTimeTranscriptionResponse
from app.services.transcription_service import transcribe_audio, transcribe_audio_data

router = APIRouter()

@router.post("/", response_model=TranscriptionResponse)
async def create_transcription(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
) -> TranscriptionResponse:
    """
    Upload an audio file and transcribe it.
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="No file provided"
        )
    
    # Check file type (optional enhancement)
    allowed_extensions = [".mp3", ".wav", ".m4a", ".mp4", ".mpeg", ".mpga", ".webm"]
    file_ext = "." + file.filename.split(".")[-1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    try:
        # Call the transcription service
        transcription_text = await transcribe_audio(file)
        
        # Create transcription record
        db_transcription = await _save_transcription(db, file.filename, transcription_text)
        
        return db_transcription
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )


@router.post("/real-time", response_model=RealTimeTranscriptionResponse)
async def real_time_transcription(
    request: RealTimeTranscriptionRequest,
    db: Session = Depends(get_db)
) -> RealTimeTranscriptionResponse:
    """
    Transcribe audio data sent in real-time.
    """
    try:
        # Decode the base64 audio data
        audio_data = base64.b64decode(request.audio_data)
        
        # Call the transcription service
        transcription_text = await transcribe_audio_data(audio_data, request.file_extension)
        
        # Save transcription to database
        db_transcription = None
        # Only save to database if save_to_db is True
        if request.save_to_db:
            filename = f"real-time-recording{request.file_extension}"
            db_transcription = await _save_transcription(db, filename, transcription_text)
            
        return RealTimeTranscriptionResponse(
            transcription=transcription_text,
            transcription_id=db_transcription.id if db_transcription else None
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )


@router.get("/{transcription_id}", response_model=TranscriptionResponse)
def get_transcription(transcription_id: int, db: Session = Depends(get_db)) -> TranscriptionResponse:
    """
    Get a specific transcription by ID.
    """
    transcription = db.query(Transcription).filter(Transcription.id == transcription_id).first()
    if not transcription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Transcription not found"
        )
    return transcription


@router.get("/", response_model=List[TranscriptionResponse])
def list_transcriptions(db: Session = Depends(get_db)) -> List[TranscriptionResponse]:
    """
    Get a list of all transcriptions.
    """
    return db.query(Transcription).all()


async def _save_transcription(db: Session, filename: str, content: str) -> Transcription:
    """
    Save a transcription to the database.
    
    Args:
        db: Database session
        filename: Name of the transcribed file
        content: Transcription text content
        
    Returns:
        The created transcription record
    """
    db_transcription = Transcription(
        filename=filename,
        content=content
    )
    db.add(db_transcription)
    db.commit()
    db.refresh(db_transcription)
    
    return db_transcription 