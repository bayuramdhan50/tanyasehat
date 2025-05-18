/**
 * Komponen InputForm untuk menerima input gejala dari pengguna
 * Mengirim input ke API backend untuk diproses
 */
'use client'

import { useState, useCallback, useRef, useEffect } from 'react';
import axios from 'axios';
import useSpeechRecognition from '../hooks/useSpeechRecognition';
import { debounce } from 'lodash'; // Install dengan: npm install lodash

interface InputFormProps {
  onResult: (data: any) => void;
  onLoading: (loading: boolean) => void;
}

export default function InputForm({ onResult, onLoading }: InputFormProps) {
  const [symptoms, setSymptoms] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [retryCount, setRetryCount] = useState(0);
  const [maxRetries] = useState(3);
  const [apiUrl, setApiUrl] = useState('http://localhost:5000/api/predict');
  const [connectionStatus, setConnectionStatus] = useState<'idle' | 'connecting' | 'connected' | 'failed'>('idle');
  const formRef = useRef<HTMLFormElement>(null);
  const [examples, setExamples] = useState<string[]>([
    'Saya mengalami demam tinggi dan sakit kepala selama 3 hari',
    'Saya batuk kering, sesak napas, dan nyeri dada sejak seminggu yang lalu',
    'Perut saya sakit dan saya sering muntah sejak kemarin',
    'Saya mengalami pusing, mual, dan pandangan kabur',
    'Tenggorokan saya sakit dan sulit menelan sejak 2 hari yang lalu'
  ]);
  
  // Check server connection status on mount
  useEffect(() => {
    checkServerConnection();
  }, []);

  const checkServerConnection = useCallback(async () => {
    try {
      setConnectionStatus('connecting');
      const response = await axios.get('http://localhost:5000/api/health');
      if (response.data.status === 'healthy') {
        setConnectionStatus('connected');
      } else {
        setConnectionStatus('failed');
      }
    } catch (error) {
      console.error('Server connection check failed:', error);
      setConnectionStatus('failed');
    }
  }, []);
  // Gunakan custom hook untuk speech recognition
  const onSpeechResult = useCallback((text: string) => {
    setSymptoms(text);
  }, []);

  const onSpeechError = useCallback((error: string) => {
    console.error('Speech recognition error:', error);
    setError('Terjadi kesalahan pada pengenalan suara. Silakan coba lagi.');
  }, []);

  const { 
    isListening, 
    startListening, 
    stopListening, 
    hasSupport 
  } = useSpeechRecognition({
    onResult: onSpeechResult,
    onError: onSpeechError,
    language: 'id-ID'
  });

  const toggleListening = () => {
    if (!hasSupport) {
      setError('Maaf, browser Anda tidak mendukung pengenalan suara.');
      return;
    }
    
    if (isListening) {
      stopListening();
    } else {
      setError('');
      startListening();
    }
  };

  const useExample = (example: string) => {
    setSymptoms(example);
  };

  // Enhanced submit handler with retry logic
  const debouncedSubmit = useCallback(
    debounce(async (text: string) => {
      if (isSubmitting) return;
      
      try {
        setIsSubmitting(true);
        onLoading(true);
        
        // Gunakan AbortController untuk membatalkan request jika terlalu lama
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 15000); // 15 detik timeout
        
        const response = await axios.post(apiUrl, 
          { text },
          { 
            signal: controller.signal,
            timeout: 15000 // Explicit timeout setting
          }
        );
        
        clearTimeout(timeoutId);
        
        // Reset retry count on success
        setRetryCount(0);
        setConnectionStatus('connected');
        
        // Log data for debugging
        console.log('API Response:', response.data);
        
        onResult(response.data);
      } catch (error: any) {
        console.error('Error:', error);
        
        // Handle different error cases with more specific messages
        if (error.name === 'AbortError' || error.name === 'CanceledError') {
          setError('Permintaan timeout. Server mungkin sedang sibuk, silakan coba lagi.');
        } else if (error.response) {
          // Server responded with an error status
          setError(`Error ${error.response.status}: ${
            error.response.data.message || 
            error.response.data.error || 
            'Terjadi kesalahan pada server'
          }`);
        } else if (error.request) {
          // Request was made but no response received
          setConnectionStatus('failed');
          setError('Tidak dapat terhubung ke server. Server mungkin sedang offline atau restart.');
        } else {
          // Error in request setup
          setError('Terjadi kesalahan saat menghubungi server. Silakan coba lagi.');
        }
        
        // Auto-retry logic for certain errors (network/connection issues)
        if (error.request && retryCount < maxRetries) {
          setRetryCount(prev => prev + 1);
          setTimeout(() => {
            setError(`Mencoba menghubungi server kembali... (Percobaan ${retryCount + 1}/${maxRetries})`);
            debouncedSubmit(text);
          }, 2000 * (retryCount + 1)); // Exponential backoff
        }
      } finally {
        setIsSubmitting(false);
        onLoading(false);
      }
    }, 500),
    [onLoading, onResult, isSubmitting, retryCount, maxRetries, apiUrl]
  );

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!symptoms.trim()) {
      setError('Silakan masukkan gejala yang Anda alami');
      return;
    }
    
    setError('');
    
    // Gunakan debounced submit
    debouncedSubmit(symptoms);
  };

  // Add manual retry button
  const handleRetry = () => {
    if (symptoms.trim()) {
      setError('Mencoba mengirim kembali...');
      debouncedSubmit(symptoms);
    }
  };

  return (
    <form ref={formRef} onSubmit={handleSubmit} className="w-full max-w-2xl mx-auto">
      {connectionStatus === 'failed' && (
        <div className="mb-4 p-3 bg-yellow-100 dark:bg-yellow-900/30 text-yellow-800 dark:text-yellow-200 rounded-lg">
          <p className="text-sm font-medium">Server tidak terhubung</p>
          <p className="text-xs mt-1">Pastikan server backend berjalan di http://localhost:5000</p>
          <button 
            type="button"
            onClick={checkServerConnection}
            className="mt-2 text-xs bg-yellow-200 dark:bg-yellow-800 px-2 py-1 rounded hover:bg-yellow-300 dark:hover:bg-yellow-700"
          >
            Periksa Koneksi
          </button>
        </div>
      )}

      <div className="mb-4">
        <label 
          htmlFor="symptoms" 
          className="block text-sm font-medium mb-2"
        >
          Deskripsikan gejala yang Anda alami:
        </label>
        <div className="relative">
          <textarea
            id="symptoms"
            className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none min-h-[120px] bg-white dark:bg-gray-800 text-gray-800 dark:text-white"
            placeholder="Contoh: Saya mengalami sakit kepala, demam, dan batuk kering sejak 3 hari yang lalu..."
            value={symptoms}
            onChange={(e) => setSymptoms(e.target.value)}
            rows={5}
            disabled={isSubmitting}
          />
          <button
            type="button"
            onClick={toggleListening}
            className={`absolute bottom-3 right-3 p-2 rounded-full ${isListening ? 'bg-red-500 animate-pulse' : 'bg-blue-500'} ${isSubmitting ? 'opacity-50 cursor-not-allowed' : ''}`}
            title={isListening ? 'Klik untuk berhenti merekam' : 'Klik untuk mulai merekam suara'}
            disabled={isSubmitting}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5 text-white"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d={isListening 
                  ? "M21 12a9 9 0 11-18 0 9 9 0 0118 0z M9 10a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z" 
                  : "M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"}
              />
            </svg>
          </button>
        </div>
        {isListening && (
          <p className="mt-2 text-sm text-green-600">
            Mendengarkan... Bicara dengan jelas tentang gejala yang Anda alami.
          </p>
        )}
        {!hasSupport && (
          <p className="mt-2 text-sm text-yellow-500">
            Browser Anda tidak mendukung fitur pengenalan suara.
          </p>
        )}
        {error && (
          <div className="mb-4 p-3 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-300 rounded-lg">
            <p className="text-sm">{error}</p>
            {error.includes('server') && (
              <button 
                type="button" 
                onClick={handleRetry}
                className="mt-2 text-xs bg-red-100 dark:bg-red-800 px-2 py-1 rounded hover:bg-red-200 dark:hover:bg-red-700"
                disabled={isSubmitting}
              >
                Coba Lagi
              </button>
            )}
          </div>
        )}
        
        {/* Contoh gejala */}
        <div className="mt-4">
          <p className="text-xs text-gray-500 mb-2">Contoh deskripsi gejala:</p>
          <div className="flex flex-wrap gap-1">
            {examples.map((example, index) => (
              <button
                key={index}
                type="button"
                onClick={() => useExample(example)}
                className="text-xs px-2 py-1 bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600 rounded transition-colors truncate max-w-[48%]"
                title={example}
                disabled={isSubmitting}
              >
                {example.length > 30 ? example.substring(0, 30) + '...' : example}
              </button>
            ))}
          </div>
        </div>
      </div>
      <button
        type="submit"
        className={`w-full ${isSubmitting ? 'bg-gray-400 cursor-not-allowed' : connectionStatus === 'failed' ? 'bg-yellow-500 hover:bg-yellow-600' : 'bg-blue-600 hover:bg-blue-700'} text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200`}
        disabled={isSubmitting || connectionStatus === 'connecting'}
      >
        {isSubmitting ? 'Memproses...' : connectionStatus === 'connecting' ? 'Memeriksa Koneksi...' : connectionStatus === 'failed' ? 'Coba Kirim (Server Tidak Terhubung)' : 'Analisis Gejala'}
      </button>
    </form>
  );
}

