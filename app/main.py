"""
Audio Transcription and Chat Application

This module serves as the main entry point for the FastAPI application.
It configures the application, sets up middleware, and mounts routes.

The application provides two main features:
1. Audio file transcription using OpenAI's GPT-4o-transcribe
2. Interactive chat with transcribed content

Key components:
- FastAPI application configuration
- CORS middleware setup
- Global exception handling
- API route mounting
- Static file serving
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import os
import logging
from dotenv import load_dotenv

from app.db.database import engine, Base
from app.api import transcription, chat

# Configure logging with structured format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application with metadata
app = FastAPI(
    title="Audio Transcription and Chat App",
    description="An application that transcribes audio files and allows chatting with the content",
    version="0.1.0"
)

# Configure CORS with allowed origins
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if os.environ.get("ENVIRONMENT") == "production" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for unhandled exceptions.
    
    Args:
        request: The FastAPI request object
        exc: The unhandled exception
        
    Returns:
        JSONResponse: A 500 error response with error details
    """
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred"}
    )

@app.get("/api")
async def api_root():
    """
    Root API endpoint that returns a welcome message.
    
    Returns:
        dict: A welcome message
    """
    return {"message": "Welcome to Audio Transcription and Chat API"}

# Mount API routes with versioning
app.include_router(transcription.router, prefix="/api/v1/transcriptions", tags=["Transcriptions"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])

# Mount static files for frontend last to avoid route conflicts
try:
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
    logger.info("Frontend files mounted successfully")
except Exception as e:
    logger.warning(f"Could not mount frontend files: {e}")

# Development server entry point
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 