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

  // Gunakan useEffect untuk merender hasil hanya sekali saat komponen di-mount atau hasil berubah
  useEffect(() => {
    const renderResults = () => {
      return (
        <>
          {/* Tab navigation */}
          <div className="flex border-b border-gray-200 dark:border-gray-700 mb-6">
            <button
              onClick={() => setActiveTab('result')}
              className={`py-2 px-4 font-medium text-sm focus:outline-none ${
                activeTab === 'result' 
                  ? 'border-b-2 border-blue-500 text-blue-600 dark:text-blue-400' 
                  : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'
              }`}
            >
              Hasil Utama
            </button>
            {result.top_diseases && result.top_diseases.length > 0 && (
              <button
                onClick={() => setActiveTab('details')}
                className={`py-2 px-4 font-medium text-sm focus:outline-none ${
                  activeTab === 'details' 
                    ? 'border-b-2 border-blue-500 text-blue-600 dark:text-blue-400' 
                    : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'
                }`}
              >
                Detail Hasil
              </button>
            )}
            {result.recommendation && result.recommendation.length > 0 && (
              <button
                onClick={() => setActiveTab('recommendations')}
                className={`py-2 px-4 font-medium text-sm focus:outline-none ${
                  activeTab === 'recommendations' 
                    ? 'border-b-2 border-blue-500 text-blue-600 dark:text-blue-400' 
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
                className={`mb-6 ${isUnknown ? 'bg-gray-50 dark:bg-gray-900/30' : 'bg-blue-50 dark:bg-blue-900/30'} p-4 rounded-lg`}
              >
                <div className="flex justify-between items-center mb-2">
                  <h3 className="font-semibold text-lg">Kemungkinan Penyakit:</h3>
                  <div className="flex items-center">
                    <span className="font-bold text-blue-600 dark:text-blue-400 mr-2">
                      {formatProbability(result.confidence)}
                    </span>
                    <div className="relative h-5 w-5 rounded-full">
                      <div 
                        className={`absolute inset-0 rounded-full ${getConfidenceColor(result.confidence)}`} 
                        title={getConfidenceMessage(result.confidence)}
                      ></div>
                    </div>
                  </div>
                </div>
                <p className={`text-2xl font-bold ${isUnknown ? 'text-gray-600 dark:text-gray-400' : 'text-blue-700 dark:text-blue-300'}`}>
                  {result.prediction}
                </p>
                
                {/* Visualisasi tingkat kepercayaan */}
                <div className="mt-5">
                  <div className="text-xs mb-1 flex justify-between">
                    <span>0%</span>
                    <span>50%</span>
                    <span>100%</span>
                  </div>
                  <div className="h-3 w-full bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                    <motion.div 
                      initial={{ width: 0 }}
                      animate={{ width: `${result.confidence * 100}%` }}
                      transition={{ duration: 1, ease: "easeOut" }}
                      className={`h-full ${getConfidenceColor(result.confidence)}`} 
                    ></motion.div>
                  </div>
                  <p className="text-sm text-gray-500 dark:text-gray-400 mt-2 font-medium text-center">
                    {getConfidenceMessage(result.confidence)}
                  </p>
                </div>

                {/* Penjelasan tingkat kepercayaan */}
                <div className="mt-4 p-3 bg-white dark:bg-gray-700 rounded-sm text-sm">
                  <p className="text-gray-600 dark:text-gray-300">
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
                <div className="bg-white dark:bg-gray-700 shadow-sm rounded-lg overflow-hidden">
                  <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-600">
                    <thead className="bg-gray-50 dark:bg-gray-800">
                      <tr>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                          Penyakit
                        </th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                          Probabilitas
                        </th>
                        <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-300 uppercase tracking-wider">
                          Visualisasi
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
                        <td className="px-6 py-4 whitespace-nowrap">
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
                          <td className="px-6 py-4 whitespace-nowrap">
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
