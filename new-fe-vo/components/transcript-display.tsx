"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"

interface TranscriptDisplayProps {
  transcript: string
  isLoading: boolean
}

export function TranscriptDisplay({ transcript, isLoading }: TranscriptDisplayProps) {
  return (
    <Card className="w-full flex-1 flex flex-col max-h-full">
      <CardHeader className="pb-2">
        <CardTitle>Transcript</CardTitle>
      </CardHeader>
      <CardContent className="overflow-y-auto flex-1">
        {isLoading ? (
          <div className="space-y-2">
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-full" />
            <Skeleton className="h-4 w-[95%]" />
            <Skeleton className="h-4 w-[90%]" />
            <Skeleton className="h-4 w-[85%]" />
          </div>
        ) : transcript ? (
          <div className="prose prose-sm md:prose-base max-w-none">
            {transcript.split('\n').map((paragraph, i) => (
              paragraph.trim() ? (
                <p key={i} className="mb-3">{paragraph}</p>
              ) : (
                <br key={i} />
              )
            ))}
          </div>
        ) : (
          <div className="text-center py-8 text-muted-foreground">
            <p>No transcript available. Upload an audio file to see the transcript.</p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}

