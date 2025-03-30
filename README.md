# 🎙️ Audio Transcription and Chat Application

A modern web application that transcribes audio files and enables interactive chat with the transcribed content using AI.

## 🚀 Features

### Core Features
1. **Audio Transcription**
   - Upload audio files (MP3, WAV, M4A, FLAC)
   - Real-time transcription using OpenAI's GPT-4o-transcribe
   - View transcription history

2. **Interactive Chat**
   - Chat with your transcriptions
   - Context-aware responses based on transcript content
   - Chat history per transcription
   - Real-time streaming responses

### Technical Features
- Fast and responsive Next.js frontend with React 19
- Modern UI using Tailwind CSS and shadcn/ui components
- Dark/light theme support
- Drag-and-drop file uploads
- FastAPI backend with async support
- SQLite database for data persistence
- OpenAI API integration
- Real-time updates with progress indicators
- Error handling and logging

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **AI Integration**: OpenAI API
- **Authentication**: JWT (planned)
- **Testing**: Pytest with coverage

### Frontend
- **Framework**: Next.js 15 with React 19
- **Language**: TypeScript
- **Styling**: Tailwind CSS with shadcn/ui components
- **Theme**: Light/dark mode via next-themes
- **State Management**: React Hooks (useState, useRef)
- **File Handling**: Base64 encoding for file uploads
- **API Client**: Fetch API with TypeScript interfaces
- **UI Components**: 
  - Radix UI primitives for accessible components
  - Lucide React for icons
  - Sonner for toast notifications

## 📁 Project Structure

### Frontend Structure (new-fe-vo)
```
new-fe-vo/
├── app/                       # Next.js app directory (App Router)
│   ├── globals.css            # Global styles
│   ├── layout.tsx             # Root layout with providers
│   └── page.tsx               # Main application page
├── components/                # React components
│   ├── chat-interface.tsx     # Chat UI component
│   ├── file-upload.tsx        # File upload component with drag-drop
│   ├── theme-toggle.tsx       # Theme switcher
│   ├── transcript-display.tsx # Transcript display component
│   └── ui/                    # shadcn/ui components
├── hooks/                     # Custom React hooks
├── lib/                       # Utilities and API client
│   └── api.ts                 # API client functions
├── public/                    # Static assets
└── styles/                    # Additional styles
```

### Backend Structure (app)
```
app/
├── api/                       # API routes and handlers
├── db/                        # Database models and connection
├── models/                    # Pydantic models for validation
├── services/                  # Business logic services
├── config.py                  # Configuration settings
└── main.py                    # Application entry point
```

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+ and npm/pnpm
- OpenAI API key

### Backend Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/audio-transcriber-chat.git
cd audio-transcriber-chat
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

4. Run the backend:
```bash
python start.py
```

The backend API will be available at http://localhost:8089

### Frontend Installation

1. Navigate to the frontend directory:
```bash
cd new-fe-vo
```

2. Install dependencies:
```bash
npm install
# or
pnpm install
```

3. Run the development server:
```bash
npm run dev
# or
pnpm dev
```

The frontend will be available at http://localhost:3000

## 🧪 Testing

Run backend tests with coverage:
```bash
python -m pytest
```

View coverage report:
```bash
# Open htmlcov/index.html in your browser
```

## 🔍 Frontend Components

### Main Page (page.tsx)
The main application page that orchestrates the other components and manages the application state. It handles:
- Transcript state
- Chat message state
- File upload events
- Transcription completion events
- Chat submission events

### File Upload (file-upload.tsx)
A component that allows users to upload audio files through:
- File browser selection
- Drag and drop interface
Features:
- Progress indicator during upload
- File type validation
- Error handling
- Auto-upload on file selection

### Transcript Display (transcript-display.tsx)
Displays the transcribed text with:
- Loading state
- Formatted transcript text
- Scrollable container

### Chat Interface (chat-interface.tsx)
Provides a chat interface for interacting with the transcript:
- Message history display
- Input field for new messages
- Send button
- Disabled state when no transcript is available

### Theme Toggle (theme-toggle.tsx)
A button that toggles between light and dark mode using next-themes.

## 📈 API Client (api.ts)

The frontend communicates with the backend through these API functions:

### `uploadAudioForTranscription`
Uploads an audio file and retrieves its transcription.
- Supports both File object and base64 encoded data
- Returns transcription data including ID and content

### `chatWithTranscription`
Sends a message to chat with a specific transcription.
- Requires transcription ID and message text
- Returns the AI assistant's response

### `getChatHistory`
Retrieves the chat history for a specific transcription.
- Takes a transcription ID
- Returns an array of chat messages

### `getTranscription`
Fetches a specific transcription by ID.
- Returns transcription details

### `getAllTranscriptions`
Retrieves all transcriptions.
- Returns an array of transcription objects

## 📚 API Documentation

The API documentation is available at:
- Swagger UI: http://localhost:8089/docs
- ReDoc: http://localhost:8089/redoc

### Key Endpoints

#### Transcriptions
- `GET /api/v1/transcriptions/` - List all transcriptions
- `POST /api/v1/transcriptions/` - Create new transcription
- `GET /api/v1/transcriptions/{id}` - Get specific transcription

#### Chat
- `GET /api/v1/chat/history/{transcription_id}` - Get chat history
- `POST /api/v1/chat/` - Send chat message

## 🔒 Security Considerations

- API keys are stored in environment variables
- Input validation using Pydantic models
- CORS configuration for production
- Rate limiting (planned)
- TypeScript type safety in frontend

## 📊 Monitoring and Logging

- Structured logging with Python's logging module
- Client-side error handling with error boundary components
- Console logging for development debugging
- Error tracking and monitoring (planned)
- Performance metrics (planned)

## 🚀 Deployment

### Local Development
```bash
# Backend
python start.py

# Frontend
cd new-fe-vo
npm run dev
```

### Production Deployment
1. Set environment variables
2. Configure CORS settings
3. Set up proper database
4. Build the frontend:
   ```bash
   cd new-fe-vo
   npm run build
   npm run start
   ```
5. Configure logging
6. Set up monitoring

## 🧩 Future Enhancements

- User authentication and authorization
- Multiple language support for transcriptions
- File management (delete, rename)
- Transcription editing
- Export functionality (PDF, Word, etc.)
- Mobile application using React Native
- Real-time collaborative features

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
- Next.js and React teams for the frontend frameworks
- shadcn/ui for the component library

## 📞 Support

For support, please open an issue in the GitHub repository or contact the maintainers. 