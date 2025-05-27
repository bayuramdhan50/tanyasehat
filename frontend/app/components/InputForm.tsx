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
  const [showExamples, setShowExamples] = useState(false);
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

  const { isListening, startListening, stopListening } = useSpeechRecognition({
    onResult: onSpeechResult,
    onError: onSpeechError,
    language: 'id-ID'
  });

  const toggleListening = () => {
    if (isListening) {
      stopListening();
    } else {
      setError('');
      startListening();
    }
  };

  // Debounce fungsi submit untuk mencegah multiple submit
  const debouncedSubmit = debounce(async (url, data) => {
    try {
      setIsSubmitting(true);
      onLoading(true);
      
      // Kirim data ke API
      const response = await axios.post(url, data);
      
      if (response.data) {
        // Reset status error
        setError('');
        setRetryCount(0);
        
        // Panggil callback dengan hasil
        onResult(response.data);
      }
    } catch (error: any) {
      console.error('API request error:', error);
      
      // Coba lagi jika belum mencapai batas percobaan
      if (retryCount < maxRetries) {
        setRetryCount(prev => prev + 1);
        setError(`Terjadi kesalahan saat menghubungi server. Mencoba lagi... (${retryCount + 1}/${maxRetries})`);
        setTimeout(() => debouncedSubmit(url, data), 2000); // Tunggu 2 detik sebelum coba lagi
      } else {
        setError('Gagal terhubung ke server setelah beberapa percobaan. Pastikan server backend sedang berjalan.');
      }
    } finally {
      setIsSubmitting(false);
      onLoading(false);
    }
  }, 500);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!symptoms.trim()) {
      setError('Silakan masukkan gejala yang Anda alami.');
      return;
    }
    
    // Reset error
    setError('');
    
    // Kirim data
    debouncedSubmit(apiUrl, { text: symptoms });
  };

  const handleExampleClick = (example: string) => {
    setSymptoms(example);
    setShowExamples(false); // Hide examples after selection
  };

  // Status koneksi server
  const renderConnectionStatus = () => {
    switch (connectionStatus) {
      case 'connecting':
        return <span className="text-xs text-blue-600 dark:text-blue-400 flex items-center">
          <svg className="animate-spin h-3 w-3 mr-1" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          Menghubungkan ke server...
        </span>;
      case 'connected':
        return <span className="text-xs text-green-600 dark:text-green-400 flex items-center">
          <svg className="h-3 w-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7"></path>
          </svg>
          Terhubung ke server
        </span>;
      case 'failed':
        return <span className="text-xs text-red-600 dark:text-red-400 flex items-center">
          <svg className="h-3 w-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
          Tidak dapat terhubung ke server
        </span>;
      default:
        return null;
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      <form ref={formRef} onSubmit={handleSubmit} className="space-y-6">
        <div className="bg-white dark:bg-gray-800 shadow-sm rounded-xl p-6 border border-gray-100 dark:border-gray-700">
          <div className="mb-5">
            <label htmlFor="symptoms" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Deskripsikan gejala yang Anda alami
            </label>
            
            <div className="flex items-center justify-between mb-2">
              <button 
                type="button"
                onClick={() => setShowExamples(!showExamples)}
                className="text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 text-sm font-medium flex items-center"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                {showExamples ? "Sembunyikan contoh" : "Lihat contoh"}
              </button>
              {renderConnectionStatus()}
            </div>

            {showExamples && (
              <div className="mb-4 bg-blue-50 dark:bg-blue-900/20 p-3 rounded-lg text-sm">
                <p className="font-medium text-gray-700 dark:text-gray-300 mb-2">Contoh deskripsi gejala:</p>
                <ul className="space-y-2">
                  {examples.map((example, idx) => (
                    <li key={idx}>
                      <button 
                        type="button" 
                        onClick={() => handleExampleClick(example)}
                        className="text-left text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300 hover:underline w-full"
                      >
                        "{example}"
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            
            <div className="relative">
              <textarea
                id="symptoms"
                name="symptoms"
                value={symptoms}
                onChange={(e) => setSymptoms(e.target.value)}
                placeholder="Contoh: Saya mengalami demam tinggi, sakit kepala, dan nyeri otot sejak 3 hari yang lalu..."
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:text-white dark:placeholder-gray-400 transition-colors"
                rows={4}
                required
              ></textarea>
              
              <button
                type="button"
                onClick={toggleListening}
                className={`absolute right-3 bottom-3 p-2 rounded-full ${
                  isListening
                    ? 'bg-red-500 text-white hover:bg-red-600'
                    : 'bg-gray-200 text-gray-600 hover:bg-gray-300 dark:bg-gray-600 dark:text-gray-200 dark:hover:bg-gray-500'
                } focus:outline-none transition-colors`}
                title={isListening ? 'Berhenti mendengarkan' : 'Bicara'}
              >
                {isListening ? (
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 animate-pulse" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14M12 5l7 7-7 7" />
                  </svg>
                ) : (
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
                  </svg>
                )}
              </button>
            </div>
            
            {isListening && (
              <p className="mt-2 text-sm text-gray-500 dark:text-gray-400 flex items-center">
                <span className="inline-block h-2 w-2 rounded-full bg-red-500 animate-pulse mr-2"></span>
                Mendengarkan... Bicara sekarang
              </p>
            )}
          </div>
          
          {error && (
            <div className="mb-4 p-3 bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500 dark:border-red-700 text-sm text-red-700 dark:text-red-400">
              <p>{error}</p>
            </div>
          )}
          
          <div className="flex justify-center">
            <button
              type="submit"
              disabled={isSubmitting || !symptoms.trim()}
              className={`px-5 py-3 w-full sm:w-auto rounded-lg font-medium text-white transition-all duration-200 ${
                isSubmitting || !symptoms.trim()
                  ? 'bg-gray-400 cursor-not-allowed dark:bg-gray-600'
                  : 'bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800'
              } flex items-center justify-center`}
            >
              {isSubmitting ? (
                <>
                  <svg className="animate-spin h-5 w-5 mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Menganalisis...
                </>
              ) : (
                <>
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                  Analisis Gejala
                </>
              )}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}

