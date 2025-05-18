/**
 * Komponen ResultCard untuk menampilkan hasil deteksi penyakit
 * Menampilkan penyakit terdeteksi beserta probabilitas dan rekomendasi
 */
'use client'

interface Disease {
  name: string;
  probability: number;
  description?: string;
  recommendations?: string[];
}

interface ResultCardProps {
  result: {
    predicted_disease: string;
    probability: number;
    top_diseases?: Disease[];
    recommendations?: string[];
  };
}

export default function ResultCard({ result }: ResultCardProps) {
  // Format persentase probabilitas
  const formatProbability = (prob: number) => {
    return (prob * 100).toFixed(2) + '%';
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 w-full max-w-2xl mx-auto mt-8">
      <h2 className="text-xl font-bold mb-4 text-center">Hasil Analisis</h2>
      
      <div className="mb-6 bg-blue-50 dark:bg-blue-900/30 p-4 rounded-lg">
        <div className="flex justify-between items-center mb-2">
          <h3 className="font-semibold text-lg">Kemungkinan Penyakit:</h3>
          <span className="font-bold text-blue-600 dark:text-blue-400">
            {formatProbability(result.probability)}
          </span>
        </div>
        <p className="text-lg font-medium">{result.predicted_disease}</p>
      </div>
      
      {result.top_diseases && result.top_diseases.length > 0 && (
        <div className="mb-6">
          <h3 className="font-semibold mb-3">Kemungkinan Penyakit Lainnya:</h3>
          <ul className="space-y-2">
            {result.top_diseases.map((disease, index) => (
              <li 
                key={index}
                className="flex justify-between p-2 border-b border-gray-100 dark:border-gray-700"
              >
                <span>{disease.name}</span>
                <span className="text-gray-600 dark:text-gray-400">
                  {formatProbability(disease.probability)}
                </span>
              </li>
            ))}
          </ul>
        </div>
      )}
      
      {result.recommendations && result.recommendations.length > 0 && (
        <div>
          <h3 className="font-semibold mb-3">Rekomendasi:</h3>
          <ul className="list-disc pl-5 space-y-1">
            {result.recommendations.map((recommendation, index) => (
              <li key={index} className="text-gray-700 dark:text-gray-300">
                {recommendation}
              </li>
            ))}
          </ul>
        </div>
      )}
      
      <div className="mt-6 pt-4 border-t border-gray-200 dark:border-gray-700 text-center text-sm text-gray-500">
        <p>
          Hasil ini hanya bersifat informatif dan tidak menggantikan diagnosis medis profesional.
          Segera konsultasikan dengan dokter untuk penanganan lebih lanjut.
        </p>
      </div>
    </div>
  );
}
