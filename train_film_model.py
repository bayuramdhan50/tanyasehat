#!/usr/bin/env python
"""
Script untuk training model FilmFinder
"""
import os
import sys
import pandas as pd
import joblib

# Tambahkan path ke root project
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.models.film_recommender import FilmRecommender

def train_model():
    """
    Training model FilmRecommender menggunakan data training
    """
    print("Memulai training model FilmFinder...")
    
    # Inisialisasi model
    film_recommender = FilmRecommender()
    
    # Path ke file training data
    training_data_path = os.path.join('data', 'training_films.csv')
    
    if not os.path.exists(training_data_path):
        print(f"Error: File {training_data_path} tidak ditemukan")
        return False
    
    try:
        # Load data training
        print(f"Membaca data training dari {training_data_path}")
        data = pd.read_csv(training_data_path)
        
        # Validasi data
        required_cols = ['preferences', 'film_genre']
        for col in required_cols:
            if col not in data.columns:
                print(f"Error: Kolom '{col}' tidak ditemukan di file training")
                return False
        
        print(f"Data training berhasil dimuat: {len(data)} baris")
        
        # Training model
        print("Melatih model FilmRecommender...")
        X = data['preferences'].tolist()
        y = data['film_genre'].tolist()
        
        # Training
        evaluation = film_recommender.train(X, y, test_size=0.2)
        
        # Simpan hasil evaluasi
        print("Hasil evaluasi model:")
        print(f"- Akurasi rata-rata: {evaluation.get('average_accuracy', 0)*100:.2f}%")
        
        # Detail untuk setiap genre
        for genre, metrics in evaluation.items():
            if genre != 'average_accuracy':
                print(f"- Genre '{genre}': Akurasi {metrics.get('accuracy', 0)*100:.2f}%")
        
        print("Model berhasil dilatih dan disimpan")
        
        # Cek file model
        model_path = os.path.join('models', 'film_recommender.joblib')
        if os.path.exists(model_path):
            print(f"File model disimpan di: {model_path}")
            
            # Tampilkan ukuran file
            size_mb = os.path.getsize(model_path) / (1024 * 1024)
            print(f"Ukuran file model: {size_mb:.2f} MB")
        
        return True
    
    except Exception as e:
        print(f"Error saat training model: {e}")
        return False

def test_model():
    """
    Menguji model dengan beberapa contoh input
    """
    print("\nMenguji model dengan contoh input...")
    
    # Inisialisasi model (akan memuat model yang sudah dilatih)
    film_recommender = FilmRecommender()
    
    # Contoh input untuk pengujian
    test_inputs = [
        "Saya suka film dengan aksi pertempuran dan efek visual keren",
        "Film romantis dengan alur cerita yang mengharukan",
        "Film horor yang menegangkan dan menakutkan",
        "Film animasi yang cocok untuk anak-anak",
        "Film sci-fi dengan konsep unik tentang masa depan"
    ]
    
    # Uji setiap input
    for input_text in test_inputs:
        print(f"\nInput: '{input_text}'")
        predictions = film_recommender.predict(input_text)
        
        print("Prediksi genre:")
        for genre_data in predictions.get('top_genres', []):
            print(f"- {genre_data['genre']}: {genre_data['confidence']*100:.2f}%")

def main():
    """
    Fungsi utama untuk training dan pengujian model
    """
    print("=" * 50)
    print("FilmFinder Model Training")
    print("=" * 50)
    
    # Jalankan training model
    success = train_model()
    
    if success:
        # Jalankan pengujian model
        test_model()
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
