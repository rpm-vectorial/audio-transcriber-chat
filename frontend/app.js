// API base URL - change this when deploying
const API_BASE_URL = 'http://localhost:8000/api/v1';

// DOM Elements
const uploadForm = document.getElementById('upload-form');
const audioFileInput = document.getElementById('audio-file');
const uploadBtn = document.getElementById('upload-btn');
const uploadStatus = document.getElementById('upload-status');
const transcriptionSection = document.getElementById('transcription-section');
const transcriptionContent = document.getElementById('transcription-content');
const chatMessages = document.getElementById('chat-messages');
const messageInput = document.getElementById('message-input');
const sendBtn = document.getElementById('send-btn');

// Voice recording elements
const startRecordingBtn = document.getElementById('start-recording-btn');
const stopRecordingBtn = document.getElementById('stop-recording-btn');
const transcribeRecordingBtn = document.getElementById('transcribe-recording-btn');
const recordingIndicator = document.getElementById('recording-indicator');
const recordingTime = document.getElementById('recording-time');
const voiceStatus = document.getElementById('voice-status');
const audioPlaybackContainer = document.getElementById('audio-playback-container');
const audioPlayback = document.getElementById('audio-playback');

// Current transcription ID
let currentTranscriptionId = null;

// Voice recording variables
let mediaRecorder = null;
let audioChunks = [];
let recordingStartTime = null;
let recordingTimer = null;
let recordedBlob = null;

// Event listeners
document.addEventListener('DOMContentLoaded', initializeApp);

/**
 * Initialize the application
 */
function initializeApp() {
    uploadForm.addEventListener('submit', handleFileUpload);
    startRecordingBtn.addEventListener('click', startRecording);
    stopRecordingBtn.addEventListener('click', stopRecording);
    transcribeRecordingBtn.addEventListener('click', transcribeRecording);
    sendBtn.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', handleMessageInputKeypress);
}

/**
 * Handle keypress in message input
 * @param {KeyboardEvent} e - Keyboard event
 */
function handleMessageInputKeypress(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
}

/**
 * Handle file upload
 * @param {Event} e - Form submit event
 */
async function handleFileUpload(e) {
    e.preventDefault();
    
    const file = audioFileInput.files[0];
    if (!file) {
        showError('Please select an audio file');
        return;
    }
    
    // Disable upload button and show status
    setUploadingState(true);
    
    try {
        const data = await uploadAndTranscribeFile(file);
        handleTranscriptionSuccess(data);
    } catch (error) {
        console.error('Error:', error);
        showError(`Error: ${error.message}`);
    } finally {
        setUploadingState(false);
    }
}

/**
 * Set the uploading state UI
 * @param {boolean} isUploading - Whether a file is being uploaded
 */
function setUploadingState(isUploading) {
    uploadBtn.disabled = isUploading;
    if (isUploading) {
        uploadStatus.innerHTML = 'Uploading and transcribing... This may take a moment.';
        uploadStatus.className = '';
    }
}

/**
 * Upload and transcribe a file
 * @param {File} file - The file to upload
 * @returns {Promise<Object>} The transcription data
 */
async function uploadAndTranscribeFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await fetch(`${API_BASE_URL}/transcriptions/`, {
        method: 'POST',
        body: formData
    });
    
    if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
    }
    
    return await response.json();
}

/**
 * Start voice recording
 */
async function startRecording() {
    try {
        // Reset recording state
        audioChunks = [];
        recordedBlob = null;
        audioPlaybackContainer.classList.add('hidden');
        transcribeRecordingBtn.disabled = true;
        
        // Get microphone access
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        // Create media recorder
        mediaRecorder = new MediaRecorder(stream);
        
        // Set up event handlers
        mediaRecorder.ondataavailable = (e) => {
            if (e.data.size > 0) {
                audioChunks.push(e.data);
            }
        };
        
        mediaRecorder.onstop = () => {
            // Create audio blob
            recordedBlob = new Blob(audioChunks, { type: 'audio/webm' });
            
            // Create audio URL and set to audio element
            const audioURL = URL.createObjectURL(recordedBlob);
            audioPlayback.src = audioURL;
            
            // Show audio playback and transcribe button
            audioPlaybackContainer.classList.remove('hidden');
            transcribeRecordingBtn.disabled = false;
            
            // Clear recording timer
            clearInterval(recordingTimer);
            
            // Show recording duration
            const duration = calculateRecordingDuration();
            voiceStatus.innerHTML = `Recording completed (${duration})`;
            voiceStatus.className = 'success';
            
            // Reset recording state
            recordingIndicator.classList.add('hidden');
        };
        
        // Start recording
        mediaRecorder.start(100); // Record in 100ms chunks
        
        // Update UI
        startRecordingBtn.disabled = true;
        stopRecordingBtn.disabled = false;
        recordingIndicator.classList.remove('hidden');
        voiceStatus.innerHTML = 'Recording started... speak now';
        voiceStatus.className = '';
        
        // Start recording timer
        recordingStartTime = new Date();
        recordingTimer = setInterval(updateRecordingTimer, 1000);
        
    } catch (error) {
        console.error('Error starting recording:', error);
        showVoiceError(`Microphone access denied: ${error.message}`);
    }
}

/**
 * Stop voice recording
 */
function stopRecording() {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
        
        // Stop all microphone tracks
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
        
        // Update UI
        startRecordingBtn.disabled = false;
        stopRecordingBtn.disabled = true;
    }
}

