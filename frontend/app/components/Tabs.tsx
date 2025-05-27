/**
 * Komponen Tabs untuk navigasi antar fitur aplikasi
 * Memungkinkan pengguna beralih antara deteksi penyakit dan chatbot
 */
'use client'

import { useState } from 'react';
import { motion } from 'framer-motion';

interface TabsProps {
  tabs: {
    id: string;
    label: string;
    content: React.ReactNode;
  }[];
  initialTabIndex?: number;
  onTabChange?: (index: number) => void;
}

export default function Tabs({ tabs, initialTabIndex = 0, onTabChange }: TabsProps) {
  const [activeTab, setActiveTab] = useState(tabs[initialTabIndex]?.id || tabs[0]?.id);

  return (
    <div className="w-full max-w-4xl mx-auto">
      <div className="flex justify-center sm:justify-start border-b border-gray-200 dark:border-gray-700 mb-8 pb-1 gap-1">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => {
              setActiveTab(tab.id);
              const newIndex = tabs.findIndex(t => t.id === tab.id);
              if (onTabChange && newIndex !== -1) {
                onTabChange(newIndex);
              }
            }}
            className={`py-3 px-6 font-medium text-sm sm:text-base rounded-t-lg transition-all duration-200 relative flex items-center ${
              activeTab === tab.id
                ? 'text-blue-600 bg-white dark:bg-gray-800 border-t border-r border-l border-gray-200 dark:border-gray-700 shadow-sm'
                : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50 dark:text-gray-400 dark:hover:text-gray-300 dark:hover:bg-gray-700/50'
            }`}
          >
            {tab.id === 'detection' && (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
              </svg>
            )}
            {tab.id === 'chatbot' && (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            )}
            {tab.label}
            {activeTab === tab.id && (
              <span className="absolute bottom-0 left-0 w-full h-0.5 bg-blue-600 dark:bg-blue-500"></span>
            )}
          </button>
        ))}
      </div>
      <div className="relative">
        {tabs.map((tab) => (
          <div
            key={tab.id}
            className={`${activeTab === tab.id ? 'block fadeIn' : 'hidden'}`}
          >
            {tab.content}
          </div>
        ))}
      </div>
    </div>
  );
}
