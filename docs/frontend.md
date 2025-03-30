# 🎨 Audio Transcriber & Chat - Frontend Documentation

This document provides comprehensive documentation for the frontend of the Audio Transcriber & Chat application. The frontend is built with Next.js, React 19, TypeScript, and Tailwind CSS with shadcn/ui components.

## 📋 Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Tech Stack](#tech-stack)
3. [Project Structure](#project-structure)
4. [Components](#components)
5. [State Management](#state-management)
6. [API Integration](#api-integration)
7. [Theming](#theming)
8. [Styling](#styling)
9. [Development](#development)

## 🏗️ Architecture Overview

The frontend follows a component-based architecture using React with Next.js App Router. The application is structured as a single-page application (SPA) with client-side rendering for most components.

Key architectural patterns:
- **Component Composition**: Building UI from smaller, reusable components
- **Hooks-based State Management**: Using React's built-in state management with hooks
- **API Client**: Centralized API client functions in `lib/api.ts`
- **Responsive Design**: Mobile-first approach using Tailwind CSS
- **Accessibility**: Built on top of accessible Radix UI primitives via shadcn/ui

## 🛠️ Tech Stack

- **Framework**: Next.js 15.x
- **UI Library**: React 19.x
- **Language**: TypeScript 5.x
- **Styling**: 
  - Tailwind CSS 3.x
  - shadcn/ui components
- **Component Libraries**:
  - Radix UI primitives
  - Lucide React for icons
  - Sonner for toast notifications
- **State Management**: React Hooks
- **Data Fetching**: Fetch API

## 📁 Project Structure

```
new-fe-vo/
├── app/                        # Next.js app directory (App Router)
│   ├── globals.css             # Global styles
│   ├── layout.tsx              # Root layout with providers
│   └── page.tsx                # Main application page
├── components/                 # React components
│   ├── chat-interface.tsx      # Chat UI component
│   ├── file-upload.tsx         # File upload component with drag-drop
│   ├── theme-toggle.tsx        # Theme switcher
│   ├── transcript-display.tsx  # Transcript display component
│   └── ui/                     # shadcn/ui components
├── hooks/                      # Custom React hooks
├── lib/                        # Utilities and API client
│   └── api.ts                  # API client functions
├── public/                     # Static assets
└── styles/                     # Additional styles
```

## 🧩 Components

### Main Page (`page.tsx`)

The main application page orchestrates the other components and manages the application state.

**State Management**:
- `transcript`: Stores the current transcription text
- `isLoading`: Tracks loading state during file upload and transcription
- `chatMessages`: Stores chat message history
- `transcriptionId`: Stores the ID of the current transcription

**Key Functions**:
- `handleTranscriptionComplete`: Processes completed transcriptions
- `handleUploadStart`: Manages state when file upload begins
- `handleChatSubmit`: Handles submission of chat messages

**Layout**:
- Responsive grid layout with 1-column on mobile, 3-column on desktop
- Left/top section: File upload and transcript display
- Right/bottom section: Chat interface

### File Upload (`file-upload.tsx`)

Component for uploading audio files via browser selection or drag-and-drop.

**Props**:
- `onUploadStart`: Callback function triggered when upload begins
- `onTranscriptionComplete`: Callback function triggered when transcription completes

**State**:
- `selectedFile`: Stores the currently selected file
- `uploadProgress`: Tracks upload progress (0-100%)
- `isUploading`: Boolean flag for upload in progress
- `error`: Stores error messages

**Features**:
- File type validation (audio files only)
- Progress indicator during upload
- Error handling with user feedback
- Auto-upload on file selection or drop
- Base64 encoding for file uploads

### Transcript Display (`transcript-display.tsx`)

Component for displaying the transcribed text.

**Props**:
- `transcript`: The transcription text to display
- `isLoading`: Boolean indicating if transcription is in progress

**Features**:
- Loading state with skeleton UI
- Scrollable text container
- Formatted transcript text

### Chat Interface (`chat-interface.tsx`)

Provides a chat interface for interacting with the transcription.

**Props**:
- `messages`: Array of chat messages
- `onSendMessage`: Callback function for sending messages
- `isDisabled`: Boolean to disable input when no transcript is available
- `transcriptionId`: Optional ID of the current transcription

**Features**:
- Message history display with user/assistant styling
- Input field with send button
- Disabled state handling
- Auto-scroll to most recent messages

### Theme Toggle (`theme-toggle.tsx`)

Button component for toggling between light and dark mode.

**Features**:
- Uses `next-themes` for theme management
- Icon changes based on current theme
- Smooth transition between themes

## 📊 State Management

The application uses React's built-in state management with hooks:

- **Local Component State**: Each component manages its own state using `useState`
- **Parent-Child Communication**: Props and callback functions
- **No Global State**: The application is simple enough to avoid Redux or Context API
- **Refs for DOM Interaction**: Using `useRef` for direct DOM manipulation when needed

State flow example:
1. User selects a file in `FileUpload`
2. `FileUpload` calls `onUploadStart` to notify parent
3. Parent updates `isLoading` state
4. When transcription completes, `FileUpload` calls `onTranscriptionComplete`
5. Parent updates `transcript` and `transcriptionId` state
6. Updated state flows to `TranscriptDisplay` and `ChatInterface`

## 🔌 API Integration

The frontend communicates with the backend through functions defined in `lib/api.ts`:

### API Endpoints

| Function | Endpoint | Method | Description |
|----------|----------|--------|-------------|
| `uploadAudioForTranscription` | `/api/v1/transcriptions/` | POST | Upload audio file and get transcription |
| `chatWithTranscription` | `/api/v1/chat/` | POST | Send chat message and get response |
| `getChatHistory` | `/api/v1/chat/history/{id}` | GET | Get chat history for transcription |
| `getTranscription` | `/api/v1/transcriptions/{id}` | GET | Get transcription by ID |
| `getAllTranscriptions` | `/api/v1/transcriptions/` | GET | Get all transcriptions |

### TypeScript Interfaces

Type-safe API integration with TypeScript interfaces:

```typescript
export interface TranscriptionResponse {
  id: number;
  filename: string;
  content: string;
  created_at: string;
}

export interface ChatResponse {
  answer: string;
}

export interface ChatMessageResponse {
  id: number;
  transcription_id: number;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
}

export interface AudioUploadData {
  filename: string;
  mimeType: string;
  content: string; // base64 encoded audio
}
```

## 🎨 Theming

The application supports light and dark mode themes:

- **Theme Provider**: `ThemeProvider` from `next-themes` in `layout.tsx`
- **Theme Toggle**: Button to switch between themes
- **System Preference**: Default theme follows system preference
- **Persistence**: Theme choice is saved in local storage

## 🎭 Styling

The application uses Tailwind CSS with shadcn/ui components:

- **Utility-First**: Using Tailwind's utility classes for styling
- **Responsive Design**: Mobile-first breakpoints
- **Accessible Components**: Built on Radix UI primitives
- **Custom UI**: shadcn/ui components with consistent design language
- **Theme Tokens**: Using CSS variables for theming
- **Typography**: Consistent type scale
- **Spacing**: Consistent spacing scale

## 💻 Development

### Getting Started

1. Clone the repository
2. Navigate to the frontend directory: `cd new-fe-vo`
3. Install dependencies: `npm install` or `pnpm install`
4. Start the development server: `npm run dev`

### Build for Production

1. Build the application: `npm run build`
2. Start the production server: `npm run start`

### Environment Variables

Create a `.env.local` file in the `new-fe-vo` directory:
```
NEXT_PUBLIC_API_URL=http://localhost:8089/api/v1
```

### Browser Support

The application supports all modern browsers (Chrome, Firefox, Safari, Edge).

### Linting and Formatting

The project uses ESLint and Prettier for code quality and formatting.

### Testing

Frontend testing is planned with Jest and React Testing Library.

## 🌐 Deployment

The frontend is designed to be deployed on Vercel or any Next.js-compatible hosting service. For production deployment, set the appropriate environment variables for the API endpoints.

## 🔮 Future Enhancements

- Advanced state management for complex workflows
- More robust error handling
- Loading states and skeletons
- Progressive Web App (PWA) features
- Responsive design improvements for mobile users
- Accessibility improvements
- Internationalization (i18n)
- End-to-end testing 