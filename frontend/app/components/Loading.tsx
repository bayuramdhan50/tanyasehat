/**
 * Komponen Loading untuk menampilkan indikator loading
 * Ditampilkan saat menunggu respons dari server
 */
export default function Loading() {
  return (
    <div className="flex items-center justify-center p-8">
      <div className="relative">
        <div className="h-16 w-16 rounded-full border-t-4 border-b-4 border-blue-500 animate-spin"></div>
        <div className="absolute top-0 left-0 h-16 w-16 rounded-full border-t-4 border-b-4 border-blue-200 animate-spin" style={{ animationDirection: 'reverse', animationDuration: '1s' }}></div>
      </div>
      <p className="ml-4 text-lg font-medium text-gray-600 dark:text-gray-300">Menganalisis data...</p>
    </div>
  );
}
