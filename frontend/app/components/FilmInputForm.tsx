/**
 * Komponen InputForm untuk menerima input preferensi film dari pengguna
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
  const [preferences, setPreferences] = useState('');
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [retryCount, setRetryCount] = useState(0);
  const [maxRetries] = useState(3);
  const [apiUrl, setApiUrl] = useState('http://localhost:5000/api/analyze');
  const [connectionStatus, setConnectionStatus] = useState<'idle' | 'connecting' | 'connected' | 'failed'>('idle');
  const formRef = useRef<HTMLFormElement>(null);
  const [examples, setExamples] = useState<string[]>([
    'Saya suka film action dengan efek visual yang keren',
    'Film drama yang mengharukan dan memiliki pesan moral',
    'Rekomendasi film horor yang benar-benar menegangkan',
    'Saya ingin menonton film sci-fi dengan plot twist menarik',
    'Film komedi romantis yang ringan dan menghibur'
  ]);

  // Menggunakan speech recognition hook
  const {
    isListening,
    startListening,
    stopListening,
    hasRecognitionSupport
  } = useSpeechRecognition({ onResult: (text) => setPreferences(prev => prev + ' ' + text) });

  // Cek status koneksi ke backend API
  const checkConnection = useCallback(debounce(async () => {
    try {
      setConnectionStatus('connecting');
      const response = await axios.get(apiUrl.replace('/analyze', '/health'), 
      { timeout: 3000 });
      if (response.status === 200) {
        setConnectionStatus('connected');
      } else {
        setConnectionStatus('failed');
        setApiUrl('https://filmfinder-api-fallback.herokuapp.com/api/analyze'); // Ganti dengan URL fallback jika ada
      }
    } catch (error) {
      console.error('Connection check failed:', error);
      setConnectionStatus('failed');
      // Fallback ke API publik jika local tidak tersedia
      setApiUrl('https://filmfinder-api-fallback.herokuapp.com/api/analyze'); // Ganti dengan URL fallback jika ada
    }
  }, 500), [apiUrl]);

  // Cek koneksi API pada load pertama
  useEffect(() => {
    checkConnection();
  }, [checkConnection]);

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!preferences.trim()) {
      setError('Silakan masukkan preferensi film Anda');
      return;
    }

    if (isSubmitting) return;

    try {
      setError('');
      setIsSubmitting(true);
      onLoading(true);
      
      // Kirim data ke backend
      const response = await axios.post(apiUrl, { text: preferences }, {
        headers: { 'Content-Type': 'application/json' },
        timeout: 10000 // 10 detik timeout
      });
      
      if (response.data) {
        onResult(response.data);
        setRetryCount(0);
      } else {
        throw new Error('Tidak ada data yang diterima dari server');
      }
    } catch (err: any) {
      console.error('Error submitting form:', err);
      
      // Coba hingga maxRetries
      if (retryCount < maxRetries) {
        setRetryCount(prevCount => prevCount + 1);
        setTimeout(() => handleSubmit(e), 1000); // Coba lagi setelah 1 detik
      } else {
        setError(err.response?.data?.message || 
                err.message || 
                'Terjadi kesalahan saat memproses permintaan Anda');
        onResult(null);
      }
    } finally {
      setIsSubmitting(false);
      onLoading(false);
    }
  };

  // Reset form
  const handleReset = () => {
    setPreferences('');
    setError('');
    onResult(null);
    if (formRef.current) {
      formRef.current.reset();
    }
  };

  // Handle input change
  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setPreferences(e.target.value);
    setError('');
  };

  // Isi contoh ke form
  const fillExample = (example: string) => {
    setPreferences(example);
    setError('');
  };

  return (
    <div className="w-full max-w-2xl mx-auto bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden p-6">
      <form ref={formRef} onSubmit={handleSubmit} className="space-y-4">
        <div className="space-y-2">
          <label htmlFor="preferences" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
            Preferensi Film
          </label>
          
          <div className="relative">
            <textarea
              id="preferences"
              name="preferences"
              rows={4}
              value={preferences}
              onChange={handleInputChange}
              placeholder="Jelaskan apa jenis film yang Anda sukai, atau film seperti apa yang ingin Anda tonton..."
              className="block w-full px-4 py-3 text-gray-700 dark:text-gray-300 bg-gray-50 dark:bg-gray-700 border rounded-md focus:border-blue-500 focus:ring-blue-500 focus:outline-none"
              aria-describedby="preferences-description"
            />
            
            {hasRecognitionSupport && (
              <button 
                type="button"
                onClick={isListening ? stopListening : startListening}
                className={`absolute bottom-3 right-3 p-2 rounded-full ${
                  isListening 
                    ? 'bg-red-500 text-white' 
                    : 'bg-gray-200 dark:bg-gray-600 text-gray-700 dark:text-gray-300'
                }`}
                aria-label={isListening ? 'Berhenti mendengarkan' : 'Mulai mendengarkan'}
                title={isListening ? 'Berhenti mendengarkan' : 'Gunakan suara'}
              >
                {isListening ? (
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8 7a1 1 0 00-1 1v4a1 1 0 001 1h4a1 1 0 001-1V8a1 1 0 00-1-1H8z" clipRule="evenodd" />
                  </svg>
                ) : (
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z" clipRule="evenodd" />
                  </svg>
                )}
              </button>
            )}
          </div>
          
          <p id="preferences-description" className="text-xs text-gray-500 dark:text-gray-400">
            Ceritakan tentang genre, tema, atau gaya film yang Anda sukai. Semakin detail semakin baik rekomendasinya.
            {isListening && <span className="text-red-500 ml-2 animate-pulse">Mendengarkan...</span>}
          </p>
        </div>

        {/* Contoh input */}
        <div className="space-y-2">
          <p className="text-sm text-gray-600 dark:text-gray-400">Contoh:</p>
          <div className="flex flex-wrap gap-2">
            {examples.map((example, index) => (
              <button
                key={index}
                type="button"
                onClick={() => fillExample(example)}
                className="text-xs px-3 py-1 bg-blue-50 dark:bg-gray-700 text-blue-600 dark:text-blue-300 rounded-full hover:bg-blue-100 dark:hover:bg-gray-600 transition-colors"
              >
                {example.length > 40 ? example.substring(0, 40) + '...' : example}
              </button>
            ))}
          </div>
        </div>

        {error && (
          <div className="text-sm text-red-600 dark:text-red-400 bg-red-50 dark:bg-red-900/20 p-3 rounded-md">
            {error}
          </div>
        )}

        <div className="flex space-x-4">
          <button
            type="submit"
            disabled={isSubmitting}
            className={`flex-1 px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 ${
              isSubmitting ? 'opacity-70 cursor-not-allowed' : ''
            }`}
          >
            {isSubmitting ? (
              <>
                <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Mencari...
              </>
            ) : (
              'Cari Rekomendasi Film'
            )}
          </button>
          <button
            type="button"
            onClick={handleReset}
            className="px-4 py-2 text-gray-700 dark:text-gray-300 bg-gray-200 dark:bg-gray-700 rounded-md hover:bg-gray-300 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
          >
            Reset
          </button>
        </div>

        {/* Status koneksi API */}
        <div className="flex items-center justify-end">
          <div className="flex items-center">
            <span className="text-xs text-gray-500 dark:text-gray-400 mr-2">API:</span>
            {connectionStatus === 'connecting' && (
              <span className="flex items-center text-xs text-yellow-500">
                <span className="h-2 w-2 bg-yellow-500 rounded-full mr-1 animate-pulse"></span>
                Menyambung...
              </span>
            )}
            {connectionStatus === 'connected' && (
              <span className="flex items-center text-xs text-green-500">
                <span className="h-2 w-2 bg-green-500 rounded-full mr-1"></span>
                Terhubung
              </span>
            )}
            {connectionStatus === 'failed' && (
              <span className="flex items-center text-xs text-red-500">
                <span className="h-2 w-2 bg-red-500 rounded-full mr-1"></span>
                Gagal terhubung
              </span>
            )}
          </div>
        </div>
      </form>
    </div>
  );
}
