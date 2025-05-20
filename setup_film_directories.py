#!/usr/bin/env python
"""
Script untuk setup direktori model dan data untuk FilmFinder
"""
import os
import sys
import shutil
import json
import csv

# Tambahkan path ke root project
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_directory(directory):
    """Membuat direktori jika belum ada"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Direktori {directory} berhasil dibuat")
    else:
        print(f"Direktori {directory} sudah ada")

def setup_directories():
    """Membuat struktur direktori yang diperlukan aplikasi"""
    print("Menyiapkan struktur direktori...")
    
    # Direktori utama yang diperlukan
    directories = [
        'models',
        'data', 
        'backend/models',
        'backend/utils',
        'backend/data',
        'frontend/app/components',
        'frontend/app/hooks'
    ]
    
    # Buat semua direktori
    for directory in directories:
        create_directory(directory)
    
    # Setup data
    setup_film_data()
    setup_faq_data()
    setup_training_data()
    
    # Salin file data ke direktori backend/data
    sync_data_to_backend()
    
    print("Setup direktori selesai!")

def setup_film_data():
    """Menyiapkan data film jika belum ada"""
    films_data_path = os.path.join('data', 'films.json')
    
    if not os.path.exists(films_data_path):
        print("File data film tidak ditemukan, membuat file baru dengan data contoh...")
        
        # Contoh data film minimal jika tidak ada file
        films_data = {
            "Dune": {
                "title": "Dune",
                "release_year": 2021,
                "director": "Denis Villeneuve",
                "genre": ["Sci-Fi", "Action", "Adventure", "Drama"],
                "description": "Film yang mengadaptasi novel fiksi ilmiah terkenal karya Frank Herbert.",
                "actors": ["Timothée Chalamet", "Rebecca Ferguson", "Oscar Isaac", "Zendaya"],
                "rating": 8.0,
                "duration": 155,
                "recommendations": ["Blade Runner 2049", "Arrival", "Interstellar"]
            },
            "Inception": {
                "title": "Inception",
                "release_year": 2010,
                "director": "Christopher Nolan",
                "genre": ["Sci-Fi", "Action", "Thriller"],
                "description": "Film fiksi ilmiah yang mengisahkan Dom Cobb, seorang pencuri terampil yang mencuri rahasia dari pikiran bawah sadar.",
                "actors": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Ellen Page"],
                "rating": 8.8,
                "duration": 148,
                "recommendations": ["Interstellar", "The Prestige", "Memento"]
            }
        }
        
        # Simpan data film ke file JSON
        with open(films_data_path, 'w', encoding='utf-8') as f:
            json.dump(films_data, f, ensure_ascii=False, indent=4)
        
        print(f"File {films_data_path} berhasil dibuat dengan data contoh")
    else:
        print(f"File {films_data_path} sudah ada")

def setup_faq_data():
    """Menyiapkan data FAQ jika belum ada"""
    faq_data_path = os.path.join('data', 'faq_films.json')
    
    if not os.path.exists(faq_data_path):
        print("File data FAQ tidak ditemukan, membuat file baru dengan data contoh...")
        
        # Contoh data FAQ minimal jika tidak ada file
        faq_data = {
            "umum": {
                "apa itu filmfinder": "FilmFinder adalah sistem rekomendasi film berbasis NLP yang membantu menemukan film sesuai preferensi Anda.",
                "rekomendasi film action terbaru": "Beberapa film action terbaru yang direkomendasikan termasuk 'John Wick 4', 'The Equalizer 3', dan 'Fast X'."
            },
            "genre_info": {
                "Action": "Genre film dengan penekanan pada adegan kekerasan atau fisik seperti perkelahian, adegan kejar-kejaran, atau aksi ketangkasan.",
                "Comedy": "Genre film yang bertujuan untuk membuat penonton tertawa dengan humor dan situasi lucu."
            },
            "film_detail": {
                "Dune": [
                    "film tentang planet gurun",
                    "film denis villeneuve",
                    "film sci-fi epik"
                ],
                "Inception": [
                    "film tentang mimpi",
                    "film christopher nolan",
                    "film dengan konsep mind-bending"
                ]
            }
        }
        
        # Simpan data FAQ ke file JSON
        with open(faq_data_path, 'w', encoding='utf-8') as f:
            json.dump(faq_data, f, ensure_ascii=False, indent=4)
        
        print(f"File {faq_data_path} berhasil dibuat dengan data contoh")
    else:
        print(f"File {faq_data_path} sudah ada")

def setup_training_data():
    """Menyiapkan data training jika belum ada"""
    training_data_path = os.path.join('data', 'training_films.csv')
    
    if not os.path.exists(training_data_path):
        print("File data training tidak ditemukan, membuat file baru dengan data contoh...")
        
        # Contoh data training minimal jika tidak ada file
        training_data = [
            ["preferences", "film_genre"],
            ["Saya suka film tentang pahlawan super dan pertempuran epic", "Action|Superhero"],
            ["Saya ingin menonton film dengan visual yang indah dan penuh fantasi", "Fantasy|Adventure"],
            ["Film dengan plot twist dan cerita yang membuat penasaran", "Thriller|Mystery"],
            ["Film yang menceritakan kisah nyata dan bersejarah", "Drama|Biography|Historical"],
            ["Saya mencari film komedi yang menghibur dan lucu", "Comedy"]
        ]
        
        # Simpan data training ke file CSV
        with open(training_data_path, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            for row in training_data:
                writer.writerow(row)
        
        print(f"File {training_data_path} berhasil dibuat dengan data contoh")
    else:
        print(f"File {training_data_path} sudah ada")

def sync_data_to_backend():
    """Menyalin data ke direktori backend/data"""
    data_files = ['films.json', 'faq_films.json', 'training_films.csv']
    
    print("Menyinkronkan file data ke backend...")
    
    for file in data_files:
        src_path = os.path.join('data', file)
        dst_path = os.path.join('backend', 'data', file)
        
        if os.path.exists(src_path):
            shutil.copy2(src_path, dst_path)
            print(f"File {file} disalin ke backend/data")
        else:
            print(f"Peringatan: File {src_path} tidak ditemukan, tidak dapat disalin")

if __name__ == "__main__":
    setup_directories()
