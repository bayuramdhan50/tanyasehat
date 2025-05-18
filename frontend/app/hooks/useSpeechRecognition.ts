'use client';

/**
 * Utilitas untuk pengenalan suara
 * Terintegrasi dengan Web Speech API
 */

import { useState, useEffect, useCallback } from 'react';

interface UseSpeechRecognitionProps {
  onResult?: (text: string) => void;
  onError?: (error: string) => void;
  language?: string;
}

interface SpeechRecognitionHook {
  isListening: boolean;
  startListening: () => void;
  stopListening: () => void;
  hasSupport: boolean;
}

// Hook khusus untuk pengenalan suara
const useSpeechRecognition = ({
  onResult = () => {},
  onError = () => {},
  language = 'id-ID'
}: UseSpeechRecognitionProps = {}): SpeechRecognitionHook => {
  const [isListening, setIsListening] = useState(false);
  const [recognition, setRecognition] = useState<any>(null);
  const [hasSupport, setHasSupport] = useState(false);
  useEffect(() => {
    if (typeof window === 'undefined') return;

    // Cek apakah browser mendukung Web Speech API
    const SpeechRecognitionAPI = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition;
    
    if (!SpeechRecognitionAPI) {
      setHasSupport(false);
      return;
    }

    setHasSupport(true);
    const recognitionInstance = new SpeechRecognitionAPI();
    
    recognitionInstance.lang = language;
    recognitionInstance.continuous = true;
    recognitionInstance.interimResults = true;
    
    recognitionInstance.onresult = (event: any) => {
      const transcript = Array.from(event.results)
        .map((result: any) => result[0])
        .map((result: any) => result.transcript)
        .join('');
      
      onResult(transcript);
    };
    
    recognitionInstance.onerror = (event: any) => {
      onError(`Error: ${event.error}`);
      setIsListening(false);
    };
    
    recognitionInstance.onend = () => {
      setIsListening(false);
    };
    
    setRecognition(recognitionInstance);
    
    return () => {
      if (recognitionInstance) {
        recognitionInstance.stop();
      }
    };
    // Only depend on the language - we handle callbacks internally to avoid dependency cycles
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [language]);

  const startListening = useCallback(() => {
    if (!recognition) return;
    
    recognition.start();
    setIsListening(true);
  }, [recognition]);

  const stopListening = useCallback(() => {
    if (!recognition) return;
    
    recognition.stop();
    setIsListening(false);
  }, [recognition]);

  return {
    isListening,
    startListening,
    stopListening,
    hasSupport
  };
};

export default useSpeechRecognition;
