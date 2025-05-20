# FilmFinder - Dokumentasi Pengembangan

## Ikhtisar Sistem

FilmFinder adalah aplikasi web untuk merekomendasikan film berdasarkan preferensi yang diinputkan pengguna dalam bahasa Indonesia menggunakan Natural Language Processing (NLP). Aplikasi ini terdiri dari dua komponen utama:

1. **Backend Flask**: Menangani preprocessing teks, klasifikasi genre film, rekomendasi film, dan chatbot
2. **Frontend Next.js**: Antarmuka pengguna interaktif dengan dukungan input suara

## Fitur Utama

### 1. Rekomendasi Film
- Input teks preferensi dalam bahasa natural Indonesia
- Dukungan input suara (Speech-to-Text)
- Analisis preferensi menggunakan NLP dan klasifikasi genre film
- Visualisasi hasil dengan tingkat kepercayaan rekomendasi

### 2. Chatbot Film Asisten
- Tanya jawab tentang informasi film
- Rekomendasi film berdasarkan genre
- Dukungan sinonim dan variasi bahasa
- Saran pertanyaan kontekstual tentang film

## Perbaikan Terbaru

### 1. Perbaikan Chatbot
- Penambahan pola pengenalan pertanyaan yang lebih fleksibel
- Implementasi fuzzy matching untuk menangani typo dan variasi kata
- Dukungan sinonim untuk judul film
- Peningkatan respons untuk pertanyaan yang tidak dikenali
- Penambahan saran pertanyaan yang kontekstual
- Visualisasi respons yang lebih baik

### 2. Peningkatan Input Pengguna
- Implementasi Speech-to-Text menggunakan Web Speech API
- Dukungan bahasa Indonesia untuk pengenalan suara
- Contoh preferensi film untuk membantu pengguna
- Penanganan error yang lebih baik

### 3. Visualisasi Hasil
- Indikator visual untuk tingkat kepercayaan rekomendasi
- Penjelasan mendalam tentang tingkat kesesuaian film dengan preferensi
- Tampilan rekomendasi film yang lebih terstruktur
- Tampilan alternatif film berdasarkan genre yang sama

### 4. Pengalaman Pengguna
- Informasi panduan penggunaan aplikasi
- Tampilan yang responsif untuk berbagai perangkat
- Antarmuka yang intuitif dengan saran kontekstual
- Tampilan detail film yang informatif

## Arsitektur Sistem

### 1. Modul Preprocessing
- Tokenisasi teks bahasa Indonesia
- Stemming menggunakan Sastrawi
- Penghapusan stopwords
- Normalisasi teks (slang, sinonim)
- Ekstraksi kata kunci film

### 2. Modul Rekomendasi Film
- Klasifikasi teks menggunakan TF-IDF
- Model Naive Bayes untuk prediksi genre
- Pendekatan multi-label untuk genre film
- Sistem perhitungan skor untuk rekomendasi film

### 3. Modul Translator
- Konversi hasil prediksi ke rekomendasi film
- Pemetaan genre ke film dalam database
- Filtering dan ranking film berdasarkan skor
- Formatting respons untuk frontend

### 4. Modul Chatbot
- Pengenalan pola pertanyaan film
- Pencarian fuzzy untuk judul film
- Penanganan query FAQ umum
- Respons informasi spesifik film

## Teknologi yang Digunakan

### Backend
- Python dengan Flask
- NLP: NLTK, Sastrawi (untuk stemming Bahasa Indonesia)
- Machine Learning: Scikit-learn (TF-IDF, Naive Bayes)
- JSON untuk penyimpanan data film

### Frontend
- Next.js (React framework)
- TypeScript
- Tailwind CSS untuk styling
- Web Speech API untuk pengenalan suara

## Rencana Pengembangan Selanjutnya

1. **Ekspansi Database Film**:
   - Penambahan lebih banyak film dengan data lengkap
   - Memperkaya informasi detail film (trailer, link streaming, dll)
   - Pengategorian film lebih spesifik (sub-genre)

2. **Peningkatan Model**:
   - Implementasi word embeddings untuk pemahaman semantik yang lebih baik
   - Eksplorasi model deep learning untuk rekomendasi
   - Personalisasi rekomendasi berdasarkan preferensi historis pengguna

3. **Fitur Baru**:
   - Sistem rating dan ulasan pengguna
   - Integrasi dengan API film eksternal (TMDB, OMDB)
   - Rekomendasi berdasarkan mood atau situasi pengguna

4. **Optimasi**:
   - Caching untuk meningkatkan performa
   - Progressive Web App (PWA) untuk penggunaan offline
   - Implementasi sistem ranking yang lebih canggih
