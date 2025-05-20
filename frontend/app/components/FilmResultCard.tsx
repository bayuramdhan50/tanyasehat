/**
 * Komponen FilmResultCard untuk menampilkan hasil rekomendasi film
 * Menampilkan film yang direkomendasikan beserta detail dan confidence score
 */
'use client'

import { useState, useEffect, memo, ReactElement } from 'react';
import { motion, AnimatePresence } from 'framer-motion'; // Perlu diinstall: npm install framer-motion

interface Film {
  title: string;
  description: string;
  genre: string;
  director: string;
  release_year: number;
  rating: number;
  confidence: number;
}

interface FilmResultCardProps {
  result: {
    message: string;
    recommendations: Film[];
  };
}

// Memoisasi komponen untuk mencegah render ulang yang tidak perlu
const FilmResultCard = memo(({ result }: FilmResultCardProps) => {
  const [activeFilmIndex, setActiveFilmIndex] = useState(0);
  const [activeTab, setActiveTab] = useState<'overview' | 'details'>('overview');
  
  // Reset active film ke film pertama ketika hasil berubah
  useEffect(() => {
    setActiveFilmIndex(0);
    setActiveTab('overview');
  }, [result]);

  if (!result || !result.recommendations || result.recommendations.length === 0) {
    return (
      <div className="w-full max-w-2xl mx-auto bg-white dark:bg-gray-800 rounded-xl shadow-md p-6 mt-6">
        <div className="text-center py-10">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-16 w-16 mx-auto text-gray-400 dark:text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 4v16M17 4v16M3 8h18M3 16h18" />
          </svg>
          <h3 className="mt-4 text-lg font-medium text-gray-700 dark:text-gray-300">Tidak Ada Rekomendasi Film</h3>
          <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
            Silakan masukkan preferensi film Anda untuk mendapatkan rekomendasi yang sesuai.
          </p>
        </div>
      </div>
    );
  }

  // Ambil film yang aktif
  const activeFilm = result.recommendations[activeFilmIndex];

  return (
    <div className="w-full max-w-2xl mx-auto bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden mt-6">
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
        <h2 className="text-lg font-semibold text-gray-800 dark:text-white">Rekomendasi Film</h2>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">{result.message}</p>
      </div>
      
      {/* Film Carousel Navigation */}
      <div className="flex overflow-x-auto p-4 gap-3 border-b border-gray-200 dark:border-gray-700">
        {result.recommendations.map((film, index) => (
          <button 
            key={index}
            className={`flex-shrink-0 px-4 py-2 rounded-lg transition-colors ${
              index === activeFilmIndex 
              ? 'bg-blue-600 text-white' 
              : 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600'
            }`}
            onClick={() => setActiveFilmIndex(index)}
          >
            <div className="flex flex-col items-start">
              <span className="text-sm font-medium truncate max-w-[150px]">{film.title}</span>
              <span className="text-xs opacity-75">{film.release_year}</span>
            </div>
          </button>
        ))}
      </div>
      
      {/* Active Film Details */}
      <div className="p-6">
        <AnimatePresence mode="wait">
          <motion.div
            key={activeFilmIndex}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="space-y-6"
          >
            {/* Film Header with Rating */}
            <div className="flex justify-between items-start">
              <div>
                <h3 className="text-xl font-bold text-gray-800 dark:text-white">{activeFilm.title}</h3>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  {activeFilm.release_year} • {activeFilm.genre}
                </p>
              </div>
              <div className="flex flex-col items-end">
                <div className="flex items-center">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-yellow-500" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                  <span className="ml-1 text-lg font-bold text-gray-800 dark:text-white">{activeFilm.rating.toFixed(1)}</span>
                </div>
                <div className="mt-1">
                  <span className={`text-xs font-medium px-2 py-1 rounded-full ${getConfidenceColor(activeFilm.confidence)}`}>
                    {activeFilm.confidence.toFixed(1)}% match
                  </span>
                </div>
              </div>
            </div>
            
            {/* Tabs */}
            <div className="border-b border-gray-200 dark:border-gray-700">
              <nav className="flex space-x-8">
                <button
                  onClick={() => setActiveTab('overview')}
                  className={`px-1 py-4 text-sm font-medium border-b-2 ${
                    activeTab === 'overview'
                    ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                    : 'border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'
                  }`}
                >
                  Ikhtisar
                </button>
                <button
                  onClick={() => setActiveTab('details')}
                  className={`px-1 py-4 text-sm font-medium border-b-2 ${
                    activeTab === 'details'
                    ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                    : 'border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'
                  }`}
                >
                  Detail
                </button>
              </nav>
            </div>
            
            {/* Content based on active tab */}
            <AnimatePresence mode="wait">
              {activeTab === 'overview' && (
                <motion.div
                  key="overview"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  transition={{ duration: 0.2 }}
                  className="space-y-4"
                >
                  <p className="text-gray-700 dark:text-gray-300">
                    {activeFilm.description}
                  </p>
                  
                  <div className="flex flex-wrap gap-2 mt-3">
                    {activeFilm.genre.split(',').map((genre, idx) => (
                      <span 
                        key={idx} 
                        className="px-2 py-1 text-xs rounded-md bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300"
                      >
                        {genre.trim()}
                      </span>
                    ))}
                  </div>
                </motion.div>
              )}
              
              {activeTab === 'details' && (
                <motion.div
                  key="details"
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -10 }}
                  transition={{ duration: 0.2 }}
                  className="space-y-3"
                >
                  <div className="grid grid-cols-3 gap-4 text-sm">
                    <div className="space-y-1">
                      <p className="font-medium text-gray-500 dark:text-gray-400">Sutradara</p>
                      <p className="text-gray-800 dark:text-gray-200">{activeFilm.director}</p>
                    </div>
                    
                    <div className="space-y-1">
                      <p className="font-medium text-gray-500 dark:text-gray-400">Tahun</p>
                      <p className="text-gray-800 dark:text-gray-200">{activeFilm.release_year}</p>
                    </div>
                    
                    <div className="space-y-1">
                      <p className="font-medium text-gray-500 dark:text-gray-400">Rating</p>
                      <div className="flex items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-yellow-500" viewBox="0 0 20 20" fill="currentColor">
                          <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                        </svg>
                        <span className="ml-1 text-gray-800 dark:text-gray-200">{activeFilm.rating.toFixed(1)}/10</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="mt-4 space-y-1">
                    <p className="font-medium text-gray-500 dark:text-gray-400">Genre</p>
                    <p className="text-gray-800 dark:text-gray-200">{activeFilm.genre}</p>
                  </div>
                  
                  <div className="mt-4">
                    <p className="font-medium text-gray-500 dark:text-gray-400">Kesesuaian dengan Preferensi</p>
                    <div className="mt-2 h-3 relative max-w-xl rounded-full overflow-hidden">
                      <div className="w-full h-full bg-gray-200 dark:bg-gray-700 absolute"></div>
                      <div
                        className={`h-full ${getProgressBarColor(activeFilm.confidence)} absolute`}
                        style={{ width: `${activeFilm.confidence}%` }}
                      ></div>
                    </div>
                    <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
                      Film ini {getMatchText(activeFilm.confidence)} dengan preferensi Anda
                    </p>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
            
            {/* Navigation Controls */}
            <div className="flex justify-between pt-4">
              <button
                onClick={() => setActiveFilmIndex(prev => Math.max(0, prev - 1))}
                disabled={activeFilmIndex === 0}
                className={`px-3 py-1.5 text-sm rounded-md ${
                  activeFilmIndex === 0
                  ? 'bg-gray-100 dark:bg-gray-800 text-gray-400 dark:text-gray-600 cursor-not-allowed'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                }`}
              >
                &larr; Sebelumnya
              </button>
              <span className="text-sm text-gray-500 dark:text-gray-400 self-center">
                {activeFilmIndex + 1} dari {result.recommendations.length}
              </span>
              <button
                onClick={() => setActiveFilmIndex(prev => Math.min(result.recommendations.length - 1, prev + 1))}
                disabled={activeFilmIndex === result.recommendations.length - 1}
                className={`px-3 py-1.5 text-sm rounded-md ${
                  activeFilmIndex === result.recommendations.length - 1
                  ? 'bg-gray-100 dark:bg-gray-800 text-gray-400 dark:text-gray-600 cursor-not-allowed'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
                }`}
              >
                Berikutnya &rarr;
              </button>
            </div>
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
});

// Untuk menampilkan warna sesuai dengan confidence score
function getConfidenceColor(confidence: number): string {
  if (confidence >= 80) return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300';
  if (confidence >= 60) return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300';
  if (confidence >= 40) return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300';
  return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300';
}

// Untuk warna progress bar sesuai confidence score
function getProgressBarColor(confidence: number): string {
  if (confidence >= 80) return 'bg-green-500';
  if (confidence >= 60) return 'bg-blue-500';
  if (confidence >= 40) return 'bg-yellow-500';
  return 'bg-red-500';
}

// Untuk teks kesesuaian berdasarkan confidence score
function getMatchText(confidence: number): string {
  if (confidence >= 80) return 'sangat sesuai';
  if (confidence >= 60) return 'cukup sesuai';
  if (confidence >= 40) return 'sesuai sebagian';
  return 'kurang sesuai';
}

FilmResultCard.displayName = 'FilmResultCard';

export default FilmResultCard;
