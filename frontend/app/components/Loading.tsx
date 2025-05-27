/**
 * Komponen Loading untuk menampilkan indikator loading
 * Ditampilkan saat menunggu respons dari server
 */
export default function Loading() {
  return (
    <div className="flex flex-col items-center justify-center p-12 slideInUp">
      <div className="relative mb-6">
        <div className="h-20 w-20 rounded-full border-t-4 border-b-4 border-blue-600 animate-spin"></div>
        <div className="absolute top-0 left-0 right-0 bottom-0 flex items-center justify-center">
          <div className="h-12 w-12 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-blue-600 dark:text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
          </div>
        </div>
      </div>
      <div className="text-center">
        <p className="text-lg font-medium text-gray-700 dark:text-gray-200 mb-2">Menganalisis data...</p>
        <p className="text-sm text-gray-500 dark:text-gray-400">Sistem sedang memproses gejala yang Anda berikan</p>
      </div>
      <div className="mt-8 flex space-x-2">
        <div className="h-2 w-2 rounded-full bg-blue-600 animate-pulse delay-100"></div>
        <div className="h-2 w-2 rounded-full bg-blue-600 animate-pulse delay-300"></div>
        <div className="h-2 w-2 rounded-full bg-blue-600 animate-pulse delay-500"></div>
      </div>
    </div>
  );
}