/**
 * Update recording timer
 */
function updateRecordingTimer() {
    const duration = calculateRecordingDuration();
    recordingTime.textContent = duration;
}

/**
 * Calculate recording duration
 * @returns {string} Formatted duration string (MM:SS)
 */
function calculateRecordingDuration() {
    const now = new Date();
    const diff = Math.floor((now - recordingStartTime) / 1000);
    const minutes = Math.floor(diff / 60).toString().padStart(2, '0');
    const seconds = (diff % 60).toString().padStart(2, '0');
    return `${minutes}:${seconds}`;
}

/**
 * Transcribe recorded audio
 */
async function transcribeRecording() {
    if (!recordedBlob) {
        showVoiceError('No recording available to transcribe');
        return;
    }
    
    // Update UI
    transcribeRecordingBtn.disabled = true;
    voiceStatus.innerHTML = 'Transcribing... This may take a moment.';
    voiceStatus.className = '';
    
    try {
        // Convert blob to base64
        const base64Data = await blobToBase64(recordedBlob);
        
        // Send to server for transcription
        const data = await submitAudioForTranscription(base64Data);
        
        // If save_to_db was set to true, we would have a transcription ID
        if (data.transcription_id) {
            // Handle like a regular file upload success
            const fullData = {
                id: data.transcription_id,
                content: data.transcription,
                created_at: new Date().toISOString(),
                filename: 'voice-recording.webm'
            };
            handleTranscriptionSuccess(fullData);
        } else {
            // Just show the transcription without saving to DB
            transcriptionContent.textContent = data.transcription;
            transcriptionSection.style.display = 'block';
            
            // Clear chat messages if there were any
            chatMessages.innerHTML = '';
            
            // No transcription ID means we can't chat with it
            currentTranscriptionId = null;
        }
        
        // Show success
        voiceStatus.innerHTML = 'Transcription completed!';
        voiceStatus.className = 'success';
        
    } catch (error) {
        console.error('Error:', error);
        showVoiceError(`Error: ${error.message}`);
        transcribeRecordingBtn.disabled = false;
    }
}

/**
 * Convert Blob to Base64
 * @param {Blob} blob - The blob to convert
 * @returns {Promise<string>} Base64 string
 */
function blobToBase64(blob) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => {
            // Remove the prefix (e.g., "data:audio/webm;base64,")
            const base64 = reader.result.split(',')[1];
            resolve(base64);
        };
        reader.onerror = reject;
        reader.readAsDataURL(blob);
    });
}

/**
 * Submit audio for transcription
 * @param {string} base64Data - Base64 encoded audio data
 * @returns {Promise<Object>} Transcription data
 */
async function submitAudioForTranscription(base64Data) {
    const response = await fetch(`${API_BASE_URL}/transcriptions/real-time`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            audio_data: base64Data,
            file_extension: '.webm',
            save_to_db: true // Set to true to enable chat functionality
        })
    });
    
    if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
    }
    
    return await response.json();
}

/**
 * Handle successful transcription
 * @param {Object} data - The transcription data
 */
function handleTranscriptionSuccess(data) {
    // Display transcription
    currentTranscriptionId = data.id;
    transcriptionContent.textContent = data.content;
    transcriptionSection.style.display = 'block';
    
    // Clear chat messages
    chatMessages.innerHTML = '';
    
    // Show success message
    uploadStatus.innerHTML = 'Transcription complete!';
    uploadStatus.className = 'success';
}

/**
 * Send a chat message
 */
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message || !currentTranscriptionId) return;
    
    // Add user message to chat
    addMessageToChat('You', message, 'user-message');
    
    // Clear input
    messageInput.value = '';
    
    try {
        const data = await sendChatRequest(message);
        
        // Add assistant message to chat
        addMessageToChat('Assistant', data.answer, 'assistant-message');
        
        // Scroll to bottom of chat
        scrollChatToBottom();
        
    } catch (error) {
        console.error('Error:', error);
        showError(`Error: ${error.message}`);
    }
}

/**
 * Send a chat request to the API
 * @param {string} message - The message to send
 * @returns {Promise<Object>} The response data
 */
async function sendChatRequest(message) {
    const response = await fetch(`${API_BASE_URL}/chat/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            transcription_id: currentTranscriptionId,
            message: message
        })
    });
    
    if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
    }
    
    return await response.json();
}

/**
 * Add a message to the chat
 * @param {string} sender - The message sender
 * @param {string} content - The message content
 * @param {string} className - The CSS class name for styling
 */
function addMessageToChat(sender, content, className) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${className}`;
    
    const senderDiv = document.createElement('div');
    senderDiv.className = 'message-sender';
    senderDiv.textContent = sender;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;
    
    messageDiv.appendChild(senderDiv);
    messageDiv.appendChild(contentDiv);
    
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    scrollChatToBottom();
}

/**
 * Scroll chat to the bottom
 */
function scrollChatToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

/**
 * Show error message in upload section
 * @param {string} message - The error message
 */
function showError(message) {
    uploadStatus.innerHTML = message;
    uploadStatus.className = 'error';
}

/**
 * Show error message in voice recording section
 * @param {string} message - The error message
 */
function showVoiceError(message) {
    voiceStatus.innerHTML = message;
    voiceStatus.className = 'error';
} 