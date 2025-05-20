/**
 * Komponen Tabs untuk beralih antara fitur Rekomendasi dan Chatbot
 */
'use client'

import { useState, ReactNode } from 'react';
import FilmInputForm from './FilmInputForm';
import FilmResultCard from './FilmResultCard';
import FilmChatbot from './FilmChatbot';

interface Tab {
  id: string;
  label: string;
  default?: boolean;
}

interface TabsProps {
  tabs: Tab[];
}

export default function FilmTabs({ tabs }: TabsProps) {
  const [activeTab, setActiveTab] = useState<string>(
    tabs.find(tab => tab.default)?.id || tabs[0]?.id
  );
  
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  return (
    <div>
      {/* Tab Navigation */}
      <div className="border-b border-gray-200 dark:border-gray-700 mb-6">
        <nav className="flex space-x-8" aria-label="Tabs">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`
                py-4 px-1 border-b-2 font-medium text-sm
                ${activeTab === tab.id
                  ? 'border-blue-500 text-blue-600 dark:text-blue-400'
                  : 'border-transparent text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'
                }
              `}
              aria-current={activeTab === tab.id ? 'page' : undefined}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="py-4">
        {activeTab === 'recommender' && (
          <div className="space-y-6">
            <FilmInputForm 
              onResult={setResult}
              onLoading={setLoading}
            />
            {loading ? (
              <div className="w-full max-w-2xl mx-auto mt-6">
                <div className="animate-pulse space-y-4 p-6 bg-white dark:bg-gray-800 rounded-xl shadow-md">
                  <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-3/4"></div>
                  <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2"></div>
                  <div className="space-y-2">
                    <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded"></div>
                    <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-5/6"></div>
                  </div>
                  <div className="flex space-x-4">
                    <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded w-1/4"></div>
                    <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded w-1/4"></div>
                  </div>
                </div>
              </div>
            ) : (
              result && <FilmResultCard result={result} />
            )}
          </div>
        )}

        {activeTab === 'chatbot' && (
          <FilmChatbot />
        )}
      </div>
    </div>
  );
}
