import React, { useState, useRef } from 'react';
import { Volume2, VolumeX, Play, Pause, Loader } from 'lucide-react';

const VoiceOutput = ({ audioData, text, autoPlay = false, onPlay, onPause }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const audioRef = useRef(null);

  const playAudio = async () => {
    try {
      setIsLoading(true);
      setError(null);
      
      if (!audioData) {
        setError('No audio data available');
        return;
      }
      
      // Convert base64 to blob
      const byteCharacters = atob(audioData);
      const byteNumbers = new Array(byteCharacters.length);
      for (let i = 0; i < byteCharacters.length; i++) {
        byteNumbers[i] = byteCharacters.charCodeAt(i);
      }
      const byteArray = new Uint8Array(byteNumbers);
      const blob = new Blob([byteArray], { type: 'audio/mpeg' });
      
      const audioUrl = URL.createObjectURL(blob);
      
      if (audioRef.current) {
        audioRef.current.src = audioUrl;
        audioRef.current.play();
        setIsPlaying(true);
        onPlay?.();
      }
      
    } catch (err) {
      setError('Failed to play audio');
      console.error('Audio playback error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const pauseAudio = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      setIsPlaying(false);
      onPause?.();
    }
  };

  const handleAudioEnded = () => {
    setIsPlaying(false);
    onPause?.();
  };

  const handleClick = () => {
    if (isLoading) return;
    
    if (isPlaying) {
      pauseAudio();
    } else {
      playAudio();
    }
  };

  return (
    <div className="flex items-center space-x-2">
      <button
        onClick={handleClick}
        disabled={isLoading || !audioData}
        className={`p-2 rounded-full transition-all duration-200 ${
          isPlaying
            ? 'bg-orange-500 hover:bg-orange-600 text-white'
            : 'bg-green-500 hover:bg-green-600 text-white'
        } ${
          isLoading || !audioData
            ? 'opacity-50 cursor-not-allowed'
            : 'cursor-pointer'
        }`}
        title={isPlaying ? 'Pause Audio' : 'Play Audio'}
      >
        {isLoading ? (
          <Loader className="w-4 h-4 animate-spin" />
        ) : isPlaying ? (
          <Pause className="w-4 h-4" />
        ) : (
          <Play className="w-4 h-4" />
        )}
      </button>
      
      {text && (
        <span className="text-sm text-gray-600 max-w-xs truncate">
          {text}
        </span>
      )}
      
      {error && (
        <div className="text-red-500 text-sm">{error}</div>
      )}
      
      <audio
        ref={audioRef}
        onEnded={handleAudioEnded}
        onError={() => setError('Audio playback failed')}
        style={{ display: 'none' }}
      />
    </div>
  );
};

export default VoiceOutput;
