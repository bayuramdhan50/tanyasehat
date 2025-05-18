from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import joblib
import json
import nltk

# Setup NLTK - Download resource yang dibutuhkan
def setup_nltk():
    """Download semua resource NLTK yang dibutuhkan aplikasi"""
    print("Menyiapkan resource NLTK...")
    # Pastikan resource punkt dan stopwords tersedia
    nltk.download('punkt_tab')
    nltk.download('stopwords')
    print("Resource NLTK berhasil disiapkan")

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
disease_classifier = DiseaseClassifier()
output_translator = OutputTranslator()
chatbot = Chatbot()

# Load model jika sudah ada
model_path = os.path.join('models', 'disease_classifier.joblib')
if os.path.exists(model_path):
    try:
        disease_classifier.load_model(model_path)
        print("Model berhasil dimuat dari", model_path)
    except Exception as e:
        print(f"Error saat memuat model: {e}")
        print("Model baru akan dibuat dan dilatih...")
        disease_classifier.train()
        disease_classifier.save_model(model_path)
else:
    print("Model tidak ditemukan. Model baru akan dibuat dan dilatih...")
    disease_classifier.train()
    disease_classifier.save_model(model_path)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint untuk health check"""
    return jsonify({'status': 'healthy'})

@app.route('/api/predict', methods=['POST'])
def predict_disease():
    """Endpoint untuk memprediksi penyakit berdasarkan gejala"""
    data = request.json
    
    if not data or 'text' not in data:
        return jsonify({'error': 'Data input tidak valid'}), 400
    
    # Ambil teks gejala dari request
    symptoms_text = data['text']
    
    # Preprocessing teks
    processed_text = preprocess_text(symptoms_text)
    
    # Prediksi penyakit
    prediction, confidence = disease_classifier.predict(processed_text)
    
    # Generate rekomendasi
    recommendation = output_translator.translate(prediction, confidence)
    
    # Menyiapkan response
    response = {
        'prediction': prediction,
        'confidence': confidence,
        'recommendation': recommendation
    }
    
    return jsonify(response)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint untuk chatbot sederhana"""
    data = request.json
    
    if not data or 'text' not in data:
        return jsonify({'error': 'Data input tidak valid'}), 400
    
    # Ambil teks pertanyaan dari request
    question = data['text']
    
    # Preprocessing teks
    processed_question = preprocess_text(question)
    
    # Dapatkan jawaban dari chatbot
    response = chatbot.get_response(processed_question, original_text=question)
    
    return jsonify({'response': response})

@app.route('/api/train', methods=['POST'])
def train_model():
    """Endpoint untuk melatih ulang model (hanya untuk development)"""
    try:
        disease_classifier.train()
        disease_classifier.save_model(model_path)
        return jsonify({'status': 'success', 'message': 'Model berhasil dilatih ulang'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
