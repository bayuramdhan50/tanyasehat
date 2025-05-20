#!/usr/bin/env python
"""
Script utama untuk menjalankan aplikasi FilmFinder
"""
import os
import sys
import subprocess
import argparse

# Tambahkan path ke root project
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_backend():
    """
    Menjalankan backend Flask
    """
    from backend.app_film import app
    
    # Tentukan port
    port = int(os.environ.get('PORT', 5000))
    
    print(f"Menjalankan backend FilmFinder di port {port}...")
    print("Akses API di http://localhost:5000/api/health")
    
    # Jalankan Flask app
    app.run(host='0.0.0.0', port=port, debug=True)

def run_frontend():
    """
    Menjalankan frontend Next.js
    """
    # Pindah ke direktori frontend
    frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend')
    
    if not os.path.exists(frontend_dir):
        print(f"Error: Direktori frontend tidak ditemukan di {frontend_dir}")
        return
    
    # Simpan direktori saat ini
    current_dir = os.getcwd()
    
    try:
        # Pindah ke direktori frontend
        os.chdir(frontend_dir)
        
        # Jalankan Next.js dengan npm
        command = 'npm run dev'
        
        print("Menjalankan frontend FilmFinder...")
        print("Akses aplikasi di http://localhost:3000")
        
        # Execute command
        process = subprocess.Popen(command, shell=True)
        process.wait()
    except Exception as e:
        print(f"Error saat menjalankan frontend: {e}")
    finally:
        # Kembali ke direktori asal
        os.chdir(current_dir)

def setup_data():
    """
    Menjalankan script setup direktori dan data
    """
    from setup_film_directories import setup_directories
    
    print("Menyiapkan direktori dan data FilmFinder...")
    setup_directories()

def train_model():
    """
    Melatih model FilmRecommender
    """
    try:
        from train_film_model import main as train_main
        
        print("Memulai proses training model...")
        train_main()
    except ImportError:
        print("Error: Module train_film_model tidak ditemukan")
    except Exception as e:
        print(f"Error saat training model: {e}")

def main():
    """
    Fungsi utama untuk parsing argumen dan menjalankan komponen
    """
    parser = argparse.ArgumentParser(description='Jalankan aplikasi FilmFinder')
    parser.add_argument('--component', choices=['backend', 'frontend', 'setup', 'train', 'all'], 
                        default='backend', help='Komponen yang akan dijalankan')
    
    args = parser.parse_args()
    
    if args.component == 'backend':
        run_backend()
    elif args.component == 'frontend':
        run_frontend()
    elif args.component == 'setup':
        setup_data()
    elif args.component == 'train':
        train_model()
    elif args.component == 'all':
        # Jalankan semua komponen secara berurutan
        setup_data()
        train_model()
        # Jalankan backend sebagai proses terakhir
        # karena merupakan proses blocking
        run_backend()
    else:
        print(f"Komponen {args.component} tidak valid")

if __name__ == '__main__':
    main()
