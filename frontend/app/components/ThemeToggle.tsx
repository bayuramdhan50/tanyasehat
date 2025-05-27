'use client'

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'

export default function ThemeToggle() {
  const [isDarkMode, setIsDarkMode] = useState(false)

  // Check initial theme
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const isDark = 
        window.matchMedia('(prefers-color-scheme: dark)').matches ||
        document.documentElement.classList.contains('dark')
      
      setIsDarkMode(isDark)
    }
  }, [])

  // Toggle theme
  const toggleTheme = () => {
    const newTheme = !isDarkMode
    setIsDarkMode(newTheme)

    // Update HTML class
    if (newTheme) {
      document.documentElement.classList.add('dark')
      localStorage.setItem('theme', 'dark')
    } else {
      document.documentElement.classList.remove('dark')
      localStorage.setItem('theme', 'light')
    }
  }

  return (
    <button
      onClick={toggleTheme}
      className="fixed bottom-4 right-4 z-50 p-2 rounded-full bg-white dark:bg-gray-800 shadow-lg border border-gray-200 dark:border-gray-700 focus:outline-none"
      aria-label={isDarkMode ? "Beralih ke mode terang" : "Beralih ke mode gelap"}
    >
      <motion.div 
        animate={{ rotate: isDarkMode ? 180 : 0 }}
        transition={{ duration: 0.5, type: "spring" }}
        className="w-7 h-7 relative"
      >
        {/* Sun */}
        <motion.div
          animate={{ opacity: isDarkMode ? 0 : 1 }}
          className="absolute inset-0 flex items-center justify-center text-yellow-500"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
        </motion.div>

        {/* Moon */}
        <motion.div
          animate={{ opacity: isDarkMode ? 1 : 0 }}
          className="absolute inset-0 flex items-center justify-center text-blue-400"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
          </svg>
        </motion.div>
      </motion.div>
    </button>
  )
}
