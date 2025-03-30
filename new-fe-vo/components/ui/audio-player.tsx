"use client"

import { useRef, useState, useEffect } from "react"
import { Play, Pause, Volume2, VolumeX } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Slider } from "@/components/ui/slider"
import { cn } from "@/lib/utils"

interface AudioPlayerProps {
  src: string
  className?: string
}

export function AudioPlayer({ src, className }: AudioPlayerProps) {
  const audioRef = useRef<HTMLAudioElement>(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentTime, setCurrentTime] = useState(0)
  const [duration, setDuration] = useState(0)
  const [isMuted, setIsMuted] = useState(false)
  const [volume, setVolume] = useState(1)

  // Update duration when audio is loaded
  useEffect(() => {
    const audio = audioRef.current
    if (!audio) return

    const setAudioData = () => {
      setDuration(audio.duration || 0)
    }

    const handleTimeUpdate = () => {
      setCurrentTime(audio.currentTime || 0)
    }

    const handleEnded = () => {
      setIsPlaying(false)
      setCurrentTime(0)
    }

    // Add event listeners
    audio.addEventListener('loadedmetadata', setAudioData)
    audio.addEventListener('timeupdate', handleTimeUpdate)
    audio.addEventListener('ended', handleEnded)

    // Set initial data if already loaded
    if (audio.readyState >= 2) {
      setAudioData()
    }

    return () => {
      audio.removeEventListener('loadedmetadata', setAudioData)
      audio.removeEventListener('timeupdate', handleTimeUpdate)
      audio.removeEventListener('ended', handleEnded)
    }
  }, [audioRef, src])

  // Format time to MM:SS
  const formatTime = (time: number) => {
    if (isNaN(time) || !isFinite(time)) return "00:00"
    const minutes = Math.floor(time / 60)
    const seconds = Math.floor(time % 60)
    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`
  }

  // Handle play/pause
  const togglePlayPause = () => {
    const audio = audioRef.current
    if (!audio) return

    if (isPlaying) {
      audio.pause()
    } else {
      audio.play()
    }
    setIsPlaying(!isPlaying)
  }

  // Handle timeline change
  const handleTimelineChange = (value: number[]) => {
    const audio = audioRef.current
    if (!audio) return

    const newTime = value[0]
    audio.currentTime = newTime
    setCurrentTime(newTime)
  }

  // Handle volume change
  const handleVolumeChange = (value: number[]) => {
    const audio = audioRef.current
    if (!audio) return

    const newVolume = value[0]
    audio.volume = newVolume
    setVolume(newVolume)
    setIsMuted(newVolume === 0)
  }

  // Toggle mute
  const toggleMute = () => {
    const audio = audioRef.current
    if (!audio) return

    const newMuteState = !isMuted
    audio.muted = newMuteState
    setIsMuted(newMuteState)
  }

  return (
    <div className={cn("flex flex-col space-y-2 w-full", className)}>
      <audio ref={audioRef} src={src} preload="metadata" className="hidden" />
      
      <div className="flex items-center space-x-2">
        <Button
          variant="ghost"
          size="icon"
          className="h-8 w-8"
          onClick={togglePlayPause}
        >
          {isPlaying ? (
            <Pause className="h-4 w-4" />
          ) : (
            <Play className="h-4 w-4" />
          )}
          <span className="sr-only">{isPlaying ? 'Pause' : 'Play'}</span>
        </Button>

        <div className="flex items-center flex-1 space-x-2">
          <span className="text-sm tabular-nums w-12 text-center">
            {formatTime(currentTime)}
          </span>
          
          <Slider
            value={[isNaN(currentTime) || !isFinite(currentTime) ? 0 : currentTime]}
            max={isNaN(duration) || !isFinite(duration) || duration <= 0 ? 100 : duration}
            step={0.1}
            onValueChange={handleTimelineChange}
            className="flex-1"
          />
          
          <span className="text-sm tabular-nums w-12 text-center">
            {formatTime(duration)}
          </span>
        </div>

        <div className="flex items-center">
          <Button
            variant="ghost"
            size="icon"
            className="h-8 w-8"
            onClick={toggleMute}
          >
            {isMuted ? (
              <VolumeX className="h-4 w-4" />
            ) : (
              <Volume2 className="h-4 w-4" />
            )}
            <span className="sr-only">{isMuted ? 'Unmute' : 'Mute'}</span>
          </Button>
          
          <Slider
            value={[isMuted ? 0 : volume]}
            max={1}
            step={0.01}
            onValueChange={handleVolumeChange}
            className="w-20"
          />
        </div>
      </div>
    </div>
  )
} 