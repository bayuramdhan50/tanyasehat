/**
 * Komponen ResultCard untuk menampilkan hasil deteksi penyakit
 * Menampilkan penyakit terdeteksi beserta probabilitas dan rekomendasi
 */
'use client'

import { useState } from 'react';

interface Disease {
  name: string;
  probability: number;
  description?: string;
  recommendations?: string[];
}

interface ResultCardProps {
  result: {
    prediction: string;
    confidence: number;
    recommendation: string[];
    top_diseases?: Disease[];
  };
}

export default function ResultCard({ result }: ResultCardProps) {
  const [showAllRecommendations, setShowAllRecommendations] = useState(false);
  
  // Format persentase probabilitas
  const formatProbability = (prob: number) => {
    return (prob * 100).toFixed(2) + '%';
  };

  // Menentukan warna berdasarkan tingkat kepercayaan
  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.7) return 'bg-green-500';
    if (confidence >= 0.5) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  // Menentukan pesan berdasarkan tingkat kepercayaan
  const getConfidenceMessage = (confidence: number) => {
    if (confidence >= 0.7) return 'Tingkat kepercayaan tinggi';
    if (confidence >= 0.5) return 'Tingkat kepercayaan sedang';
    return 'Tingkat kepercayaan rendah';
  };

  // Menentukan apakah prediksi tidak diketahui
  const isUnknown = result.prediction === "Tidak diketahui";
  
  // Teks dengan penjelasan tingkat kepercayaan
  const confidenceExplanation = isUnknown
    ? "Sistem tidak dapat menentukan diagnosis dengan pasti berdasarkan gejala yang diinputkan."
    : result.confidence >= 0.7
      ? "Tingkat kepercayaan tinggi menunjukkan bahwa gejala yang diinputkan memiliki korelasi kuat dengan penyakit yang terdeteksi."
      : result.confidence >= 0.5
        ? "Tingkat kepercayaan sedang menunjukkan bahwa ada kemungkinan penyakit lain dengan gejala serupa."
        : "Tingkat kepercayaan rendah menunjukkan bahwa gejala yang diinputkan tidak cukup spesifik. Sebaiknya konsultasikan dengan dokter.";

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 w-full max-w-2xl mx-auto mt-8">
      <h2 className="text-xl font-bold mb-4 text-center">Hasil Analisis</h2>
      
      <div className={`mb-6 ${isUnknown ? 'bg-gray-50 dark:bg-gray-900/30' : 'bg-blue-50 dark:bg-blue-900/30'} p-4 rounded-lg`}>
        <div className="flex justify-between items-center mb-2">
          <h3 className="font-semibold text-lg">Kemungkinan Penyakit:</h3>
          <div className="flex items-center">
            <span className="font-bold text-blue-600 dark:text-blue-400 mr-2">
              {formatProbability(result.confidence)}
            </span>
            <div className="relative h-5 w-5 rounded-full">
              <div className={`absolute inset-0 rounded-full ${getConfidenceColor(result.confidence)}`} 
                title={getConfidenceMessage(result.confidence)}></div>
            </div>
          </div>
        </div>
        <p className={`text-lg font-medium ${isUnknown ? 'text-gray-600 dark:text-gray-400' : ''}`}>
          {result.prediction}
        </p>
        
        {/* Visualisasi tingkat kepercayaan */}
        <div className="mt-3">
          <div className="text-xs mb-1 flex justify-between">
            <span>0%</span>
            <span>50%</span>
            <span>100%</span>
          </div>
          <div className="h-2 w-full bg-gray-200 dark:bg-gray-700 rounded overflow-hidden">
            <div 
              className={`h-full ${getConfidenceColor(result.confidence)}`} 
              style={{width: `${result.confidence * 100}%`}}
            ></div>
          </div>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1 text-center">
            {getConfidenceMessage(result.confidence)}
          </p>
        </div>
        
        {/* Penjelasan tingkat kepercayaan */}
        <div className="mt-3 p-2 bg-white dark:bg-gray-700 rounded-sm text-sm">
          <p className="text-gray-600 dark:text-gray-300">
            {confidenceExplanation}
          </p>
        </div>
      </div>
      
      {result.top_diseases && result.top_diseases.length > 0 && (
        <div className="mb-6">
          <h3 className="font-semibold mb-3">Kemungkinan Penyakit Lainnya:</h3>
          <ul className="space-y-2">
            {result.top_diseases.map((disease, index) => (
              <li 
                key={index}
                className="flex justify-between p-2 border-b border-gray-100 dark:border-gray-700"
              >
                <span>{disease.name}</span>
                <div className="flex items-center">
                  <span className="text-gray-600 dark:text-gray-400">
                    {formatProbability(disease.probability)}
                  </span>
                  <div className="ml-2 w-16 h-2 bg-gray-200 dark:bg-gray-700 rounded overflow-hidden">
                    <div 
                      className={`h-full ${getConfidenceColor(disease.probability)}`} 
                      style={{width: `${disease.probability * 100}%`}}
                    ></div>
                  </div>
                </div>
              </li>
            ))}
          </ul>
          
          {isUnknown && result.top_diseases.length > 1 && (
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-2 italic">
              Gejala yang Anda sampaikan menunjukkan potensi beberapa kondisi dengan tingkat kepercayaan rendah. 
              Konsultasikan dengan dokter untuk diagnosis yang akurat.
            </p>
          )}
        </div>
      )}
      
      {result.recommendation && result.recommendation.length > 0 && (
        <div>
          <h3 className="font-semibold mb-3">Rekomendasi:</h3>
          <ul className="list-disc pl-5 space-y-2">
            {result.recommendation.slice(0, showAllRecommendations ? result.recommendation.length : 3).map((rec: string, index: number) => (
              <li 
                key={index} 
                className={`${index === 0 && result.confidence < 0.6 ? 'text-red-600 dark:text-red-400 font-medium' : 'text-gray-700 dark:text-gray-300'}`}
              >
                {rec}
              </li>
            ))}
          </ul>
          
          {result.recommendation.length > 3 && (
            <button
              onClick={() => setShowAllRecommendations(!showAllRecommendations)}
              className="mt-2 text-blue-500 hover:text-blue-600 text-sm font-medium focus:outline-none"
            >
              {showAllRecommendations 
                ? "Tampilkan lebih sedikit" 
                : `Tampilkan semua rekomendasi (${result.recommendation.length})`}
            </button>
          )}
        </div>
      )}
      
      <div className="mt-6 pt-4 border-t border-gray-200 dark:border-gray-700">
        <div className="flex items-center p-3 bg-yellow-50 dark:bg-yellow-900/30 rounded-lg">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-yellow-500 mr-2 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p className="text-sm text-gray-600 dark:text-gray-300">
            Hasil ini hanya bersifat informatif dan tidak menggantikan diagnosis medis profesional.
            Segera konsultasikan dengan dokter untuk penanganan lebih lanjut.
          </p>
        </div>
      </div>
    </div>
  );
}
