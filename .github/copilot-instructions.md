<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# FilmFinder - Sistem Rekomendasi Film Berbasis NLP

## Konteks Proyek
Proyek ini adalah aplikasi web untuk mencari rekomendasi dan informasi seputar film yang dicari dengan cara diinputkan pengguna dalam bahasa Indonesia menggunakan NLP (Natural Language Processing). Aplikasi terdiri dari backend Flask dan frontend Next.js.

## Spesifikasi Teknis
- Menggunakan Python untuk backend dengan Flask
- Menggunakan Next.js untuk frontend
- Preprocessing teks bahasa Indonesia (tokenisasi, stemming, stopword removal)
- Klasifikasi teks menggunakan TF-IDF dan Naive Bayes
- Chatbot sederhana untuk menjawab pertanyaan tentang film

## Konvensi Kode
- Gunakan bahasa Indonesia untuk semua komentar dan dokumentasi
- Gunakan snake_case untuk nama fungsi dan variabel di Python
- Gunakan camelCase untuk nama fungsi dan variabel di JavaScript/TypeScript
- Sertakan docstring untuk setiap fungsi dan kelas

## Fitur yang Perlu Diimplementasikan
1. Modul preprocessing teks dalam bahasa Indonesia
2. Dictionary/lexicon film dan genre film
3. Model klasifikasi teks (TF-IDF + Naive Bayes) untuk analisis preferensi film
4. Output translator untuk rekomendasi film berbasis hasil prediksi
5. Chatbot sederhana berbasis Flask API untuk informasi film
6. Frontend Next.js untuk mengirim input teks ke backend dan menampilkan hasil film
