/**
 * Komponen ResultCard untuk menampilkan hasil deteksi penyakit
 * Menampilkan penyakit terdeteksi beserta probabilitas dan rekomendasi
 */
'use client'

import { useState, useEffect, memo, ReactElement } from 'react';
import { motion, AnimatePresence } from 'framer-motion'; // Perlu diinstall: npm install framer-motion

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
    processing_time?: string;
  };
}

// Memoisasi komponen untuk mencegah render ulang yang tidak perlu
const ResultCard = memo(({ result }: ResultCardProps) => {
  const [showAllRecommendations, setShowAllRecommendations] = useState(false);
  const [showDetails, setShowDetails] = useState(false);
  const [activeTab, setActiveTab] = useState<'result' | 'details' | 'recommendations'>('result');
  const [renderedResults, setRenderedResults] = useState<ReactElement | null>(null);
  
  // Format persentase probabilitas
  const formatProbability = (prob: number) => {
    return (prob * 100).toFixed(2) + '%';
  };

  // Menentukan warna berdasarkan tingkat kepercayaan
  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.7) return 'bg-green-500 dark:bg-green-500';
    if (confidence >= 0.5) return 'bg-yellow-500 dark:bg-yellow-500';
    return 'bg-red-500 dark:bg-red-500';
  };

  // Menentukan warna teks berdasarkan tingkat kepercayaan
  const getConfidenceTextColor = (confidence: number) => {
    if (confidence >= 0.7) return 'text-green-600 dark:text-green-400';
    if (confidence >= 0.5) return 'text-yellow-600 dark:text-yellow-400';
    return 'text-red-600 dark:text-red-400';
  };

  // Menentukan pesan berdasarkan tingkat kepercayaan
  const getConfidenceMessage = (confidence: number) => {
    if (confidence >= 0.7) return 'Tingkat kepercayaan tinggi';
    if (confidence >= 0.5) return 'Tingkat kepercayaan sedang';
    return 'Tingkat kepercayaan rendah';
  };

  // Menentukan ikon berdasarkan tingkat kepercayaan
  const getConfidenceIcon = (confidence: number) => {
    if (confidence >= 0.7) {
      return (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
        </svg>
      );
    }
    if (confidence >= 0.5) {
      return (
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
        </svg>
      );
    }
    return (
      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
        <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
      </svg>
    );
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

  // Gunakan useEffect untuk merender hasil hanya sekali saat komponen di-mount atau hasil berubah
  useEffect(() => {
    const renderResults = () => {
      return (
        <>
          {/* Tab navigation */}
          <div className="flex border-b border-gray-200 dark:border-gray-700 mb-6">
            <button
              onClick={() => setActiveTab('result')}
              className={`py-3 px-5 font-medium text-sm focus:outline-none transition-colors duration-200 ${
                activeTab === 'result' 
                  ? 'border-b-2 border-blue-600 text-blue-600 dark:text-blue-400' 
                  : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'
              }`}
            >
              Hasil Utama
            </button>
            {result.top_diseases && result.top_diseases.length > 0 && (
              <button
                onClick={() => setActiveTab('details')}
                className={`py-3 px-5 font-medium text-sm focus:outline-none transition-colors duration-200 ${
                  activeTab === 'details' 
                    ? 'border-b-2 border-blue-600 text-blue-600 dark:text-blue-400' 
                    : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'
                }`}
              >
                Detail Hasil
              </button>
            )}
            {result.recommendation && result.recommendation.length > 0 && (
              <button
                onClick={() => setActiveTab('recommendations')}
                className={`py-3 px-5 font-medium text-sm focus:outline-none transition-colors duration-200 ${
                  activeTab === 'recommendations' 
                    ? 'border-b-2 border-blue-600 text-blue-600 dark:text-blue-400' 
                    : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'
                }`}
              >
                Rekomendasi
              </button>
            )}
          </div>

          <AnimatePresence mode="wait">
            {activeTab === 'result' && (
              <motion.div
                key="result"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.3 }}
                className={`mb-6 ${isUnknown ? 'bg-gray-50 dark:bg-gray-800/60' : 'bg-blue-50 dark:bg-blue-900/20'} p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700`}
              >
                <div className="flex justify-between items-center mb-4">
                  <h3 className="font-semibold text-lg text-gray-800 dark:text-gray-200">Kemungkinan Penyakit:</h3>
                  <div className="flex items-center">
                    <span className="font-bold text-lg text-blue-600 dark:text-blue-400 mr-2">
                      {formatProbability(result.confidence)}
                    </span>
                    <div className={`flex items-center justify-center h-6 w-6 rounded-full ${getConfidenceTextColor(result.confidence)}`}
                         title={getConfidenceMessage(result.confidence)}>
                      {getConfidenceIcon(result.confidence)}
                    </div>
                  </div>
                </div>
                
                <p className={`text-3xl font-bold mb-5 ${isUnknown ? 'text-gray-600 dark:text-gray-400' : 'text-blue-700 dark:text-blue-300'}`}>
                  {result.prediction}
                </p>
                
                {/* Visualisasi tingkat kepercayaan */}
                <div className="mt-6">
                  <div className="text-xs mb-2 flex justify-between">
                    <span className="text-gray-500 dark:text-gray-400">0%</span>
                    <span className="text-gray-500 dark:text-gray-400">50%</span>
                    <span className="text-gray-500 dark:text-gray-400">100%</span>
                  </div>
                  <div className="h-3 w-full bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                    <motion.div 
                      initial={{ width: 0 }}
                      animate={{ width: `${result.confidence * 100}%` }}
                      transition={{ duration: 1, ease: "easeOut" }}
                      className={`h-full ${getConfidenceColor(result.confidence)}`} 
                    ></motion.div>
                  </div>
                  <div className={`flex items-center justify-center mt-3 ${getConfidenceTextColor(result.confidence)}`}>
                    {getConfidenceIcon(result.confidence)}
                    <p className="text-sm font-medium ml-2">
                      {getConfidenceMessage(result.confidence)}
                    </p>
                  </div>
                </div>

                {/* Penjelasan tingkat kepercayaan */}
                <div className="mt-6 p-4 bg-white dark:bg-gray-700/50 rounded-lg text-sm border border-gray-100 dark:border-gray-600">
                  <p className="text-gray-600 dark:text-gray-300 leading-relaxed">
                    {confidenceExplanation}
                  </p>
                </div>

                {result.processing_time && (
                  <div className="mt-4 text-xs text-gray-500 dark:text-gray-400 text-right">
                    Waktu pemrosesan: {result.processing_time}
                  </div>
                )}
              </motion.div>
            )}

            {activeTab === 'details' && result.top_diseases && (
              <motion.div
                key="details"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.3 }}
                className="mb-6"
              >
                <div className="bg-white dark:bg-gray-800 shadow-md rounded-xl overflow-hidden border border-gray-100 dark:border-gray-700">
                  <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                    <thead className="bg-gray-50 dark:bg-gray-800/80">
                      <tr>
                        <th scope="col" className="px-6 py-4 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                          Penyakit
                        </th>
                        <th scope="col" className="px-6 py-4 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                          Probabilitas
                        </th>
                        <th scope="col" className="px-6 py-4 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider hidden sm:table-cell">
                          Tingkat Keyakinan
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white dark:bg-gray-700 divide-y divide-gray-200 dark:divide-gray-600">
                      {/* Penyakit utama */}
                      <tr className="bg-blue-50 dark:bg-blue-900/30">
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-blue-700 dark:text-blue-300">
                          {result.prediction}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-blue-600 dark:text-blue-400">
                          {formatProbability(result.confidence)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap hidden sm:table-cell">
                          <div className="w-full h-4 bg-gray-200 dark:bg-gray-600 rounded-full overflow-hidden">
                            <div 
                              className={`h-full ${getConfidenceColor(result.confidence)}`} 
                              style={{width: `${result.confidence * 100}%`}}
                            ></div>
                          </div>
                        </td>
                      </tr>
                      
                      {/* Penyakit lainnya */}
                      {result.top_diseases.map((disease, index) => (
                        <tr key={index} className={index % 2 === 0 ? 'bg-gray-50 dark:bg-gray-800/50' : ''}>
                          <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-700 dark:text-gray-300">
                            {disease.name}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600 dark:text-gray-400">
                            {formatProbability(disease.probability)}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap hidden sm:table-cell">
                            <div className="w-full h-3 bg-gray-200 dark:bg-gray-600 rounded-full overflow-hidden">
                              <div 
                                className={`h-full ${getConfidenceColor(disease.probability)}`}
                                style={{width: `${disease.probability * 100}%`}}
                              ></div>
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                
                {isUnknown && result.top_diseases.length > 1 && (
                  <p className="text-sm text-gray-500 dark:text-gray-400 mt-4 italic bg-yellow-50 dark:bg-yellow-900/30 p-3 rounded-lg">
                    Gejala yang Anda sampaikan menunjukkan potensi beberapa kondisi dengan tingkat kepercayaan rendah. 
                    Konsultasikan dengan dokter untuk diagnosis yang akurat.
                  </p>
                )}
              </motion.div>
            )}

            {activeTab === 'recommendations' && result.recommendation && (
              <motion.div
                key="recommendations"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -10 }}
                transition={{ duration: 0.3 }}
              >
                <div className="bg-white dark:bg-gray-700 p-4 rounded-lg shadow-sm">
                  <h3 className="font-semibold text-lg mb-4">Rekomendasi untuk {result.prediction}</h3>
                  
                  <ul className="space-y-3">
                    {result.recommendation.map((rec: string, index: number) => (
                      <motion.li 
                        key={index} 
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ duration: 0.3, delay: index * 0.1 }}
                        className={`flex ${index === 0 && result.confidence < 0.6 ? 'text-red-600 dark:text-red-400 font-medium' : 'text-gray-700 dark:text-gray-300'}`}
                      >
                        <span className="mr-2 text-blue-500">•</span>
                        <span>{rec}</span>
                      </motion.li>
                    ))}
                  </ul>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
          
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
        </>
      );
    };

    setRenderedResults(renderResults());
  }, [
    result.prediction, 
    result.confidence, 
    result.recommendation, 
    result.top_diseases,
    result.processing_time,
    isUnknown, 
    showAllRecommendations, 
    showDetails,
    activeTab,
    confidenceExplanation
  ]);

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6 w-full max-w-2xl mx-auto mt-8">
      <h2 className="text-xl font-bold mb-4 text-center pb-2 border-b border-gray-200 dark:border-gray-700">
        Hasil Analisis Gejala
      </h2>
      {renderedResults}
    </div>
  );
});

ResultCard.displayName = 'ResultCard';

export default ResultCard;
