/**
 * Komponen Header untuk aplikasi TanyaSehat
 * Menampilkan judul dan deskripsi singkat aplikasi
 */
'use client'

import Image from 'next/image';
import { motion } from 'framer-motion';

export default function Header() {
  return (
    <motion.header 
      className="text-center mb-12"
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="flex justify-center mb-6 relative">
        <motion.div 
          className="absolute -z-10 w-28 h-28 bg-blue-100 dark:bg-blue-900/30 rounded-full blur-xl opacity-70"
          animate={{ 
            scale: [1, 1.05, 1],
          }}
          transition={{ 
            repeat: Infinity,
            duration: 4,
            ease: "easeInOut",
          }}
        ></motion.div>
        <motion.div
          whileHover={{ rotate: [0, -5, 5, -5, 0], scale: 1.05 }}
          transition={{ duration: 0.5 }}
        >
          <Image 
            src="/logo.svg" 
            alt="TanyaSehat Logo" 
            width={120} 
            height={120}
            priority
            className="drop-shadow-md"
          />
        </motion.div>
      </div>
      <motion.h1 
        className="text-4xl font-bold mb-3 text-primary bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-indigo-600 dark:from-blue-400 dark:to-indigo-400"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2, duration: 0.7 }}
      >
        TanyaSehat
      </motion.h1>
      <motion.p 
        className="text-gray-600 dark:text-gray-300 max-w-md mx-auto text-lg"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4, duration: 0.7 }}
      >
        Sistem Deteksi Penyakit Berbasis NLP untuk Bahasa Indonesia
      </motion.p>
      
      <motion.div 
        className="mt-6 flex justify-center space-x-3"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.6, duration: 0.7 }}
      >
        <span className="px-3 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded-full dark:bg-blue-900/50 dark:text-blue-300">
          Bahasa Indonesia
        </span>
        <span className="px-3 py-1 bg-indigo-100 text-indigo-800 text-xs font-medium rounded-full dark:bg-indigo-900/50 dark:text-indigo-300">
          NLP
        </span>
        <span className="px-3 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full dark:bg-green-900/50 dark:text-green-300">
          Kesehatan
        </span>
      </motion.div>
    </motion.header>
  );
}
