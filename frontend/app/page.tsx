'use client'

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import Header from './components/Header';
import InputForm from './components/InputForm';
import ResultCard from './components/ResultCard';
import Chatbot from './components/Chatbot';
import Loading from './components/Loading';
import Tabs from './components/Tabs';
import ThemeToggle from './components/ThemeToggle';

export default function Home() {
  const [result, setResult] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [showInfo, setShowInfo] = useState(true);
  const [activeTabIndex, setActiveTabIndex] = useState(0);

  const handleResult = (data: any) => {
    setResult(data);
    setShowInfo(false); // Sembunyikan info setelah hasil diterima
    // Scroll to result area
    setTimeout(() => {
      window.scrollTo({ top: 400, behavior: 'smooth' });
    }, 100);
  };

  const handleLoading = (loading: boolean) => {
    setIsLoading(loading);
  };
  
  const handleTabChange = (index: number) => {
    setActiveTabIndex(index);
  };

  const InfoCard = () => (
    <div className="bg-white/90 dark:bg-gray-800/90 backdrop-blur-sm rounded-xl shadow-lg p-8 w-full max-w-2xl mx-auto mt-8 border border-gray-100 dark:border-gray-700">
      <div className="flex items-center mb-6">
        <div className="bg-blue-100 dark:bg-blue-900/50 p-3 rounded-lg mr-4">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h2 className="text-2xl font-bold text-gray-800 dark:text-gray-100">Selamat Datang di TanyaSehat</h2>
      </div>
      
      <div className="prose dark:prose-invert prose-sm max-w-none">
        <p className="text-gray-700 dark:text-gray-300 text-base leading-relaxed">
          TanyaSehat adalah sistem deteksi penyakit berbasis Natural Language Processing (NLP) 
          yang dapat membantu Anda mengidentifikasi kemungkinan penyakit berdasarkan gejala yang Anda alami.
        </p>
        
        <h3 className="text-xl font-medium mt-6 mb-4 text-gray-800 dark:text-gray-200">Cara Menggunakan:</h3>
        <div className="space-y-4">
          <div className="flex items-start">
            <div className="bg-blue-50 dark:bg-blue-900/30 rounded-full p-1 text-blue-600 dark:text-blue-400 mr-3">
              <span className="inline-flex items-center justify-center h-6 w-6 font-bold">1</span>
            </div>
            <div>
              <p className="font-medium text-gray-800 dark:text-gray-200">Deskripsikan gejala Anda</p>
              <p className="text-gray-600 dark:text-gray-400 text-sm">
                Gunakan bahasa alami dalam kolom input. 
                Contoh: "Saya mengalami demam tinggi, sakit kepala, dan nyeri otot sejak 2 hari yang lalu."
              </p>
            </div>
          </div>
          <div className="flex items-start">
            <div className="bg-blue-50 dark:bg-blue-900/30 rounded-full p-1 text-blue-600 dark:text-blue-400 mr-3">
              <span className="inline-flex items-center justify-center h-6 w-6 font-bold">2</span>
            </div>
            <div>
              <p className="font-medium text-gray-800 dark:text-gray-200">Gunakan fitur input suara</p>
              <p className="text-gray-600 dark:text-gray-400 text-sm">
                Klik ikon mikrofon jika Anda lebih nyaman berbicara daripada mengetik.
              </p>
            </div>
          </div>
          <div className="flex items-start">
            <div className="bg-blue-50 dark:bg-blue-900/30 rounded-full p-1 text-blue-600 dark:text-blue-400 mr-3">
              <span className="inline-flex items-center justify-center h-6 w-6 font-bold">3</span>
            </div>
            <div>
              <p className="font-medium text-gray-800 dark:text-gray-200">Analisis Gejala</p>
              <p className="text-gray-600 dark:text-gray-400 text-sm">
                Klik tombol "Analisis Gejala" untuk mendapatkan hasil deteksi beserta rekomendasi.
              </p>
            </div>
          </div>
          <div className="flex items-start">
            <div className="bg-blue-50 dark:bg-blue-900/30 rounded-full p-1 text-blue-600 dark:text-blue-400 mr-3">
              <span className="inline-flex items-center justify-center h-6 w-6 font-bold">4</span>
            </div>
            <div>
              <p className="font-medium text-gray-800 dark:text-gray-200">Konsultasi dengan Asisten</p>
              <p className="text-gray-600 dark:text-gray-400 text-sm">
                Gunakan tab Asisten TanyaSehat untuk informasi lebih lanjut tentang penyakit atau perawatan kesehatan.
              </p>
            </div>
          </div>
        </div>
        
        <div className="mt-8 p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border-l-4 border-yellow-400 dark:border-yellow-600">
          <div className="flex">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-yellow-600 dark:text-yellow-500 mr-2 flex-shrink-0" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <p className="text-sm text-yellow-800 dark:text-yellow-200">
              <strong>Penting:</strong> Sistem ini dirancang sebagai alat bantu informatif dan bukan pengganti diagnosis medis profesional.
              Selalu konsultasikan dengan dokter untuk diagnosis dan perawatan yang tepat.
            </p>
          </div>
        </div>
      </div>
      
      <button 
        onClick={() => setShowInfo(false)} 
        className="mt-6 text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 text-sm font-medium flex items-center group focus:outline-none"
      >
        <span>Sembunyikan informasi ini</span>
        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 ml-1 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
        </svg>
      </button>
    </div>
  );

  const tabs = [
    {
      id: 'detection',
      label: 'Deteksi Penyakit',
      content: (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          <InputForm onResult={handleResult} onLoading={handleLoading} />
          {isLoading ? <Loading /> : result ? <ResultCard result={result} /> : showInfo && <InfoCard />}
        </motion.div>
      ),
    },
    {
      id: 'chatbot',
      label: 'Asisten TanyaSehat',
      content: (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.3 }}
        >
          <Chatbot />
        </motion.div>
      ),
    },
  ];

  useEffect(() => {
    // Initialize theme from localStorage
    if (typeof window !== 'undefined') {
      const storedTheme = localStorage.getItem('theme')
      if (storedTheme === 'dark' || 
        (!storedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
    }
  }, [])

  return (
    <div className="min-h-screen text-gray-900 dark:text-gray-50 py-10 px-4 sm:px-6 relative overflow-hidden">
      {/* Background decorations */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none -z-10">
        <div className="absolute top-20 left-20 w-64 h-64 rounded-full bg-blue-300/20 dark:bg-blue-900/20 blur-3xl"></div>
        <div className="absolute top-40 right-20 w-72 h-72 rounded-full bg-indigo-300/20 dark:bg-indigo-900/20 blur-3xl"></div>
        <div className="absolute bottom-20 left-1/3 w-80 h-80 rounded-full bg-blue-200/20 dark:bg-blue-800/20 blur-3xl"></div>
      </div>
      
      <motion.div 
        className="max-w-4xl mx-auto"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <Header />
        <motion.div 
          className="backdrop-blur-sm bg-white/80 dark:bg-gray-800/80 rounded-xl shadow-xl p-6 mb-10 border border-gray-100 dark:border-gray-700"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3, duration: 0.6 }}
        >
          <Tabs 
            tabs={tabs} 
            initialTabIndex={activeTabIndex}
            onTabChange={handleTabChange}
          />
        </motion.div>
      </motion.div>
      
      <footer className="mt-20 text-center text-sm text-gray-500 dark:text-gray-400 max-w-3xl mx-auto border-t border-gray-200 dark:border-gray-700 pt-8">
        <p className="font-medium">TanyaSehat &copy; {new Date().getFullYear()} - Sistem Deteksi Penyakit Berbasis NLP</p>
        <p className="mt-2 text-xs opacity-75">Disclaimer: Hasil deteksi bersifat informatif dan tidak menggantikan konsultasi dengan tenaga medis profesional.</p>
        
        {/* Tampilkan tombol untuk menampilkan info kembali jika sudah disembunyikan */}
        {!showInfo && !isLoading && result && (
          <button 
            onClick={() => setShowInfo(true)} 
            className="mt-4 text-blue-500 hover:text-blue-600 text-xs px-3 py-1 rounded-full bg-blue-50 dark:bg-blue-900/30 hover:bg-blue-100 dark:hover:bg-blue-900/50 transition-colors focus:outline-none flex items-center mx-auto"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-3 w-3 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Tampilkan informasi penggunaan
          </button>
        )}
      </footer>

      {/* Theme toggle */}
      <ThemeToggle />
    </div>
  );
}
