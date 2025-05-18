# TanyaSehat - Sistem Deteksi Penyakit Berbasis NLP

Aplikasi web untuk mendeteksi kemungkinan penyakit berdasarkan gejala yang diinputkan pengguna dalam bahasa Indonesia menggunakan NLP (Natural Language Processing). TanyaSehat menggabungkan backend Flask dengan preprocessor teks bahasa Indonesia dan model klasifikasi penyakit, serta frontend Next.js untuk antarmuka pengguna yang modern dan responsif.

## Fitur

- Deteksi penyakit berdasarkan teks gejala yang diinputkan dalam bahasa Indonesia
- Preprocessing teks dalam bahasa Indonesia (tokenisasi, stemming, dan stopword removal)
- Klasifikasi teks menggunakan TF-IDF dan Naive Bayes
- Chatbot sederhana untuk menjawab pertanyaan tentang penyakit
- Rekomendasi kustom berdasarkan hasil prediksi penyakit
- Antarmuka pengguna yang responsif dan mobile-friendly
- Tampilan mode gelap (dark mode)

## Teknologi yang Digunakan

### Backend
- **Python** dengan **Flask** sebagai framework web
- **Scikit-learn** untuk pemodelan machine learning
- **Sastrawi** untuk stemming bahasa Indonesia
- **NLTK** untuk preprocessing teks
- **NumPy** dan **Pandas** untuk manipulasi data

### Frontend
- **Next.js** untuk aplikasi React dengan server-side rendering
- **TypeScript** untuk type safety
- **Tailwind CSS** untuk styling
- **Axios** untuk komunikasi dengan API

## Struktur Proyek

```
tanyasehat/
│
├── backend/
│   ├── app.py                     # Aplikasi Flask utama
│   ├── models/
│   │   ├── __init__.py
│   │   ├── classifier.py          # Model klasifikasi (TF-IDF + Naive Bayes)
│   │   ├── chatbot.py             # Fitur chatbot sederhana
│   │   └── translator.py          # Output translator (rekomendasi)
│   │
│   ├── data/
│   │   ├── diseases.json          # Data penyakit dan informasinya
│   │   ├── symptoms.json          # Lexicon gejala penyakit
│   │   └── training_data.csv      # Data latih (gejala -> penyakit)
│   │
│   └── utils/
│       ├── __init__.py
│       └── preprocessor.py        # Modul preprocessing teks bahasa Indonesia
│
├── frontend/
│   ├── app/
│   │   ├── components/            # Komponen UI React 
│   │   │   ├── Header.tsx
│   │   │   ├── InputForm.tsx
│   │   │   ├── ResultCard.tsx
│   │   │   ├── Chatbot.tsx
│   │   │   ├── Loading.tsx
│   │   │   └── Tabs.tsx
│   │   ├── globals.css            # Style global
│   │   ├── layout.tsx             # Layout utama
│   │   └── page.tsx               # Halaman utama
│   │
│   ├── public/                    # Asset statis
│   │   └── logo.svg               # Logo TanyaSehat
│   │
│   ├── next.config.ts             # Konfigurasi Next.js
│   ├── package.json               # Dependensi JavaScript
│   └── ...
│
├── requirements.txt               # Dependensi Python
└── README.md                      # Dokumentasi proyek
```

## Instalasi dan Pengaturan

### Prasyarat
- Python 3.7+
- Node.js 18+
- npm atau yarn

### Backend (Flask)

1. Buat virtual environment Python:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependensi:
   ```bash
   pip install -r requirements.txt
   ```

3. Jalankan aplikasi Flask:
   ```bash
   cd backend
   python app.py
   ```
   
   Server akan berjalan di http://localhost:5000

### Frontend (Next.js)

1. Install dependensi:
   ```bash
   cd frontend
   npm install
   # atau
   yarn install
   ```

2. Jalankan aplikasi Next.js dalam mode development:
   ```bash
   npm run dev
   # atau
   yarn dev
   ```
   
   Aplikasi akan berjalan di http://localhost:3000

## API Endpoints

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
    "predicted_disease": "Pneumonia",
    "probability": 0.85,
    "recommendations": [
      "Segera konsultasikan dengan dokter",
      "Istirahat yang cukup",
      "Minum banyak cairan"
    ]
  }
  ```

### 2. Chatbot
- **URL**: `/api/chat`
- **Method**: POST
- **Request Body**:
  ```json
  {
    "message": "Apa itu diabetes?"
  }
  ```
- **Response**:
  ```json
  {
    "response": "Diabetes adalah kondisi kronis yang ditandai dengan kadar gula darah tinggi..."
  }
  ```

## Pengembangan

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

### Melatih Ulang Model
Setelah menambahkan data baru ke `training_data.csv`, jalankan script:
```bash
cd backend
python -c "from models.classifier import train_model; train_model()"
```

## Lisensi

Proyek ini dilisensikan di bawah lisensi MIT.

## Kontributor

- Dibuat untuk Mata Kuliah Sistem Pakar - Semester 6
