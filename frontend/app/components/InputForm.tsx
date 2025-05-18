/**
 * Komponen InputForm untuk menerima input gejala dari pengguna
 * Mengirim input ke API backend untuk diproses
 */
'use client'

import { useState } from 'react';
import axios from 'axios';
import useSpeechRecognition from '../hooks/useSpeechRecognition';

interface InputFormProps {
  onResult: (data: any) => void;
  onLoading: (loading: boolean) => void;
}

export default function InputForm({ onResult, onLoading }: InputFormProps) {
  const [symptoms, setSymptoms] = useState('');
  const [error, setError] = useState('');
  const [examples, setExamples] = useState<string[]>([
    'Saya mengalami demam tinggi dan sakit kepala selama 3 hari',
    'Saya batuk kering, sesak napas, dan nyeri dada sejak seminggu yang lalu',
    'Perut saya sakit dan saya sering muntah sejak kemarin',
    'Saya mengalami pusing, mual, dan pandangan kabur',
    'Tenggorokan saya sakit dan sulit menelan sejak 2 hari yang lalu'
  ]);
  
  // Gunakan custom hook untuk speech recognition
  const { 
    isListening, 
    startListening, 
    stopListening, 
    hasSupport 
  } = useSpeechRecognition({
    onResult: (text) => {
      setSymptoms(text);
    },
    onError: (error) => {
      console.error('Speech recognition error:', error);
      setError('Terjadi kesalahan pada pengenalan suara. Silakan coba lagi.');
    },
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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!symptoms.trim()) {
      setError('Silakan masukkan gejala yang Anda alami');
      return;
    }
    
    setError('');
    onLoading(true);
    
    try {
      const response = await axios.post('http://localhost:5000/api/predict', {
        text: symptoms
      });
      
      // Log data untuk debugging
      console.log('API Response:', response.data);
      
      onResult(response.data);
    } catch (error) {
      console.error('Error:', error);
      setError('Terjadi kesalahan saat menghubungi server');
    } finally {
      onLoading(false);
    }
  };
  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl mx-auto">
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
          />
          <button
            type="button"
            onClick={toggleListening}
            className={`absolute bottom-3 right-3 p-2 rounded-full ${isListening ? 'bg-red-500 animate-pulse' : 'bg-blue-500'}`}
            title={isListening ? 'Klik untuk berhenti merekam' : 'Klik untuk mulai merekam suara'}
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
        {error && <p className="mt-2 text-red-500 text-sm">{error}</p>}
        
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
              >
                {example.length > 30 ? example.substring(0, 30) + '...' : example}
              </button>
            ))}
          </div>
        </div>
      </div>
      <button
        type="submit"
        className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200"
      >
        Analisis Gejala
      </button>
    </form>
  );
}
