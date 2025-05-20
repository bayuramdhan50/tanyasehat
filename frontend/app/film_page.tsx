import { Suspense } from 'react';
import Header from './components/Header';
import Tabs from './components/Tabs';
import Loading from './components/Loading';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col bg-gray-50 dark:bg-gray-900">
      <Header 
        title="FilmFinder"
        subtitle="Rekomendasi film berdasarkan preferensi Anda"
      />

      <div className="container mx-auto px-4 py-8">
        <Suspense fallback={<Loading />}>
          <Tabs
            tabs={[
              { id: 'recommender', label: 'Rekomendasi Film', default: true },
              { id: 'chatbot', label: 'Film Assistant' },
            ]}
          />
        </Suspense>
      </div>
    </main>
  );
}
