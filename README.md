# 🎙️ Audio Transcription and Chat Application

A modern web application that transcribes audio files and enables interactive chat with the transcribed content using AI.

## 🚀 Features

### Core Features
1. **Audio Transcription**
   - Upload audio files (MP3, WAV, M4A)
   - Real-time transcription using OpenAI's GPT-4o-transcribe
   - View transcription history

2. **Interactive Chat**
   - Chat with your transcriptions
   - Context-aware responses
   - Chat history per transcription

### Technical Features
- FastAPI backend with async support
- SQLite database for data persistence
- Modern React frontend
- OpenAI API integration
- Real-time updates
- Error handling and logging

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **AI Integration**: OpenAI API
- **Authentication**: JWT (planned)
- **Testing**: Pytest with coverage

### Frontend
- **Framework**: React
- **Styling**: CSS3
- **State Management**: React Hooks
- **API Client**: Fetch API

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 14+ (for frontend development)
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/audio-transcript.git
cd audio-transcript
```

2. Set up Python virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

4. Run the application:
```bash
python run.py
```

The application will be available at http://localhost:8000

## 🧪 Testing

Run tests with coverage:
```bash
python -m pytest
```

View coverage report:
```bash
# Open htmlcov/index.html in your browser
```

## 📚 API Documentation

The API documentation is available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Key Endpoints

#### Transcriptions
- `GET /api/v1/transcriptions/` - List all transcriptions
- `POST /api/v1/transcriptions/` - Create new transcription
- `GET /api/v1/transcriptions/{id}` - Get specific transcription

#### Chat
- `GET /api/v1/chat/{transcription_id}` - Get chat history
- `POST /api/v1/chat/` - Send chat message

## 🔒 Security Considerations

- API keys are stored in environment variables
- Input validation using Pydantic models
- CORS configuration for production
- Rate limiting (planned)

## 📊 Monitoring and Logging

- Structured logging with Python's logging module
- Error tracking and monitoring (planned)
- Performance metrics (planned)

## 🚀 Deployment

### Local Development
```bash
python run.py
```

### Production Deployment
1. Set environment variables
2. Configure CORS settings
3. Set up proper database
4. Configure logging
5. Set up monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for the transcription API
- FastAPI team for the excellent framework
- React team for the frontend framework

## 📞 Support

For support, please open an issue in the GitHub repository or contact the maintainers. 