/**
 * Komponen Chatbot untuk interaksi tanya jawab tentang penyakit
 * Mengirim pertanyaan ke API backend untuk mendapatkan jawaban
 */
'use client'

import { useState, useRef, useEffect } from 'react';
import axios from 'axios';

interface Message {
  role: 'user' | 'bot';
  content: string;
}

export default function Chatbot() {
  const [messages, setMessages] = useState<Message[]>([
    { role: 'bot', content: 'Halo! Saya asisten kesehatan TanyaSehat. Ada yang bisa saya bantu tentang informasi penyakit?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
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
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [
        ...prev, 
        { 
          role: 'bot', 
          content: 'Maaf, terjadi kesalahan dalam memproses permintaan Anda.' 
        }
      ]);
    } finally {
      setIsLoading(false);
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
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div 
              className={`max-w-[80%] p-3 rounded-lg ${
                message.role === 'user' 
                  ? 'bg-blue-600 text-white rounded-tr-none' 
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-white rounded-tl-none'
              }`}
            >
              {message.content}
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="max-w-[80%] p-3 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-white rounded-tl-none">
              <span className="inline-block w-5 h-5 animate-pulse">...</span>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
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
