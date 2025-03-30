"use client"

import { useState } from "react"
import { FileUpload } from "@/components/file-upload"
import { TranscriptDisplay } from "@/components/transcript-display"
import { ChatInterface } from "@/components/chat-interface"
import { ThemeToggle } from "@/components/theme-toggle"
import { uploadAudioForTranscription, chatWithTranscription } from "@/lib/api"

export default function Home() {
  const [transcript, setTranscript] = useState<string>("")
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [chatMessages, setChatMessages] = useState<Array<{ role: "user" | "assistant"; content: string; isStreaming?: boolean }>>([])
  const [transcriptionId, setTranscriptionId] = useState<number | null>(null)

  // Handle transcription completion
  const handleTranscriptionComplete = (text: string, id?: number) => {
    setTranscript(text)
    setIsLoading(false)
    if (id) {
      setTranscriptionId(id)
    }
    
    // Reset chat messages when a new transcription is ready
    setChatMessages([])
  }
  
  // Handle file upload start
  const handleUploadStart = () => {
    setIsLoading(true)
    setTranscript("")
  }
  
  // Handle chat submission
  const handleChatSubmit = async (message: string) => {
    if (!transcriptionId) return
    
    // Add user message
    setChatMessages((prev) => [...prev, { role: "user", content: message }])
    
    // Add loading message for assistant
    setChatMessages((prev) => [...prev, { role: "assistant", content: "", isStreaming: true }])
    
    try {
      // Get response from API
      const response = await chatWithTranscription(transcriptionId, message)
      
      // Update assistant message with response
      setChatMessages((prev) => [
        ...prev.slice(0, -1),
        { role: "assistant", content: response }
      ])
    } catch (error) {
      console.error("Error sending message:", error)
      
      // Update assistant message with error
      setChatMessages((prev) => [
        ...prev.slice(0, -1),
        { role: "assistant", content: "Sorry, there was an error processing your request." }
      ])
    }
  }

  return (
    <main className="min-h-screen w-full px-3 py-4 md:px-6 lg:px-8 max-w-[1600px] mx-auto">
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-xl md:text-2xl font-bold">Audio Transcription & Chat</h1>
        <ThemeToggle />
      </div>
      
      <div className="grid w-full grid-cols-1 lg:grid-cols-3 gap-4 h-[calc(100vh-7rem)]">
        <div className="lg:col-span-2 flex flex-col space-y-4 overflow-y-auto pr-2">
          <div className="space-y-3">
            <h2 className="text-lg font-semibold">Upload Audio File</h2>
            <FileUpload
              onUploadStart={handleUploadStart}
              onTranscriptionComplete={(result) => {
                if (typeof result === 'object' && result.content && result.id) {
                  handleTranscriptionComplete(result.content, result.id)
                } else {
                  handleTranscriptionComplete(String(result))
                }
              }}
            />
          </div>

          <TranscriptDisplay transcript={transcript} isLoading={isLoading} />
        </div>

        <div className="lg:col-span-1 h-full">
          <ChatInterface 
            messages={chatMessages} 
            onSendMessage={handleChatSubmit} 
            isDisabled={!transcript}
            transcriptionId={transcriptionId || undefined}
          />
        </div>
      </div>
    </main>
  )
}

