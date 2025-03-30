"use client"

import { useState, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Progress } from "@/components/ui/progress"
import { X } from "lucide-react"
import { uploadAudioForTranscription } from "@/lib/api"

interface FileUploadProps {
  onUploadStart: () => void
  onTranscriptionComplete: (result: { content: string; id: number } | string) => void
}

export function FileUpload({ onUploadStart, onTranscriptionComplete }: FileUploadProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [uploadProgress, setUploadProgress] = useState<number>(0)
  const [isUploading, setIsUploading] = useState<boolean>(false)
  const [error, setError] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] || null
    setSelectedFile(file)
    setError(null)
    
    // Auto-start upload when file is selected
    if (file) {
      handleUpload(file);
    }
  }

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    e.stopPropagation()
  }

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    e.stopPropagation()
    
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0]
      // Check if the file is an audio file
      if (file.type.startsWith('audio/')) {
        setSelectedFile(file)
        setError(null)
        // Auto-start upload when file is dropped
        handleUpload(file);
      } else {
        setError("Please upload an audio file.")
      }
    }
  }

  const handleUpload = async (file?: File) => {
    // Use the passed file if available, otherwise use the selected file
    const fileToUpload = file || selectedFile
    
    // If no file is available, trigger the file input click
    if (!fileToUpload) {
      fileInputRef.current?.click();
      return;
    }

    setIsUploading(true)
    setUploadProgress(0)
    onUploadStart()
    
    // Simulate upload progress
    const progressInterval = setInterval(() => {
      setUploadProgress(prev => {
        const newProgress = prev + Math.random() * 10
        return newProgress >= 90 ? 90 : newProgress // Cap at 90% until actual completion
      })
    }, 500)

    try {
      // Convert file to base64
      const base64 = await new Promise<string>((resolve, reject) => {
        const reader = new FileReader()
        reader.readAsDataURL(fileToUpload)
        reader.onload = () => {
          const result = reader.result as string
          const base64String = result.split(',')[1] // Remove the data URL prefix
          resolve(base64String)
        }
        reader.onerror = error => reject(error)
      })

      // Call API to upload and transcribe
      const response = await uploadAudioForTranscription({
        filename: fileToUpload.name,
        mimeType: fileToUpload.type,
        content: base64
      })

      clearInterval(progressInterval)
      setUploadProgress(100)
      
      setTimeout(() => {
        setIsUploading(false)
        onTranscriptionComplete(response)
      }, 500)
    } catch (err) {
      clearInterval(progressInterval)
      setError("Failed to upload and transcribe the file. Please try again.")
      console.error(err)
      setIsUploading(false)
    }
  }

  const clearSelectedFile = () => {
    setSelectedFile(null)
    if (fileInputRef.current) {
      fileInputRef.current.value = ""
    }
  }

  return (
    <div className="flex flex-col space-y-3">
      <div
        className={`border ${isUploading ? "border-solid" : "border-dashed"} rounded-md p-4 flex flex-col items-center justify-center cursor-pointer transition-colors ${
          isUploading ? "bg-muted" : "hover:bg-muted/50"
        }`}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onClick={() => !isUploading && fileInputRef.current?.click()}
      >
        <input
          type="file"
          ref={fileInputRef}
          className="hidden"
          accept="audio/*"
          onChange={handleFileChange}
          disabled={isUploading}
        />
        
        <div className="text-center">
          <p className="text-sm font-medium mb-1">
            {isUploading
              ? "Uploading..."
              : selectedFile
              ? selectedFile.name
              : "Drag and drop an audio file or click to browse"}
          </p>
          <p className="text-xs text-muted-foreground">
            Supports MP3, WAV, M4A, and FLAC
          </p>
        </div>
      </div>

      {selectedFile && !isUploading && (
        <div className="flex items-center justify-between p-2 border rounded-md">
          <span className="truncate max-w-[300px] text-sm">{selectedFile.name}</span>
          <Button variant="ghost" size="sm" onClick={clearSelectedFile}>
            <X className="w-3 h-3" />
          </Button>
        </div>
      )}

      {isUploading && (
        <div className="space-y-1">
          <Progress value={uploadProgress} className="w-full h-2" />
          <p className="text-xs text-muted-foreground text-right">
            {Math.round(uploadProgress)}%
          </p>
        </div>
      )}

      {error && <p className="text-destructive text-xs">{error}</p>}

      <Button 
        onClick={() => handleUpload()} 
        disabled={isUploading}
        className="w-full h-8 text-sm"
        size="sm"
      >
        {isUploading ? "Transcribing..." : "Upload & Transcribe"}
      </Button>
    </div>
  )
}

