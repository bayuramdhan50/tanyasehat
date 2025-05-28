/**
 * Komponen Chatbot untuk interaksi tanya jawab tentang penyakit
 * Mengirim pertanyaan ke API backend untuk mendapatkan jawaban
 */
'use client'

import { useState, useRef, useEffect, useCallback } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion'; // Perlu diinstall: npm install framer-motion

interface Message {
  role: 'user' | 'bot' | 'system';
  content: string;
  timestamp?: Date;
  isTyping?: boolean;
  id?: number;
}

interface Suggestion {
  text: string;
  category: string;
}

export default function Chatbot() {
  const [messages, setMessages] = useState<Message[]>([
    { 
      role: 'bot', 
      content: 'Halo! Saya asisten kesehatan TanyaSehat. Ada yang bisa saya bantu tentang informasi penyakit?',
      timestamp: new Date()
    },
    { 
      role: 'system', 
      content: 'Anda dapat bertanya tentang: informasi penyakit, gejala, cara mengobati, cara mencegah, atau berapa lama penyakit sembuh.',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [showSuggestions, setShowSuggestions] = useState(true);
  const [connectionStatus, setConnectionStatus] = useState<'idle' | 'connecting' | 'connected' | 'failed'>('idle');
  
  // State untuk sugesti dinamis berdasarkan konteks percakapan
  const [suggestions, setSuggestions] = useState<Suggestion[]>([
    { text: 'Apa itu demam berdarah?', category: 'definisi' },
    { text: 'Apa gejala flu?', category: 'gejala' },
    { text: 'Bagaimana cara mengobati maag?', category: 'penanganan' },
    { text: 'Cara mencegah diabetes?', category: 'pencegahan' },
    { text: 'Berapa lama tipes sembuh?', category: 'durasi' }
  ]);
  
  // State untuk menyimpan penyakit yang disebutkan dalam percakapan
  const [mentionedDiseases, setMentionedDiseases] = useState<Set<string>>(new Set());
  
  // Data penyakit umum untuk membuat saran
  const commonDiseases = [
    'Flu', 'Demam Berdarah', 'Tipes', 'Maag', 'Diabetes', 
    'Hipertensi', 'TBC', 'Asma', 'Migrain', 'Diare'
  ];
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  // Ref untuk melacak pembaruan sugesti terakhir
  const lastSuggestionUpdateRef = useRef<number | null>(null);

  // Check server connection status
  const checkServerConnection = useCallback(async () => {
    try {
      setConnectionStatus('connecting');
      const response = await axios.get('http://localhost:5000/api/health');
      if (response.data.status === 'healthy') {
        setConnectionStatus('connected');
        return true;
      } else {
        setConnectionStatus('failed');
        return false;
      }
    } catch (error) {
      console.error('Server connection check failed:', error);
      setConnectionStatus('failed');
      return false;
    }
  }, []);
  
  // Check connection on mount
  useEffect(() => {
    checkServerConnection();
  }, [checkServerConnection]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Fungsi untuk menambahkan efek typing pada pesan bot
  const addTypingEffect = async (content: string) => {
    // Tambahkan pesan dengan indikator typing
    const typingMessageId = Date.now();
    setMessages(prev => [...prev, { 
      role: 'bot', 
      content: '',
      isTyping: true,
      timestamp: new Date(),
      id: typingMessageId
    } as Message]);
    
    // Delay sebelum mulai menampilkan teks
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // Hitung karakter per detik berdasarkan panjang pesan
    const charsPerSecond = Math.max(20, Math.min(60, content.length / 10)); // Min 20, max 60
    const totalTimeMs = (content.length / charsPerSecond) * 1000;
    const incrementPerChar = totalTimeMs / content.length;
    
    let currentText = '';
    
    for (let i = 0; i < content.length; i++) {
      currentText += content[i];
      setMessages(prev => prev.map(msg => 
        (msg as Message).id === typingMessageId 
          ? { ...msg, content: currentText } 
          : msg
      ));
      // Waktu delay antara karakter bervariasi untuk kesan lebih natural
      await new Promise(resolve => setTimeout(resolve, incrementPerChar * (0.8 + Math.random() * 0.4)));
    }
    
    // Setelah selesai, hapus indikator typing
    setMessages(prev => prev.map(msg => 
      (msg as Message).id === typingMessageId 
        ? { ...msg, isTyping: false, timestamp: new Date() } 
        : msg
    ));
    
    // Ekstrak penyakit dari respons untuk memperbarui saran
    extractDiseasesFromResponse(content);
  };
  
  // Fungsi untuk mengekstrak penyakit yang disebutkan dalam respons
  const extractDiseasesFromResponse = (content: string) => {
    let diseaseDetected = false;
    
    // Ekstrak penyakit dari respons bot
    commonDiseases.forEach(disease => {
      if (content.includes(disease)) {
        // Tambahkan ke daftar penyakit yang disebutkan
        setMentionedDiseases(prev => new Set([...prev, disease]));
        diseaseDetected = true;
      }
    });
    
    // Jika tidak ada penyakit baru yang terdeteksi, tidak perlu update saran
    // Ini mencegah perubahan saran yang tidak perlu
    if (!diseaseDetected) {
      return;
    }
  };

  // Fungsi untuk mendapatkan penyakit acak yang berbeda dari yang diberikan
  const getRandomDisease = (excludeDisease?: string) => {
    let availableDiseases = [...commonDiseases];
    if (excludeDisease) {
      availableDiseases = availableDiseases.filter(d => d !== excludeDisease);
    }
    return availableDiseases[Math.floor(Math.random() * availableDiseases.length)];
  };
  
  // Fungsi untuk mendapatkan beberapa penyakit acak
  const getRandomDiseases = (count: number, preferredDiseases: string[] = []) => {
    const result: string[] = [];
    
    // Tambahkan dari preferredDiseases terlebih dahulu
    for (let i = 0; i < preferredDiseases.length && result.length < count; i++) {
      if (!result.includes(preferredDiseases[i])) {
        result.push(preferredDiseases[i]);
      }
    }
    
    // Tambahkan dari commonDiseases jika masih kurang
    let availableDiseases = commonDiseases.filter(d => !result.includes(d));
    while (result.length < count && availableDiseases.length > 0) {
      const randomIndex = Math.floor(Math.random() * availableDiseases.length);
      result.push(availableDiseases[randomIndex]);
      availableDiseases.splice(randomIndex, 1);
    }
    
    return result;
  };
  
  // Fungsi untuk menghasilkan saran baru berdasarkan konteks percakapan
  const updateSuggestions = useCallback(() => {
    // Cek apakah ada pesan bot yang baru, jika tidak ada, jangan update sugesti
    const lastBotMessage = messages.filter(m => m.role === 'bot' && !m.isTyping).pop();
    if (!lastBotMessage) return;
    
    // Cek apakah kita sudah memperbarui sugesti untuk pesan bot ini
    // Jika ya, jangan perbarui lagi untuk mencegah efek glitch
    if (lastSuggestionUpdateRef.current === lastBotMessage.id) {
      return;
    }
    
    // Catat ID pesan terakhir yang sudah digunakan untuk memperbarui sugesti
    lastSuggestionUpdateRef.current = lastBotMessage.id || Date.now();
    
    // Dapatkan daftar penyakit yang disebutkan
    let diseasesInContext = Array.from(mentionedDiseases);
    
    // Jika tidak ada penyakit yang terdeteksi, gunakan daftar umum
    if (diseasesInContext.length === 0) {
      diseasesInContext = commonDiseases.slice(0, 3);
    }
    
    const disease = diseasesInContext[0] || 'Demam Berdarah';
    const otherDisease = getRandomDisease(disease);
    
    // Buat saran berdasarkan penyakit yang terdeteksi
    const newSuggestions: Suggestion[] = [
      { text: `Apa itu ${disease}?`, category: 'definisi' },
      { text: `Apa gejala ${disease}?`, category: 'gejala' },
      { text: `Bagaimana cara mengobati ${disease}?`, category: 'penanganan' },
      { text: `Cara mencegah ${disease}?`, category: 'pencegahan' },
      { text: `Berapa lama ${disease} sembuh?`, category: 'durasi' }
    ];
    
    // Tambahkan pertanyaan tentang penyakit lain untuk variasi
    if (otherDisease !== disease) {
      newSuggestions.push({ text: `Apa itu ${otherDisease}?`, category: 'definisi' });
      newSuggestions.push({ text: `Apa gejala ${otherDisease}?`, category: 'gejala' });
    }
    
    // Gunakan ID pesan sebagai seed untuk pengacakan yang konsisten
    // Ini akan membuat saran tidak berubah-ubah secara visual
    const seed = lastBotMessage.id || Date.now();
    const shuffled = [...newSuggestions].sort((a, b) => {
      const hashA = (seed + a.text.length) % 100;
      const hashB = (seed + b.text.length) % 100;
      return hashA - hashB;
    });
    
    const selected = shuffled.slice(0, 5);
    
    // Update state suggestions hanya jika benar-benar perlu
    setSuggestions(selected);
  }, [mentionedDiseases, messages, getRandomDisease]);
  
  // Update saran ketika percakapan berubah
  useEffect(() => {
    // Hanya update saran jika ada pesan baru dari bot dan pesan tidak sedang typing
    const lastMessage = messages[messages.length - 1];
    if (lastMessage && lastMessage.role === 'bot' && !lastMessage.isTyping) {
      // Gunakan setTimeout untuk memastikan UI tidak melakukan update terlalu sering
      // yang dapat menyebabkan efek glitch
      setTimeout(() => {
        updateSuggestions();
        setShowSuggestions(true);
      }, 200);
    }
  }, [messages, updateSuggestions]);
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!input.trim()) return;
    
    const userMessage = input;
    setInput('');
    
    // Tambahkan pesan pengguna ke daftar pesan
    const newUserMessage: Message = { role: 'user', content: userMessage, timestamp: new Date() };
    setMessages(prev => [...prev, newUserMessage]);
    setIsLoading(true);
    setShowSuggestions(false);
    
    try {
      // Kirim pertanyaan ke API dengan format yang sesuai dengan backend (text bukan query)
      const response = await axios.post('http://localhost:5000/api/chat', { text: userMessage });
      
      if (response.data && response.data.response) {
        // Tambahkan jawaban dari bot dengan efek typing
        setIsLoading(false);
        await addTypingEffect(response.data.response);
      } else {
        throw new Error('Format respons tidak valid');
      }
    } catch (error: any) {
      console.error('Error sending chat message:', error);
      
      // Tampilkan pesan error yang lebih informatif
      let errorMessage = 'Maaf, saya mengalami masalah teknis. Silakan coba lagi nanti.';
      
      // Cek jika error berasal dari respons API
      if (error.response) {
        if (error.response.status === 400) {
          errorMessage = 'Maaf, format pesan tidak valid. Silakan coba lagi.';
        } else if (error.response.status === 500) {
          errorMessage = 'Terjadi masalah pada server. Tim kami sedang mengatasi masalah ini.';
        }
        
        // Jika ada pesan error spesifik dari backend
        if (error.response.data && error.response.data.error) {
          console.error('Server error:', error.response.data.error);
        }
      } else if (error.request) {
        // Request dibuat tapi tidak ada respons (kemungkinan masalah koneksi)
        errorMessage = 'Tidak dapat terhubung ke server. Pastikan server backend berjalan dan Anda terhubung ke internet.';
      }
      
      setIsLoading(false);
      await addTypingEffect(errorMessage);
      
      // Coba koneksi ulang setelah beberapa detik
      setTimeout(() => {
        checkServerConnection();
      }, 5000);
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setInput(suggestion);
    inputRef.current?.focus();
  };

  // Render server error message when connection fails
  const renderConnectionError = () => {
    if (connectionStatus === 'failed') {
      return (
        <div className="flex flex-col items-center justify-center py-8 px-4 text-center">
          <div className="bg-red-50 dark:bg-red-900/20 p-3 rounded-full mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-red-500 dark:text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
          </div>
          <h3 className="text-lg font-medium text-gray-800 dark:text-gray-200 mb-2">
            Tidak dapat terhubung ke server
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-4 max-w-sm">
            TanyaSehat tidak dapat berkomunikasi dengan server backend. Pastikan server berjalan dan coba lagi.
          </p>
          <button
            onClick={checkServerConnection}
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors flex items-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Coba lagi
          </button>
        </div>
      );
    }
    return null;
  };

  const formatTime = (date?: Date) => {
    if (!date) return '';
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="flex flex-col h-[600px] max-h-[70vh] bg-gray-50 dark:bg-gray-800/50 rounded-xl shadow-lg border border-gray-100 dark:border-gray-700 overflow-hidden"
    >
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600/90 to-blue-800/90 dark:from-blue-800/90 dark:to-blue-900/90 py-4 px-6 border-b border-blue-400/20 dark:border-blue-700/30 flex items-center justify-between shadow-md">
        <div className="flex items-center">
          <div className="h-12 w-12 rounded-full bg-white/90 dark:bg-gray-800/90 shadow-inner flex items-center justify-center mr-4 border border-blue-200/30 dark:border-blue-700/30">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
            </svg>
          </div>
          <div>
            <h3 className="font-semibold text-white text-lg">Asisten TanyaSehat</h3>
            <div className="flex items-center mt-1">
              <div className={`h-2 w-2 rounded-full mr-2 ${
                connectionStatus === 'connected' ? 'bg-green-400' : 
                connectionStatus === 'connecting' ? 'bg-yellow-300 animate-pulse' : 
                'bg-red-400'
              }`}></div>
              <p className="text-xs text-blue-100">
                {connectionStatus === 'connected' && 'Online - Siap menjawab pertanyaan tentang kesehatan'}
                {connectionStatus === 'connecting' && 'Menghubungkan ke server...'}
                {connectionStatus === 'failed' && 'Offline - Gagal terhubung ke server'}
                {connectionStatus === 'idle' && 'Memuat...'}
              </p>
            </div>
          </div>
        </div>
        
        {/* AI Assistant badge */}
        <div className="bg-blue-500/20 dark:bg-blue-900/50 py-1 px-3 rounded-full border border-blue-300/30 dark:border-blue-700/30">
          <span className="text-xs text-white flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
            </svg>
            AI Assistant
          </span>
        </div>
      </div>
      
      {/* Chat Area */}
      <div className="flex-1 p-4 overflow-y-auto bg-gray-50 dark:bg-gray-800/30">
        {connectionStatus === 'failed' && messages.length <= 2 ? (
          renderConnectionError()
        ) : (
          <>
            <div className="space-y-4">
              <AnimatePresence>
                {messages.map((message, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0 }}
                    transition={{ duration: 0.3 }}
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} ${message.role === 'system' ? 'opacity-70' : ''}`}
                  >
                    <div className={`max-w-[80%] ${
                      message.role === 'user' 
                        ? 'bg-blue-600 text-white rounded-tl-2xl rounded-tr-sm rounded-bl-2xl' 
                        : message.role === 'system'
                          ? 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-tl-sm rounded-tr-2xl rounded-br-2xl' 
                          : 'bg-white dark:bg-gray-700 text-gray-800 dark:text-gray-200 shadow-sm border border-gray-100 dark:border-gray-600 rounded-tl-sm rounded-tr-2xl rounded-br-2xl'
                    } px-4 py-3 mb-1`}
                    >
                      <p className="whitespace-pre-wrap">
                        {message.content}
                        {message.isTyping && (
                          <span className="inline-flex ml-1">
                            <span className="animate-ping-slow h-1 w-1 rounded-full bg-current mx-0.5"></span>
                            <span className="animate-ping-slow delay-100 h-1 w-1 rounded-full bg-current mx-0.5"></span>
                            <span className="animate-ping-slow delay-200 h-1 w-1 rounded-full bg-current mx-0.5"></span>
                          </span>
                        )}
                      </p>
                    </div>
                    {message.timestamp && (
                      <div className={`text-[10px] text-gray-500 dark:text-gray-400 mt-1 ${message.role === 'user' ? 'mr-1' : 'ml-1'}`}>
                        {formatTime(message.timestamp)}
                      </div>
                    )}
                  </motion.div>
                ))}
              </AnimatePresence>
            
              {isLoading && (
                <motion.div 
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="flex justify-start"
                >
                  <div className="bg-white dark:bg-gray-700 text-gray-500 dark:text-gray-300 px-4 py-3 rounded-xl shadow-sm border border-gray-100 dark:border-gray-600 max-w-[80%]">
                    <div className="flex space-x-2">
                      <div className="h-2 w-2 rounded-full bg-blue-600 animate-bounce"></div>
                      <div className="h-2 w-2 rounded-full bg-blue-600 animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                      <div className="h-2 w-2 rounded-full bg-blue-600 animate-bounce" style={{ animationDelay: '0.4s' }}></div>
                    </div>
                  </div>
                </motion.div>
              )}
              
              {!isLoading && showSuggestions && suggestions.length > 0 && (
                <motion.div 
                  key="suggestions-container"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.5, duration: 0.3 }}
                  className="mt-6 mb-2"
                >
                  <p className="text-xs text-gray-500 dark:text-gray-400 mb-2 ml-1">Pertanyaan yang mungkin ingin Anda tanyakan:</p>
                  <div className="flex flex-wrap gap-2">
                    {suggestions.map((suggestion, index) => (
                      <motion.button
                        key={`suggestion-${suggestion.text}`}
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: 0.5 + index * 0.1, duration: 0.2 }}
                        onClick={() => handleSuggestionClick(suggestion.text)}
                        className={`px-3 py-2 text-sm rounded-full border transition-colors ${
                          suggestion.category === 'gejala' 
                            ? 'bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400 border-green-200 dark:border-green-800 hover:bg-green-100 dark:hover:bg-green-800/30'
                            : suggestion.category === 'penanganan'
                              ? 'bg-blue-50 dark:bg-blue-900/20 text-blue-600 dark:text-blue-400 border-blue-200 dark:border-blue-800 hover:bg-blue-100 dark:hover:bg-blue-800/30'
                              : suggestion.category === 'pencegahan'
                                ? 'bg-purple-50 dark:bg-purple-900/20 text-purple-600 dark:text-purple-400 border-purple-200 dark:border-purple-800 hover:bg-purple-100 dark:hover:bg-purple-800/30'
                                : suggestion.category === 'durasi'
                                  ? 'bg-orange-50 dark:bg-orange-900/20 text-orange-600 dark:text-orange-400 border-orange-200 dark:border-orange-800 hover:bg-orange-100 dark:hover:bg-orange-800/30'
                                  : 'bg-white dark:bg-gray-700 text-gray-600 dark:text-gray-300 border-gray-200 dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-600'
                        }`}
                      >
                        {suggestion.text}
                      </motion.button>
                    ))}
                  </div>
                </motion.div>
              )}
              {renderConnectionError()}
            </div>
            <div ref={messagesEndRef} />
          </>
        )}
      </div>
      
      {/* Input Area */}
      <form onSubmit={handleSubmit} className="bg-white dark:bg-gray-800 p-4 border-t border-gray-100 dark:border-gray-700">
        <div className="flex space-x-2">
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={connectionStatus === 'failed' ? "Server sedang offline..." : "Ketik pertanyaan tentang kesehatan..."}
            className={`flex-1 px-4 py-2 border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 ${
              connectionStatus === 'failed'
                ? 'bg-gray-100 dark:bg-gray-800 text-gray-400 dark:text-gray-500 border-gray-300 dark:border-gray-600'
                : 'bg-gray-50 dark:bg-gray-700 text-gray-800 dark:text-white border-gray-200 dark:border-gray-700'
            }`}
            disabled={isLoading || connectionStatus === 'failed'}
          />
          <button
            type="submit"
            disabled={!input.trim() || isLoading || connectionStatus === 'failed' || connectionStatus === 'connecting'}
            className={`px-4 py-2 rounded-full flex items-center justify-center ${
              !input.trim() || isLoading || connectionStatus === 'failed' || connectionStatus === 'connecting'
                ? 'bg-gray-300 dark:bg-gray-600 text-gray-500 dark:text-gray-400 cursor-not-allowed'
                : 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-2 focus:ring-blue-300 dark:focus:ring-blue-800'
            } transition-colors`}
          >
            {isLoading ? (
              <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            ) : connectionStatus === 'failed' ? (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.141 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0" />
              </svg>
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
              </svg>
            )}
          </button>
        </div>
        
        {connectionStatus === 'failed' ? (
          <div className="flex justify-center mt-3">
            <button 
              onClick={(e) => {
                e.preventDefault();
                checkServerConnection();
              }}
              className="text-xs text-blue-500 hover:text-blue-600 dark:text-blue-400 dark:hover:text-blue-300 flex items-center"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Coba hubungkan kembali
            </button>
          </div>
        ) : (
          <p className="text-xs text-center text-gray-500 dark:text-gray-400 mt-2">
            Asisten TanyaSehat memberikan informasi umum, bukan pengganti konsultasi medis profesional.
          </p>
        )}
      </form>
    </motion.div>
  );
}
