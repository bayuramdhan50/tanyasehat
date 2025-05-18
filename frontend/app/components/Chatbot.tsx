/**
 * Komponen Chatbot untuk interaksi tanya jawab tentang penyakit
 * Mengirim pertanyaan ke API backend untuk mendapatkan jawaban
 */
'use client'

import { useState, useRef, useEffect } from 'react';
import axios from 'axios';

interface Message {
  role: 'user' | 'bot' | 'system';
  content: string;
}

export default function Chatbot() {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'bot', content: 'Halo! Saya asisten kesehatan TanyaSehat. Ada yang bisa saya bantu tentang informasi penyakit?' },
    { role: 'system', content: 'Anda dapat bertanya tentang: informasi penyakit, gejala, cara mengobati, cara mencegah, atau berapa lama penyakit sembuh.' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [suggestions, setSuggestions] = useState<string[]>([
    'Apa itu demam berdarah?',
    'Apa gejala flu?',
    'Bagaimana cara mengobati maag?',
    'Cara mencegah diabetes?',
    'Berapa lama tipes sembuh?'
  ]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!input.trim()) return;
    
    const userMessage = input;
    setInput('');
    
    // Tambahkan pesan pengguna ke daftar pesan
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);
    
    try {
      const response = await axios.post('http://localhost:5000/api/chat', {
        text: userMessage
      });
      
      // Tambahkan respon dari bot ke daftar pesan
      setMessages(prev => [...prev, { role: 'bot', content: response.data.response }]);
      
      // Hasilkan saran baru berdasarkan konteks percakapan
      generateNewSuggestions(userMessage, response.data.response);
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [
        ...prev, 
        { 
          role: 'bot', 
          content: 'Maaf, terjadi kesalahan dalam memproses permintaan Anda. Mohon periksa koneksi ke server dan coba lagi.' 
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setInput(suggestion);
  };

  // Fungsi untuk menghasilkan saran baru berdasarkan konteks percakapan
  const generateNewSuggestions = (userMessage: string, botResponse: string) => {
    // Identifikasi penyakit yang disebutkan dalam percakapan terakhir
    const diseases = [
      'Flu', 'Demam Berdarah', 'Tipes', 'TBC', 'Maag', 
      'Asma', 'Migrain', 'Diare', 'Hipertensi', 'Diabetes',
      'Alergi Makanan', 'Sinusitis'
    ];
    
    let detectedDisease = '';
    
    for (const disease of diseases) {
      if (userMessage.toLowerCase().includes(disease.toLowerCase()) || 
          botResponse.toLowerCase().includes(disease.toLowerCase())) {
        detectedDisease = disease;
        break;
      }
    }
    
    // Buat saran baru berdasarkan penyakit yang terdeteksi
    if (detectedDisease) {
      setSuggestions([
        `Apa gejala ${detectedDisease}?`,
        `Bagaimana cara mengobati ${detectedDisease}?`,
        `Cara mencegah ${detectedDisease}?`,
        `Berapa lama ${detectedDisease} sembuh?`,
        `Apa penyebab ${detectedDisease}?`
      ]);
    } else {
      // Jika tidak ada penyakit yang terdeteksi, berikan saran umum
      setSuggestions([
        'Apa itu demam berdarah?',
        'Apa gejala flu?',
        'Bagaimana cara mengobati maag?',
        'Cara mencegah diabetes?',
        'Berapa lama tipes sembuh?'
      ]);
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md w-full max-w-2xl mx-auto mt-8 overflow-hidden flex flex-col h-[500px]">
      <div className="p-4 bg-blue-600 text-white">
        <h2 className="font-bold">TanyaSehat Assistant</h2>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message, index) => (
          <div 
            key={index} 
            className={`flex ${
              message.role === 'user' 
                ? 'justify-end' 
                : message.role === 'system' 
                  ? 'justify-center' 
                  : 'justify-start'
            }`}
          >
            <div 
              className={`${
                message.role === 'user' 
                  ? 'max-w-[80%] p-3 rounded-lg bg-blue-600 text-white rounded-tr-none' 
                  : message.role === 'system'
                    ? 'max-w-[90%] p-2 text-sm bg-gray-200 dark:bg-gray-600 text-gray-600 dark:text-gray-300 rounded-lg italic'
                    : 'max-w-[80%] p-3 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-white rounded-tl-none'
              }`}
            >
              {message.content.split('\n').map((line, i) => (
                <span key={i}>
                  {line}
                  {i < message.content.split('\n').length - 1 && <br />}
                </span>
              ))}
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="max-w-[80%] p-3 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-white rounded-tl-none">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                <div className="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                <div className="w-2 h-2 bg-gray-400 dark:bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      {/* Suggestion chips */}
      <div className="px-4 py-2 flex flex-wrap gap-2">
        {suggestions.map((suggestion, index) => (
          <button
            key={index}
            onClick={() => handleSuggestionClick(suggestion)}
            className="text-xs bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 rounded-full px-3 py-1 transition-colors duration-200"
          >
            {suggestion}
          </button>
        ))}
      </div>
      
      <form onSubmit={handleSubmit} className="p-4 border-t border-gray-200 dark:border-gray-700 flex">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Tulis pesan Anda..."
          className="flex-1 p-2 border rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-800 text-gray-800 dark:text-white"
          disabled={isLoading}
        />
        <button
          type="submit"
          className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-r-lg transition-colors duration-200 disabled:bg-blue-400"
          disabled={isLoading}
        >
          Kirim
        </button>
      </form>
    </div>
  );
}
