# TanyaSehat - Dokumentasi Pengembangan

## Ikhtisar Sistem

TanyaSehat adalah aplikasi web untuk mendeteksi kemungkinan penyakit berdasarkan gejala yang diinputkan pengguna dalam bahasa Indonesia menggunakan Natural Language Processing (NLP). Aplikasi ini terdiri dari dua komponen utama:

1. **Backend Flask**: Menangani preprocessing teks, klasifikasi penyakit, dan chatbot
2. **Frontend Next.js**: Antarmuka pengguna interaktif dengan dukungan input suara

## Fitur Utama

### 1. Deteksi Penyakit
- Input teks gejala dalam bahasa natural Indonesia
- Dukungan input suara (Speech-to-Text)
- Analisis gejala menggunakan NLP dan klasifikasi
- Visualisasi hasil dengan tingkat kepercayaan

### 2. Chatbot Asisten
- Tanya jawab tentang informasi penyakit
- Rekomendasi pencegahan dan pengobatan
- Dukungan sinonim dan variasi bahasa
- Saran pertanyaan kontekstual

## Perbaikan Terbaru

### 1. Perbaikan Chatbot
- Penambahan pola pengenalan pertanyaan yang lebih fleksibel
- Implementasi fuzzy matching untuk menangani typo dan variasi kata
- Dukungan sinonim untuk nama penyakit
- Peningkatan respons untuk pertanyaan yang tidak dikenali
- Penambahan saran pertanyaan yang kontekstual
- Visualisasi respons yang lebih baik

### 2. Peningkatan Input Pengguna
- Implementasi Speech-to-Text menggunakan Web Speech API
- Dukungan bahasa Indonesia untuk pengenalan suara
- Contoh deskripsi gejala untuk membantu pengguna
- Penanganan error yang lebih baik

### 3. Visualisasi Hasil
- Indikator visual untuk tingkat kepercayaan
- Penjelasan mendalam tentang tingkat kepercayaan
- Tampilan rekomendasi yang lebih terstruktur
- Tampilan kemungkinan penyakit alternatif

### 4. Pengalaman Pengguna
- Informasi panduan penggunaan aplikasi
- Tampilan yang responsif untuk berbagai perangkat
- Pesan peringatan dan disclaimer yang jelas
- Antarmuka yang intuitif dengan saran kontekstual

## Teknologi yang Digunakan

### Backend
- Python dengan Flask
- NLP: NLTK, Sastrawi (untuk stemming Bahasa Indonesia)
- Machine Learning: Scikit-learn (TF-IDF, Naive Bayes)
- JSON untuk penyimpanan data

### Frontend
- Next.js (React framework)
- TypeScript
- Tailwind CSS untuk styling
- Web Speech API untuk pengenalan suara

## Rencana Pengembangan Selanjutnya

1. **Penambahan Dataset**:
   - Memperluas kamus gejala penyakit
   - Menambahkan lebih banyak variasi deskripsi gejala

2. **Peningkatan Model**:
   - Implementasi model deep learning (jika diperlukan)
   - Peningkatan akurasi prediksi

3. **Fitur Baru**:
   - Riwayat diagnosis untuk pengguna yang login
   - Visualisasi statistik penyakit
   - Integrasi dengan API eksternal untuk informasi kesehatan

4. **Optimasi**:
   - Caching untuk meningkatkan performa
   - Progressive Web App (PWA) untuk penggunaan offline
