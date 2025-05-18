'use client'

import { useState } from 'react';
import Header from './components/Header';
import InputForm from './components/InputForm';
import ResultCard from './components/ResultCard';
import Chatbot from './components/Chatbot';
import Loading from './components/Loading';
import Tabs from './components/Tabs';

export default function Home() {
  const [result, setResult] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleResult = (data: any) => {
    setResult(data);
  };

  const handleLoading = (loading: boolean) => {
    setIsLoading(loading);
  };

  const tabs = [
    {
      id: 'detection',
      label: 'Deteksi Penyakit',
      content: (
        <div>
          <InputForm onResult={handleResult} onLoading={handleLoading} />
          {isLoading ? <Loading /> : result && <ResultCard result={result} />}
        </div>
      ),
    },
    {
      id: 'chatbot',
      label: 'Asisten TanyaSehat',
      content: <Chatbot />,
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-50 py-10 px-4 sm:px-6">
      <div className="max-w-4xl mx-auto">
        <Header />
        <Tabs tabs={tabs} />
      </div>
      
      <footer className="mt-20 text-center text-sm text-gray-500 dark:text-gray-400">
        <p>TanyaSehat &copy; {new Date().getFullYear()} - Sistem Deteksi Penyakit Berbasis NLP</p>
        <p className="mt-1">Disclaimer: Hasil deteksi bersifat informatif dan tidak menggantikan konsultasi dengan tenaga medis profesional.</p>
      </footer>
    </div>
  );
}
