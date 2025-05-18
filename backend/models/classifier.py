"""
Model Klasifikasi Penyakit menggunakan TF-IDF dan Naive Bayes
"""
import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

from utils.preprocessor import preprocess_text

class DiseaseClassifier:
    """
    Kelas untuk mengklasifikasikan penyakit berdasarkan teks gejala.
    Menggunakan TF-IDF dan Naive Bayes.
    """
    
    def __init__(self):
        """Inisialisasi model klasifikasi penyakit"""
        # Pipeline untuk preprocessing dan klasifikasi
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(max_features=5000, ngram_range=(1, 2))),
            ('clf', MultinomialNB(alpha=1.0))
        ])
        
        # Path ke file data training
        self.data_path = os.path.join('data', 'training_data.csv')
        
        # Dictionary untuk menyimpan semua penyakit dan gejala-gejalanya
        self.diseases_info = {}
        
        # Dictionary untuk menyimpan skor kepercayaan (confidence) model
        self.model_confidence = {}
    
    def load_data(self):
        """
        Memuat data training dari CSV.
        Jika file tidak ada, akan dibuat data contoh terlebih dahulu.
        """
        try:
            # Coba load file CSV jika sudah ada
            data = pd.read_csv(self.data_path)
            print(f"Data training berhasil dimuat dari {self.data_path}")
        except (FileNotFoundError, pd.errors.EmptyDataError):
            # Jika file belum ada, buat contoh data training
            print(f"File {self.data_path} tidak ditemukan. Membuat data contoh...")
            data = self._create_sample_data()
        
        return data
    
    def _create_sample_data(self):
        """
        Membuat contoh data training jika belum ada file CSV.
        Data ini berisi pasangan gejala -> penyakit untuk melatih model.
        """
        # Data contoh: gejala -> penyakit
        sample_data = [
            # Flu
            {"symptoms": "Demam tinggi, pilek, hidung tersumbat, bersin-bersin, batuk kering, sakit tenggorokan, nyeri otot", "disease": "Flu"},
            {"symptoms": "Badan panas dingin, kepala pusing, batuk pilek, hidung meler", "disease": "Flu"},
            {"symptoms": "Demam, nyeri otot, sakit kepala, bersin, hidung tersumbat, batuk", "disease": "Flu"},
            {"symptoms": "Badan menggigil, demam, batuk kering, sakit kepala, hidung meler", "disease": "Flu"},
            {"symptoms": "Suhu tubuh tinggi, lemas, bersin-bersin, nyeri tenggorokan, batuk", "disease": "Flu"},
            
            # Demam Berdarah
            {"symptoms": "Demam tinggi mendadak, nyeri di belakang mata, sakit kepala parah, ruam merah, nyeri sendi dan otot", "disease": "Demam Berdarah"},
            {"symptoms": "Demam 40 derajat, nyeri otot dan sendi, mual, muntah, bintik merah di kulit", "disease": "Demam Berdarah"},
            {"symptoms": "Panas tinggi selama 2-7 hari, nyeri sendi luar biasa, sakit kepala berat, bintik merah di anggota tubuh", "disease": "Demam Berdarah"},
            {"symptoms": "Demam tinggi, perdarahan gusi, mimisan, bintik merah di tubuh, mual dan muntah", "disease": "Demam Berdarah"},
            {"symptoms": "Panas tinggi, nyeri otot dan sendi parah, mata merah dan nyeri, lemas, bintik kemerahan", "disease": "Demam Berdarah"},
            
            # Tipes
            {"symptoms": "Demam tinggi berkelanjutan, sakit kepala, nafsu makan menurun, nyeri perut, sembelit atau diare", "disease": "Tipes"},
            {"symptoms": "Demam naik secara bertahap, lemas, sakit perut, tidak nafsu makan, lidah kotor", "disease": "Tipes"},
            {"symptoms": "Panas tinggi terus menerus, nyeri perut bagian kanan bawah, sembelit, lidah berselaput", "disease": "Tipes"},
            {"symptoms": "Demam lebih dari seminggu, sakit kepala, tidak nafsu makan, perut tidak nyaman", "disease": "Tipes"},
            {"symptoms": "Panas terus-menerus, lemas, mual, sakit perut, lidah kotor, konstipasi", "disease": "Tipes"},
            
            # TBC
            {"symptoms": "Batuk berdahak lebih dari 2 minggu, batuk darah, nyeri dada, demam, berkeringat di malam hari, berat badan turun", "disease": "TBC"},
            {"symptoms": "Batuk lama tidak sembuh, dahak kental, batuk darah, berat badan menurun drastis, keringat malam", "disease": "TBC"},
            {"symptoms": "Batuk terus-menerus lebih dari 3 minggu, sesak napas, nyeri dada, demam rendah, keringat malam, nafsu makan berkurang", "disease": "TBC"},
            {"symptoms": "Batuk darah, demam bertahap, berkeringat di malam hari, badan kurus, lemas", "disease": "TBC"},
            {"symptoms": "Batuk berdahak lebih dari sebulan, demam, nafsu makan hilang, berat badan turun, keringat malam", "disease": "TBC"},
            
            # Maag
            {"symptoms": "Nyeri ulu hati, perut kembung, mual, muntah, nafsu makan berkurang", "disease": "Maag"},
            {"symptoms": "Sakit perut bagian atas, kembung, sendawa terus-menerus, mual", "disease": "Maag"},
            {"symptoms": "Perih di ulu hati, perut terasa penuh, sering bersendawa, mual setelah makan", "disease": "Maag"},
            {"symptoms": "Nyeri perut seperti terbakar, kembung, mual, muntah, cepat kenyang", "disease": "Maag"},
            {"symptoms": "Perih di lambung, kembung, nafsu makan berkurang, mual muntah", "disease": "Maag"},
            
            # Asma
            {"symptoms": "Sesak napas, napas berbunyi, batuk-batuk, dada terasa berat", "disease": "Asma"},
            {"symptoms": "Sulit bernapas, napas berbunyi seperti mengi, batuk terutama malam hari", "disease": "Asma"},
            {"symptoms": "Sesak napas mendadak, dada terasa sempit, batuk kering, suara napas berbunyi", "disease": "Asma"},
            {"symptoms": "Kesulitan bernapas, batuk terus-menerus, dada sesak, napas bunyi seperti peluit", "disease": "Asma"},
            {"symptoms": "Serangan sesak napas, batuk, napas berbunyi, kesulitan tidur karena batuk", "disease": "Asma"},
            
            # Migrain
            {"symptoms": "Sakit kepala berdenyut di satu sisi, mual, muntah, sensitif terhadap cahaya dan suara", "disease": "Migrain"},
            {"symptoms": "Nyeri kepala parah, pandangan kabur, sensitif terhadap cahaya, mual", "disease": "Migrain"},
            {"symptoms": "Sakit kepala berdenyut, mual, sensitif terhadap suara, penglihatan berbayang", "disease": "Migrain"},
            {"symptoms": "Nyeri kepala sebelah, sensitif terhadap cahaya dan suara, mual, muntah", "disease": "Migrain"},
            {"symptoms": "Sakit kepala hebat, mual, mata berkunang-kunang, sensitif terhadap suara", "disease": "Migrain"},
            
            # Diare
            {"symptoms": "BAB cair lebih dari 3 kali sehari, sakit perut, kram perut, mual, muntah", "disease": "Diare"},
            {"symptoms": "BAB encer berkali-kali, perut kram, mual, lemas, dehidrasi", "disease": "Diare"},
            {"symptoms": "Buang air besar cair berkali-kali, sakit perut, mual, muntah, kurang nafsu makan", "disease": "Diare"},
            {"symptoms": "BAB encer terus menerus, perut sakit, kembung, mual, badan lemas", "disease": "Diare"},
            {"symptoms": "Mencret berkali-kali, kram perut, mual, muntah, haus terus", "disease": "Diare"},
            
            # Hipertensi
            {"symptoms": "Sakit kepala, pusing, jantung berdebar, sesak napas, telinga berdenging", "disease": "Hipertensi"},
            {"symptoms": "Sakit kepala parah, pusing, sesak napas, jantung berdebar kencang", "disease": "Hipertensi"},
            {"symptoms": "Pusing, sakit kepala terutama di tengkuk, wajah kemerahan, mudah lelah", "disease": "Hipertensi"},
            {"symptoms": "Pusing, leher kaku, pandangan kabur, sesak napas, jantung berdebar", "disease": "Hipertensi"},
            {"symptoms": "Sakit kepala, penglihatan kabur, jantung berdebar, sulit tidur", "disease": "Hipertensi"},
            
            # Diabetes
            {"symptoms": "Sering buang air kecil, selalu haus, selalu lapar, berat badan turun, pandangan kabur, luka lambat sembuh", "disease": "Diabetes"},
            {"symptoms": "Kencing terus-menerus, haus terus, lapar berlebihan, berat badan menurun", "disease": "Diabetes"},
            {"symptoms": "Sering kencing terutama malam hari, haus berlebihan, lemas, luka sulit sembuh", "disease": "Diabetes"},
            {"symptoms": "Kencing terus, selalu haus, nafsu makan bertambah, lemas, penglihatan kabur", "disease": "Diabetes"},
            {"symptoms": "Haus terus, sering pipis, cepat lelah, berat badan turun tanpa sebab", "disease": "Diabetes"}
        ]
        
        # Konversi ke DataFrame
        df = pd.DataFrame(sample_data)
        
        # Buat direktori data jika belum ada
        os.makedirs(os.path.dirname(self.data_path), exist_ok=True)
        
        # Simpan ke CSV
        df.to_csv(self.data_path, index=False)
        print(f"Data contoh berhasil dibuat dan disimpan ke {self.data_path}")
        
        return df
    
    def preprocess_training_data(self, data):
        """
        Melakukan preprocessing pada data training.
        
        Parameters
        ----------
        data : pandas.DataFrame
            DataFrame yang berisi kolom 'symptoms' dan 'disease'
        
        Returns
        -------
        pandas.DataFrame
            DataFrame yang telah dipreproses
        """
        # Buat kolom baru untuk teks yang sudah dipreproses
        data['processed_symptoms'] = data['symptoms'].apply(preprocess_text)
        
        # Kumpulkan informasi tentang penyakit dan gejalanya
        for disease in data['disease'].unique():
            disease_symptoms = data[data['disease'] == disease]['symptoms'].tolist()
            self.diseases_info[disease] = disease_symptoms
        
        return data
    
    def train(self):
        """
        Melatih model klasifikasi penyakit
        """
        # Muat data
        data = self.load_data()
        
        # Preprocess data
        data = self.preprocess_training_data(data)
        
        # Split data menjadi data training dan testing (80:20)
        X_train, X_test, y_train, y_test = train_test_split(
            data['processed_symptoms'], 
            data['disease'], 
            test_size=0.2, 
            random_state=42
        )
        
        # Latih model
        self.pipeline.fit(X_train, y_train)
        
        # Evaluasi model
        y_pred = self.pipeline.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        
        print(f"Akurasi model: {accuracy:.2f}")
        print("Classification Report:")
        print(report)
        
        # Hitung confidence untuk setiap kelas
        class_probas = self.pipeline.predict_proba(X_test)
        for i, disease in enumerate(self.pipeline.classes_):
            # Rata-rata confidence untuk setiap penyakit
            avg_confidence = np.mean([proba[i] for proba in class_probas])
            self.model_confidence[disease] = avg_confidence
        
        print("Model berhasil dilatih!")
        
        return accuracy
    
    def predict(self, text):
        """
        Memprediksi penyakit berdasarkan teks gejala
        
        Parameters
        ----------
        text : str
            Teks gejala yang akan diprediksi penyakitnya
        
        Returns
        -------
        tuple
            (nama_penyakit, confidence)
        """
        # Pastikan model sudah dilatih
        if not hasattr(self.pipeline, 'classes_'):
            self.train()
        
        # Prediksi
        predicted_disease = self.pipeline.predict([text])[0]
        
        # Prediksi probabilitas
        probas = self.pipeline.predict_proba([text])[0]
        # Ambil probabilitas tertinggi
        max_proba = max(probas)
        
        # Jika confidence terlalu rendah, kita ragu dengan prediksi
        if max_proba < 0.3:
            return "Tidak diketahui", max_proba
        
        return predicted_disease, max_proba
    
    def save_model(self, model_path):
        """
        Menyimpan model ke file
        
        Parameters
        ----------
        model_path : str
            Path untuk menyimpan model
        """
        # Buat direktori jika belum ada
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        # Simpan model
        joblib.dump(self.pipeline, model_path)
        print(f"Model berhasil disimpan ke {model_path}")
    
    def load_model(self, model_path):
        """
        Memuat model dari file
        
        Parameters
        ----------
        model_path : str
            Path untuk memuat model
        """
        self.pipeline = joblib.load(model_path)
        print(f"Model berhasil dimuat dari {model_path}")
        
        # Muat informasi penyakit dan gejala
        data = self.load_data()
        self.preprocess_training_data(data)
