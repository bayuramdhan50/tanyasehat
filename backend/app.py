from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import joblib
import json
import nltk
import time
import traceback

# Setup NLTK - Download resource yang dibutuhkan
def setup_nltk():
    """Download semua resource NLTK yang dibutuhkan aplikasi"""
    print("Menyiapkan resource NLTK...")
    # Pastikan resource punkt dan stopwords tersedia
    try:
        nltk.download('punkt')
        nltk.download('stopwords')
        print("Resource NLTK berhasil disiapkan")
    except Exception as e:
        print(f"Gagal menyiapkan NLTK: {e}")

# Jalankan setup NLTK pertama kali
setup_nltk()

# Menambahkan path untuk import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import modul-modul aplikasi
from utils.preprocessor import preprocess_text
from models.classifier import DiseaseClassifier
from models.translator import OutputTranslator
from models.chatbot import Chatbot

app = Flask(__name__)
CORS(app)  # Mengaktifkan CORS untuk integrasi dengan frontend

# Inisialisasi Model
print("Menginisialisasi model...")
disease_classifier = DiseaseClassifier()
output_translator = OutputTranslator()
chatbot = Chatbot()

# Nama file model
model_filename = 'disease_classifier.joblib'
model_format_version = 2  # Versi format model saat ini

# Flag untuk memaksa pelatihan ulang (set True untuk memaksa melatih ulang model)
force_retrain = False

# Cek apakah model sudah ada
models_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models')
model_path = os.path.join(models_dir, model_filename)

if os.path.exists(model_path) and not force_retrain:
    try:
        disease_classifier.load_model(model_filename)
        print("Model berhasil dimuat dari", model_path)
    except Exception as e:
        print(f"Error saat memuat model: {e}")
        print("Model baru akan dibuat dan dilatih...")
        accuracy = disease_classifier.train()
        disease_classifier.save_model(model_filename)
        print(f"Model baru telah dilatih dengan akurasi: {accuracy:.4f}")
else:
    if force_retrain:
        print("Memaksa pelatihan ulang model...")
    else:
        print("Model tidak ditemukan. Model baru akan dibuat dan dilatih...")
    
    accuracy = disease_classifier.train()
    saved_path = disease_classifier.save_model(model_filename)
    print(f"Model baru telah dilatih dengan akurasi: {accuracy:.4f}")
    print(f"Model disimpan di: {saved_path}")

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint untuk health check"""
    return jsonify({'status': 'healthy'})

@app.route('/api/predict', methods=['POST'])
def predict_disease():
    """Endpoint untuk memprediksi penyakit berdasarkan gejala"""
    start_time = time.time()
    
    try:
        data = request.json
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Data input tidak valid'}), 400
          
        # Ambil teks gejala dari request
        symptoms_text = data['text']
        
        # Preprocessing teks
        processed_text = preprocess_text(symptoms_text)
        
        # Prediksi penyakit
        prediction, confidence, top_diseases = disease_classifier.predict(processed_text)
        
        # Format top diseases untuk response
        formatted_top_diseases = [
            {"name": disease, "probability": prob}
            for disease, prob in top_diseases
            if disease != prediction  # Jangan duplikat penyakit utama
        ]
        
        # Generate rekomendasi
        recommendation = output_translator.translate(prediction, confidence)
        
        # Menyiapkan response
        response = {
            'prediction': prediction,
            'confidence': confidence,
            'recommendation': recommendation,
            'top_diseases': formatted_top_diseases,
            'processing_time': f"{(time.time() - start_time):.2f} detik"
        }
        
        return jsonify(response)
    
    except Exception as e:
        print(f"Error pada endpoint predict: {e}")
        traceback.print_exc()
        return jsonify({
            'error': 'Terjadi kesalahan internal saat memproses permintaan',
            'message': str(e)
        }), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint untuk chatbot sederhana"""
    try:
        data = request.json
        
        if not data or 'text' not in data:
            return jsonify({'error': 'Data input tidak valid'}), 400
        
        # Ambil teks pertanyaan dari request
        question = data['text']
        
        # Preprocessing teks
        processed_question = preprocess_text(question)
        
        # Dapatkan jawaban dari chatbot
        response = chatbot.get_response(processed_question, original_text=question)
        
        # Log untuk debugging
        print(f"Pertanyaan: {question}")
        print(f"Preprocessing: {processed_question}")
        print(f"Jawaban: {response}")
        
        return jsonify({'response': response})
    
    except Exception as e:
        print(f"Error pada endpoint chat: {e}")
        traceback.print_exc()
        return jsonify({
            'error': 'Terjadi kesalahan internal saat memproses permintaan',
            'message': str(e)
        }), 500

@app.route('/api/train', methods=['POST'])
def train_model():
    """Endpoint untuk melatih ulang model (hanya untuk development)"""
    try:
        start_time = time.time()
        accuracy = disease_classifier.train()
        disease_classifier.save_model(model_path)
        
        training_time = time.time() - start_time
        
        return jsonify({
            'status': 'success', 
            'message': 'Model berhasil dilatih ulang',
            'accuracy': accuracy,
            'training_time': f"{training_time:.2f} detik"
        })
    except Exception as e:
        print(f"Error saat melatih ulang model: {e}")
        traceback.print_exc()
        return jsonify({
            'status': 'error', 
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
