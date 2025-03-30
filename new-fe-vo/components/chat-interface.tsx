"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { Send } from "lucide-react"

interface ChatInterfaceProps {
  messages: Array<{
    role: "user" | "assistant"
    content: string
    isStreaming?: boolean
  }>
  onSendMessage: (message: string) => void
  isDisabled?: boolean
  transcriptionId?: number
}

// Helper function to clean markdown formatting
const cleanMarkdownFormatting = (text: string): string => {
  if (!text) return "";
  
  return text
    .replace(/\*\*\*(.*?)\*\*\*/g, '$1') // Remove bold italic
    .replace(/\*\*(.*?)\*\*/g, '$1')     // Remove bold
    .replace(/\*(.*?)\*/g, '$1')         // Remove italic
    .replace(/^#+\s+/gm, '')             // Remove headers
    .replace(/`(.*?)`/g, '$1')           // Remove inline code
    .replace(/~~(.*?)~~/g, '$1')         // Remove strikethrough
    .replace(/^\d+\.\s+/gm, '')          // Remove numbered lists
    .replace(/^-\s+/gm, '')              // Remove bullet points
    .replace(/\[(.*?)\]\((.*?)\)/g, '$1'); // Remove links but keep text
};

export function ChatInterface({
  messages,
  onSendMessage,
  isDisabled = false,
  transcriptionId
}: ChatInterfaceProps) {
  const [message, setMessage] = useState("")
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (message.trim() && !isDisabled) {
      onSendMessage(message.trim())
      setMessage("")
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  return (
    <Card className="flex flex-col h-[calc(100vh-8rem)] overflow-hidden">
      <div className="px-4 py-3 border-b bg-card sticky top-0">
        <h2 className="text-lg font-medium">Chat with AI</h2>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="h-full flex items-center justify-center">
            <div className="text-center text-muted-foreground space-y-2">
              <p>Ask questions about the transcribed audio</p>
            </div>
          </div>
        ) : (
          messages.map((msg, i) => (
            <div
              key={i}
              className={`flex ${
                msg.role === "user" ? "justify-end" : "justify-start"
              }`}
            >
              <div
                className={`max-w-[80%] px-4 py-3 rounded-lg ${
                  msg.role === "user"
                    ? "bg-primary text-primary-foreground"
                    : "bg-muted"
                }`}
              >
                {msg.content ? (
                  <div className="whitespace-pre-wrap">
                    {msg.role === "assistant" ? cleanMarkdownFormatting(msg.content) : msg.content}
                  </div>
                ) : (
                  msg.isStreaming && (
                    <div className="flex space-x-2">
                      <div className="w-2 h-2 rounded-full bg-current animate-bounce" />
                      <div className="w-2 h-2 rounded-full bg-current animate-bounce [animation-delay:-.3s]" />
                      <div className="w-2 h-2 rounded-full bg-current animate-bounce [animation-delay:-.5s]" />
                    </div>
                  )
                )}
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 border-t mt-auto">
        <form onSubmit={handleSubmit} className="flex space-x-2">
          <Textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={
              isDisabled
                ? "Upload an audio file to start chatting"
                : "Ask a question about the transcription..."
            }
            disabled={isDisabled}
            className="min-h-12 resize-none"
          />
          <Button
            type="submit"
            size="icon"
            disabled={isDisabled || !message.trim()}
          >
            <Send className="h-4 w-4" />
          </Button>
        </form>
      </div>
    </Card>
  )
}

