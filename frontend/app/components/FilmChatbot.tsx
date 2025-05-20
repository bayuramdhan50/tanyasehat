/**
 * Komponen FilmChatbot untuk interaksi percakapan tentang film
 */
'use client'

import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';

interface Message {
  type: 'user' | 'bot';
  content: string;
  timestamp: Date;
  filmInfo?: any;
  recommendations?: any[];
  films?: any[];
}

export default function FilmChatbot() {
  const [messages, setMessages] = useState<Message[]>([
    {
      type: 'bot',
      content: 'Halo! Saya adalah asisten film yang dapat membantu Anda menemukan informasi tentang film. Apa yang ingin Anda ketahui tentang film?',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [apiUrl, setApiUrl] = useState('http://localhost:5000/api/chat');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll ke pesan terbaru
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!input.trim()) return;
    
    // Tambahkan pesan user ke state
    const userMessage: Message = {
      type: 'user',
      content: input,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    
    try {
      // Kirim pesan ke API chatbot
      const response = await axios.post(apiUrl, {
        message: input
      }, {
        headers: { 'Content-Type': 'application/json' },
        timeout: 10000 // 10 detik timeout
      });
      
      // Proses respons dari API
      if (response.data) {
        const botMessage: Message = {
          type: 'bot',
          content: response.data.content,
          timestamp: new Date()
        };
        
        // Tambahkan informasi film jika ada
        if (response.data.type === 'film_info' && response.data.film) {
          botMessage.filmInfo = response.data.film;
        }
        
        // Tambahkan rekomendasi film jika ada
        if (response.data.type === 'recommendations' && response.data.recommendations) {
          botMessage.recommendations = response.data.recommendations;
        }
        
        // Tambahkan daftar film berdasarkan genre jika ada
        if (response.data.type === 'genre_films' && response.data.films) {
          botMessage.films = response.data.films;
        }
        
        setMessages(prev => [...prev, botMessage]);
      }
    } catch (err: any) {
      console.error('Error sending message to chatbot:', err);
      
      // Tambahkan pesan error
      const errorMessage: Message = {
        type: 'bot',
        content: 'Maaf, terjadi kesalahan saat memproses pesan Anda. Silakan coba lagi nanti.',
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Format waktu pesan
  const formatTime = (date: Date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  // Render informasi film dalam format card
  const renderFilmInfo = (filmInfo: any) => {
    if (!filmInfo) return null;
    
    return (
      <div className="mt-2 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg border border-gray-200 dark:border-gray-600">
        <h4 className="font-bold text-gray-800 dark:text-gray-200">{filmInfo.title} ({filmInfo.release_year})</h4>
        <p className="mt-1 text-sm text-gray-600 dark:text-gray-300">{filmInfo.description}</p>
        
        <div className="mt-2 grid grid-cols-2 gap-2 text-sm">
          <div>
            <span className="text-gray-500 dark:text-gray-400">Sutradara:</span> {filmInfo.director}
          </div>
          <div>
            <span className="text-gray-500 dark:text-gray-400">Genre:</span> {filmInfo.genre}
          </div>
          <div>
            <span className="text-gray-500 dark:text-gray-400">Rating:</span> 
            <span className="ml-1 flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-yellow-500" viewBox="0 0 20 20" fill="currentColor">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
              {filmInfo.rating}/10
            </span>
          </div>
          <div>
            <span className="text-gray-500 dark:text-gray-400">Tahun:</span> {filmInfo.release_year}
          </div>
        </div>
        
        {filmInfo.actors && (
          <div className="mt-2 text-sm">
            <span className="text-gray-500 dark:text-gray-400">Pemeran:</span> {filmInfo.actors}
          </div>
        )}
      </div>
    );
  };

  // Render daftar rekomendasi film
  const renderRecommendations = (recommendations: any[]) => {
    if (!recommendations || recommendations.length === 0) return null;
    
    return (
      <div className="mt-2 space-y-2">
        {recommendations.slice(0, 3).map((film, index) => (
          <div 
            key={index} 
            className="p-2 bg-gray-50 dark:bg-gray-700 rounded-md border border-gray-200 dark:border-gray-600"
          >
            <div className="flex justify-between">
              <h5 className="font-medium text-gray-800 dark:text-gray-200">
                {film.title}
              </h5>
              {film.release_year && (
                <span className="text-sm text-gray-500">{film.release_year}</span>
              )}
            </div>
            {film.description && (
              <p className="mt-1 text-sm text-gray-600 dark:text-gray-300 line-clamp-2">
                {film.description}
              </p>
            )}
          </div>
        ))}
        
        {recommendations.length > 3 && (
          <p className="text-xs text-gray-500 dark:text-gray-400">
            +{recommendations.length - 3} film lainnya
          </p>
        )}
      </div>
    );
  };

  // Render daftar film berdasarkan genre
  const renderGenreFilms = (films: any[]) => {
    if (!films || films.length === 0) return null;
    
    return (
      <div className="mt-2 space-y-2">
        {films.slice(0, 3).map((film, index) => (
          <div 
            key={index} 
            className="p-2 bg-gray-50 dark:bg-gray-700 rounded-md border border-gray-200 dark:border-gray-600 flex justify-between"
          >
            <div>
              <h5 className="font-medium text-gray-800 dark:text-gray-200">
                {film.title}
              </h5>
              {film.description && (
                <p className="mt-0.5 text-xs text-gray-600 dark:text-gray-300 line-clamp-1">
                  {film.description}
                </p>
              )}
            </div>
            <div className="flex flex-col items-end">
              {film.release_year && (
                <span className="text-xs text-gray-500">{film.release_year}</span>
              )}
              {film.rating && (
                <span className="text-xs flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 text-yellow-500" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                  <span className="ml-0.5">{film.rating}</span>
                </span>
              )}
            </div>
          </div>
        ))}
        
        {films.length > 3 && (
          <p className="text-xs text-gray-500 dark:text-gray-400">
            +{films.length - 3} film lainnya
          </p>
        )}
      </div>
    );
  };

  return (
    <div className="w-full max-w-2xl mx-auto bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden flex flex-col h-[500px]">
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
        <h2 className="text-lg font-semibold text-gray-800 dark:text-white">Film Assistant</h2>
        <p className="text-sm text-gray-500 dark:text-gray-400">
          Tanya tentang film, genre, atau rekomendasi tontonan
        </p>
      </div>
      
      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        <AnimatePresence>
          {messages.map((message, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`max-w-[80%] ${
                message.type === 'user' 
                  ? 'bg-blue-600 text-white rounded-t-2xl rounded-bl-2xl'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-t-2xl rounded-br-2xl'
              } px-4 py-3`}>
                {/* Message Content */}
                <div className="text-sm whitespace-pre-wrap">
                  {message.content}
                </div>
                
                {/* Film Info Card */}
                {message.filmInfo && renderFilmInfo(message.filmInfo)}
                
                {/* Recommendations */}
                {message.recommendations && renderRecommendations(message.recommendations)}
                
                {/* Genre Films */}
                {message.films && renderGenreFilms(message.films)}
                
                {/* Timestamp */}
                <div className={`text-xs mt-1 ${
                  message.type === 'user' 
                    ? 'text-blue-200'
                    : 'text-gray-500 dark:text-gray-400'
                }`}>
                  {formatTime(message.timestamp)}
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
        
        {/* Loading indicator */}
        {isLoading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex justify-start"
          >
            <div className="bg-gray-100 dark:bg-gray-700 rounded-2xl px-4 py-3">
              <div className="flex space-x-2">
                <div className="w-2 h-2 rounded-full bg-gray-400 dark:bg-gray-500 animate-bounce" style={{ animationDelay: '0ms' }}></div>
                <div className="w-2 h-2 rounded-full bg-gray-400 dark:bg-gray-500 animate-bounce" style={{ animationDelay: '200ms' }}></div>
                <div className="w-2 h-2 rounded-full bg-gray-400 dark:bg-gray-500 animate-bounce" style={{ animationDelay: '400ms' }}></div>
              </div>
            </div>
          </motion.div>
        )}
        
        {/* Auto-scroll anchor */}
        <div ref={messagesEndRef} />
      </div>
      
      {/* Input Form */}
      <form onSubmit={handleSubmit} className="border-t border-gray-200 dark:border-gray-700 p-4">
        <div className="relative">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Tanyakan tentang film..."
            className="w-full px-4 py-2 pr-12 border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className={`absolute right-2 top-1/2 -translate-y-1/2 p-1.5 rounded-full ${
              isLoading || !input.trim()
                ? 'bg-gray-200 dark:bg-gray-600 text-gray-400 dark:text-gray-500 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700'
            }`}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </div>
        
        <div className="mt-2 text-xs text-gray-500 dark:text-gray-400 flex justify-between">
          <span>Tanyakan tentang judul, genre, atau rekomendasi film</span>
          <span>Contoh: "Film apa yang mirip dengan Inception?"</span>
        </div>
      </form>
    </div>
  );
}
