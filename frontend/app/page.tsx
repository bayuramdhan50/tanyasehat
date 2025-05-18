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
  const [showInfo, setShowInfo] = useState(true);

  const handleResult = (data: any) => {
    setResult(data);
    setShowInfo(false); // Sembunyikan info setelah hasil diterima
  };

  const handleLoading = (loading: boolean) => {
    setIsLoading(loading);
  };

  const InfoCard = () => (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 w-full max-w-2xl mx-auto mt-8">
      <h2 className="text-xl font-bold mb-4">Selamat Datang di TanyaSehat</h2>
      
      <div className="prose dark:prose-invert prose-sm max-w-none">
        <p>
          TanyaSehat adalah sistem deteksi penyakit berbasis Natural Language Processing (NLP) 
          yang dapat membantu Anda mengidentifikasi kemungkinan penyakit berdasarkan gejala yang Anda alami.
        </p>
        
        <h3 className="text-lg font-medium mt-4">Cara Menggunakan:</h3>
        <ol className="list-decimal pl-5 space-y-2">
          <li>
            <strong>Deskripsikan gejala Anda</strong> dengan bahasa alami dalam kolom input. 
            Contoh: "Saya mengalami demam tinggi, sakit kepala, dan nyeri otot sejak 2 hari yang lalu."
          </li>
          <li>
            <strong>Gunakan fitur input suara</strong> dengan mengklik ikon mikrofon jika Anda lebih nyaman berbicara daripada mengetik.
          </li>
          <li>
            <strong>Klik tombol "Analisis Gejala"</strong> untuk mendapatkan hasil deteksi beserta rekomendasi.
          </li>
          <li>
            <strong>Konsultasikan dengan Asisten TanyaSehat</strong> di tab kedua untuk informasi lebih lanjut tentang penyakit atau perawatan kesehatan.
          </li>
        </ol>
        
        <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-900/30 rounded-lg">
          <p className="text-sm">
            <strong>Penting:</strong> Sistem ini dirancang sebagai alat bantu informatif dan bukan pengganti diagnosis medis profesional.
            Selalu konsultasikan dengan dokter untuk diagnosis dan perawatan yang tepat.
          </p>
        </div>
      </div>
      
      <button 
        onClick={() => setShowInfo(false)} 
        className="mt-4 text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 text-sm font-medium focus:outline-none"
      >
        Sembunyikan informasi ini
      </button>
    </div>
  );

  const tabs = [
    {
      id: 'detection',
      label: 'Deteksi Penyakit',
      content: (
        <div>
          <InputForm onResult={handleResult} onLoading={handleLoading} />
          {isLoading ? <Loading /> : result ? <ResultCard result={result} /> : showInfo && <InfoCard />}
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
        
        {/* Tampilkan tombol untuk menampilkan info kembali jika sudah disembunyikan */}
        {!showInfo && !isLoading && result && (
          <button 
            onClick={() => setShowInfo(true)} 
            className="mt-2 text-blue-500 hover:text-blue-600 text-xs underline focus:outline-none"
          >
            Tampilkan informasi penggunaan
          </button>
        )}
      </footer>
    </div>
  );
}
