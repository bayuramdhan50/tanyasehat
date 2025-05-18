# TanyaSehat - Sistem Deteksi Penyakit Berbasis NLP

<div align="center">
  <h3>Deteksi penyakit berdasarkan deskripsi gejala dalam Bahasa Indonesia</h3>
</div>

## 📋 Deskripsi

TanyaSehat adalah aplikasi web untuk mendeteksi kemungkinan penyakit berdasarkan gejala yang diinputkan pengguna dalam bahasa Indonesia. Sistem ini menggunakan Natural Language Processing (NLP) untuk memahami input pengguna dan memberikan prediksi berdasarkan model klasifikasi yang telah dilatih.

## ✨ Fitur

- 🔍 **Deteksi Penyakit**: Analisis gejala dalam bahasa natural untuk memprediksi kemungkinan penyakit
- 🎤 **Input Suara**: Dukungan untuk input suara (speech-to-text) dalam Bahasa Indonesia
- 🤖 **Chatbot Asisten**: Tanya jawab interaktif tentang informasi penyakit dan rekomendasi kesehatan
- 📊 **Visualisasi Hasil**: Tampilan hasil dengan indikator tingkat kepercayaan dan rekomendasi
- 🌙 **Mode Gelap**: Antarmuka yang nyaman untuk penggunaan di berbagai kondisi pencahayaan

## 🚀 Teknologi

### Backend
- Python 3.x
- Flask (Web framework)
- NLTK & Sastrawi (NLP untuk Bahasa Indonesia)
- Scikit-learn (Machine Learning)

### Frontend
- Next.js 15
- TypeScript
- Tailwind CSS
- Web Speech API

## 🛠️ Instalasi dan Penggunaan

### Prasyarat
- Python 3.8+
- Node.js 18+
- npm atau yarn

### Langkah Instalasi

#### Backend
1. Clone repositori ini
   ```bash
   git clone https://github.com/username/tanyasehat.git
   cd tanyasehat
   ```

2. Siapkan lingkungan virtual Python (opsional tapi disarankan)
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Install dependensi backend
   ```bash
   pip install -r requirements.txt
   ```

4. Jalankan server backend
   ```bash
   cd backend
   python app.py
   ```
   Server akan berjalan di http://localhost:5000

#### Frontend
1. Masuk ke direktori frontend
   ```bash
   cd frontend
   ```

2. Install dependensi frontend
   ```bash
   npm install
   # atau
   yarn install
   ```

3. Jalankan server development frontend
   ```bash
   npm run dev
   # atau
   yarn dev
   ```
   Frontend akan tersedia di http://localhost:3000

## 📚 Cara Menggunakan

1. Buka aplikasi di browser
2. Pilih tab "Deteksi Penyakit"
3. Deskripsikan gejala yang dialami dalam bahasa Indonesia (bisa melalui ketikan atau input suara)
4. Klik "Analisis Gejala" untuk mendapatkan hasil
5. Lihat hasil diagnosis beserta rekomendasi
6. Untuk pertanyaan lebih lanjut, gunakan tab "Asisten TanyaSehat"

## 📊 Struktur Proyek

```
tanyasehat/
├── backend/                   # Kode backend Flask
│   ├── app.py                 # Aplikasi utama Flask
│   ├── data/                  # Data untuk model
│   ├── docs/                  # Dokumentasi backend
│   ├── models/                # Model-model
│   │   ├── classifier.py      # Model klasifikasi penyakit
│   │   ├── chatbot.py         # Model chatbot sederhana
│   │   └── translator.py      # Translator hasil prediksi
│   └── utils/                 # Utilitas
│       └── preprocessor.py    # Preprocessing teks
├── frontend/                  # Kode frontend Next.js
│   ├── app/                   # Aplikasi Next.js
│   │   ├── components/        # Komponen React
│   │   ├── hooks/             # Custom React hooks
│   │   ├── types/             # TypeScript type definitions
│   │   ├── page.tsx           # Halaman utama
│   │   └── layout.tsx         # Layout aplikasi
│   ├── public/                # Aset statis
│   └── package.json           # Dependensi frontend
├── DOKUMENTASI.md             # Dokumentasi pengembangan
└── requirements.txt           # Dependensi backend
```

## 🔌 API Endpoints

### 1. Prediksi Penyakit
- **URL**: `/api/predict`
- **Method**: POST
- **Request Body**:
  ```json
  {
    "text": "Saya mengalami batuk berdahak, demam tinggi, dan nyeri dada saat bernapas"
  }
  ```
- **Response**:
  ```json
  {
    "prediction": "Pneumonia",
    "confidence": 0.85,
    "recommendation": [
      "Segera konsultasikan dengan dokter",
      "Istirahat yang cukup",
      "Minum banyak cairan"
    ],
    "top_diseases": [
      {"name": "Bronkitis", "probability": 0.12},
      {"name": "Asma", "probability": 0.03}
    ]
  }
  ```

### 2. Chatbot
- **URL**: `/api/chat`
- **Method**: POST
- **Request Body**:
  ```json
  {
    "text": "Apa itu diabetes?"
  }
  ```
- **Response**:
  ```json
  {
    "response": "Diabetes adalah kondisi kronis yang ditandai dengan kadar gula darah tinggi..."
  }
  ```

### 3. Melatih Ulang Model
- **URL**: `/api/train`
- **Method**: POST
- **Response**:
  ```json
  {
    "status": "success",
    "message": "Model berhasil dilatih ulang"
  }
  ```

## 🛠️ Pengembangan

### Menambahkan Data Penyakit Baru
Untuk menambahkan data penyakit baru, tambahkan entri ke file `backend/data/diseases.json` dengan format:

```json
{
  "nama_penyakit": {
    "description": "Deskripsi penyakit",
    "recommendations": ["Rekomendasi 1", "Rekomendasi 2"]
  }
}
```

Setelah itu, tambahkan contoh gejala di `backend/models/classifier.py` dan latih ulang model melalui endpoint `/api/train`.

## ⚠️ Disclaimer

Aplikasi ini hanya bersifat informatif dan **tidak** menggantikan konsultasi medis profesional. Hasil deteksi yang diberikan tidak dapat dianggap sebagai diagnosis medis. Selalu konsultasikan dengan dokter untuk diagnosis dan penanganan medis yang tepat.

## 👥 Kontributor

- Dibuat untuk Mata Kuliah Sistem Pakar - Semester 6

## 📄 Lisensi

Proyek ini tersedia di bawah lisensi MIT. Lihat file `LICENSE` untuk informasi selengkapnya.
