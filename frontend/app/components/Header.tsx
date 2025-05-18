/**
 * Komponen Header untuk aplikasi TanyaSehat
 * Menampilkan judul dan deskripsi singkat aplikasi
 */
import Image from 'next/image';

export default function Header() {
  return (
    <header className="text-center mb-8">
      <div className="flex justify-center mb-4">
        <Image 
          src="/logo.svg" 
          alt="TanyaSehat Logo" 
          width={100} 
          height={100}
          priority
        />
      </div>
      <h1 className="text-3xl font-bold mb-2 text-primary">TanyaSehat</h1>
      <p className="text-gray-600 dark:text-gray-300">
        Sistem Deteksi Penyakit Berbasis NLP untuk Bahasa Indonesia
      </p>
    </header>
  );
}
