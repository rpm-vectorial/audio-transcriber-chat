# 📚 API Documentation

## Overview

The Audio Transcription and Chat API provides endpoints for managing audio transcriptions and interacting with them through chat. The API follows RESTful principles and uses JSON for request/response bodies.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Currently, the API uses API key authentication for OpenAI services. Future versions will implement JWT authentication for user management.

## Endpoints

### Transcriptions

#### List Transcriptions
```http
GET /transcriptions/
```

**Response**
```json
[
  {
    "id": 1,
    "filename": "example.mp3",
    "content": "Transcribed text...",
    "created_at": "2024-03-30T20:00:00Z"
  }
]
```

#### Create Transcription
```http
POST /transcriptions/
Content-Type: multipart/form-data

file: <audio_file>
```

**Response**
```json
{
  "id": 1,
  "filename": "example.mp3",
  "content": "Transcribed text...",
  "created_at": "2024-03-30T20:00:00Z"
}
```

#### Get Transcription
```http
GET /transcriptions/{id}
```

**Response**
```json
{
  "id": 1,
  "filename": "example.mp3",
  "content": "Transcribed text...",
  "created_at": "2024-03-30T20:00:00Z"
}
```

### Chat

#### Get Chat History
```http
GET /chat/{transcription_id}
```

**Response**
```json
[
  {
    "id": 1,
    "transcription_id": 1,
    "role": "user",
    "content": "User message",
    "created_at": "2024-03-30T20:00:00Z"
  },
  {
    "id": 2,
    "transcription_id": 1,
    "role": "assistant",
    "content": "Assistant response",
    "created_at": "2024-03-30T20:00:01Z"
  }
]
```

#### Send Chat Message
```http
POST /chat/
Content-Type: application/json

{
  "transcription_id": 1,
  "content": "User message"
}
```

**Response**
```json
{
  "id": 1,
  "transcription_id": 1,
  "role": "assistant",
  "content": "Assistant response",
  "created_at": "2024-03-30T20:00:00Z"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "content"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "An unexpected error occurred"
}
```

## Rate Limiting

Rate limiting will be implemented in future versions to prevent abuse of the API.

## Best Practices

1. **Error Handling**
   - Always check response status codes
   - Handle rate limiting errors gracefully
   - Implement retry logic for transient failures

2. **File Uploads**
   - Use multipart/form-data for file uploads
   - Validate file types and sizes
   - Handle upload progress for large files

3. **Chat Interactions**
   - Maintain chat context using transcription_id
   - Handle long-running responses appropriately
   - Implement proper error recovery

## SDK Examples

### Python
```python
import requests

def create_transcription(file_path):
    url = "http://localhost:8000/api/v1/transcriptions/"
    files = {"file": open(file_path, "rb")}
    response = requests.post(url, files=files)
    return response.json()

def send_chat_message(transcription_id, message):
    url = "http://localhost:8000/api/v1/chat/"
    data = {
        "transcription_id": transcription_id,
        "content": message
    }
    response = requests.post(url, json=data)
    return response.json()
```

### JavaScript
```javascript
async function createTranscription(file) {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch('http://localhost:8000/api/v1/transcriptions/', {
    method: 'POST',
    body: formData
  });
  
  return response.json();
}

async function sendChatMessage(transcriptionId, message) {
  const response = await fetch('http://localhost:8000/api/v1/chat/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      transcription_id: transcriptionId,
      content: message
    })
  });
  
  return response.json();
}
```

## Versioning

The API is versioned through the URL path (`/api/v1/`). Breaking changes will be introduced in new versions (e.g., `/api/v2/`).

## Future Enhancements

1. **Authentication**
   - JWT-based authentication
   - API key management
   - User roles and permissions

2. **Features**
   - Batch transcription processing
   - Custom transcription models
   - Advanced chat features (context management, memory)

3. **Performance**
   - Caching layer
   - Rate limiting
   - Request queuing

## Support

For API support:
- Open an issue in the GitHub repository
- Contact the maintainers
- Check the API documentation at `/docs` or `/redoc` 