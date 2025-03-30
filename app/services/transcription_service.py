"""
Transcription Service Module

This module handles audio file transcription using OpenAI's GPT-4o-transcribe API.
It provides functions for processing audio files and managing transcriptions.

Key components:
- Audio file processing
- OpenAI API integration
- Temporary file management
- Error handling
"""

import os
import tempfile
import openai
from fastapi import UploadFile
from typing import Optional, Union
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Initialize OpenAI client with API key from environment
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def transcribe_audio(file: UploadFile) -> str:
    """
    Transcribes an audio file using OpenAI's GPT-4o-transcribe API.
    
    This function handles the complete transcription process:
    1. Creates a temporary file for the uploaded audio
    2. Sends the file to OpenAI for transcription
    3. Cleans up temporary files
    4. Returns the transcribed text
    
    Args:
        file: The uploaded audio file (FastAPI UploadFile)
        
    Returns:
        str: The transcribed text
        
    Raises:
        Exception: If transcription fails or file processing errors occur
        
    Note:
        The function uses temporary files to handle the audio data.
        These files are automatically cleaned up after processing.
    """
    temp_file_path: Optional[str] = None
    try:
        # Create a temporary file to store the uploaded content
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            # Read content from the uploaded file and write to the temp file
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Rewind the uploaded file for potential reuse
        await file.seek(0)
        
        # Open the temporary file and send to OpenAI
        with open(temp_file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="gpt-4o-transcribe",
                file=audio_file
            )
        
        # Clean up the temporary file
        os.unlink(temp_file_path)
        
        return transcription.text
    
    except Exception as e:
        # Clean up temp file if it exists and there was an error
        if temp_file_path:
            os.unlink(temp_file_path)
        logger.error(f"Error transcribing audio: {str(e)}")
        raise Exception(f"Error transcribing audio: {str(e)}")

async def transcribe_audio_data(audio_data: bytes, file_extension: str = ".webm") -> str:
    """
    Transcribes raw audio data using OpenAI's GPT-4o-transcribe API.
    
    This function is similar to transcribe_audio but works with raw bytes
    instead of a file upload. It's useful for processing audio data from
    other sources like web streams or direct uploads.
    
    Args:
        audio_data: Raw audio data in bytes
        file_extension: The file extension to use for the temporary file
        
    Returns:
        str: The transcribed text
        
    Raises:
        Exception: If transcription fails or data processing errors occur
        
    Note:
        The function creates a temporary file with the specified extension
        to handle the audio data. This file is cleaned up after processing.
    """
    temp_file_path: Optional[str] = None
    try:
        # Create a temporary file to store the audio data
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            temp_file.write(audio_data)
            temp_file_path = temp_file.name
        
        # Open the temporary file and send to OpenAI
        with open(temp_file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="gpt-4o-transcribe",
                file=audio_file
            )
        
        # Clean up the temporary file
        os.unlink(temp_file_path)
        
        return transcription.text
    
    except Exception as e:
        # Clean up temp file if it exists and there was an error
        if temp_file_path:
            os.unlink(temp_file_path)
        logger.error(f"Error transcribing audio data: {str(e)}")
        raise Exception(f"Error transcribing audio data: {str(e)}") 