/**
 * Komponen InputForm untuk menerima input gejala dari pengguna
 * Mengirim input ke API backend untuk diproses
 */
'use client'

import { useState } from 'react';
import axios from 'axios';

interface InputFormProps {
  onResult: (data: any) => void;
  onLoading: (loading: boolean) => void;
}

export default function InputForm({ onResult, onLoading }: InputFormProps) {
  const [symptoms, setSymptoms] = useState('');
  const [error, setError] = useState('');

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
        <textarea
          id="symptoms"
          className="w-full p-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none min-h-[120px] bg-white dark:bg-gray-800 text-gray-800 dark:text-white"
          placeholder="Contoh: Saya mengalami sakit kepala, demam, dan batuk kering sejak 3 hari yang lalu..."
          value={symptoms}
          onChange={(e) => setSymptoms(e.target.value)}
          rows={5}
        />
        {error && <p className="mt-2 text-red-500 text-sm">{error}</p>}
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
