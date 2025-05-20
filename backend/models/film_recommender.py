"""
Model Klasifikasi Film menggunakan TF-IDF dan Naive Bayes
"""
import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB, ComplementNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from sklearn.ensemble import VotingClassifier
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer
import joblib

from backend.utils.film_preprocessor import preprocess_text

class FilmRecommender:
    """
    Kelas untuk merekomendasikan film berdasarkan teks preferensi pengguna.
    Menggunakan TF-IDF dan Naive Bayes dengan optimasi parameter.
    """
    
    def __init__(self):
        """Inisialisasi model rekomendasi film"""
        # Pipeline untuk preprocessing dan klasifikasi dengan parameter yang dioptimalkan
        self.pipeline = Pipeline([
            ('tfidf', TfidfVectorizer(
                max_features=10000,  # Meningkatkan jumlah fitur untuk menangkap lebih banyak pola
                ngram_range=(1, 3),  # Menggunakan n-gram dari 1 hingga 3 untuk menangkap frasa
                min_df=2,            # Minimal muncul di 2 dokumen
                max_df=0.9,          # Maksimal muncul di 90% dokumen
                use_idf=True,        # Gunakan inverse document frequency
                sublinear_tf=True,   # Skala logaritmik untuk term frequency
            )),
            ('clf', MultinomialNB(alpha=0.1)),  # Naive Bayes dengan smoothing yang sesuai
        ])
        
        # Label encoder untuk genre film
        self.label_encoder = None
        self.multilabel_binarizer = None
        
        # Path penyimpanan model
        self.model_path = os.path.join('models', 'film_recommender.joblib')
        
        # Load model jika sudah ada
        if os.path.exists(self.model_path):
            self._load_model()
    
    def _preprocess_data(self, X):
        """
        Melakukan preprocessing pada data teks
        
        Parameters
        ----------
        X : list
            List dari string preferensi pengguna
            
        Returns
        -------
        list
            List dari string hasil preprocessing
        """
        return [preprocess_text(text) for text in X]
    
    def prepare_multilabel_data(self, y):
        """
        Menyiapkan data untuk klasifikasi multilabel
        
        Parameters
        ----------
        y : list
            List dari string genre yang dipisahkan dengan '|'
            
        Returns
        -------
        numpy.ndarray
            Matrix one-hot encoding untuk label multilabel
        """
        # Split genre dengan separator '|'
        genres_list = [genres.split('|') for genres in y]
        
        # Gunakan MultiLabelBinarizer untuk encoding
        if self.multilabel_binarizer is None:
            self.multilabel_binarizer = MultiLabelBinarizer()
            return self.multilabel_binarizer.fit_transform(genres_list)
        else:
            return self.multilabel_binarizer.transform(genres_list)
    
    def train(self, X, y, test_size=0.2, random_state=42):
        """
        Melatih model klasifikasi dengan data pelatihan
        
        Parameters
        ----------
        X : list
            List dari string preferensi film
        y : list
            List dari string genre film (bisa multilabel dengan separator '|')
        test_size : float, optional
            Proporsi data pengujian, by default 0.2
        random_state : int, optional
            Seed untuk random number generator, by default 42
            
        Returns
        -------
        dict
            Dictionary berisi metrik evaluasi model
        """
        # Preprocessing data teks
        X_prep = self._preprocess_data(X)
        
        # Menyiapkan data multilabel
        y_multilabel = self.prepare_multilabel_data(y)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_prep, y_multilabel, test_size=test_size, random_state=random_state
        )
        
        # Latih model untuk setiap genre (pendekatan OneVsRest implisit)
        for i in range(y_multilabel.shape[1]):
            genre_pipeline = Pipeline([
                ('tfidf', TfidfVectorizer(
                    max_features=10000,
                    ngram_range=(1, 3),
                    min_df=2,
                    max_df=0.9,
                    use_idf=True,
                    sublinear_tf=True,
                )),
                ('clf', MultinomialNB(alpha=0.1)),
            ])
            
            # Latih pada genre saat ini
            genre_pipeline.fit(X_train, y_train[:, i])
            
            # Tambahkan ke daftar model
            genre_name = self.multilabel_binarizer.classes_[i]
            setattr(self, f'pipeline_{genre_name}', genre_pipeline)
        
        # Evaluasi model
        evaluation = self._evaluate_model(X_test, y_test)
        
        # Simpan model
        self._save_model()
        
        return evaluation
    
    def _evaluate_model(self, X_test, y_test):
        """
        Mengevaluasi model pada data pengujian
        
        Parameters
        ----------
        X_test : list
            List dari string preferensi film pada data pengujian
        y_test : numpy.ndarray
            Matrix one-hot encoding untuk label multilabel pada data pengujian
            
        Returns
        -------
        dict
            Dictionary berisi metrik evaluasi model
        """
        # Dictionary untuk menyimpan hasil evaluasi
        evaluation = {}
        
        # Evaluasi setiap model genre
        for i, genre in enumerate(self.multilabel_binarizer.classes_):
            pipeline = getattr(self, f'pipeline_{genre}')
            y_pred = pipeline.predict(X_test)
            
            # Hitung akurasi
            acc = accuracy_score(y_test[:, i], y_pred)
            evaluation[genre] = {
                'accuracy': acc,
                'classification_report': classification_report(y_test[:, i], y_pred, output_dict=True)
            }
        
        # Hitung akurasi rata-rata
        accuracies = [evaluation[genre]['accuracy'] for genre in self.multilabel_binarizer.classes_]
        evaluation['average_accuracy'] = sum(accuracies) / len(accuracies)
        
        return evaluation
    
    def predict(self, text):
        """
        Memprediksi genre film berdasarkan teks preferensi pengguna
        
        Parameters
        ----------
        text : str
            Teks preferensi pengguna
            
        Returns
        -------
        dict
            Dictionary berisi hasil prediksi dengan confidence score
        """
        # Preprocessing teks
        text_prep = preprocess_text(text)
        
        # Prediksi untuk setiap genre
        result = {}
        predictions = []
        scores = []
        
        # Ambil prediksi dari setiap model genre
        for genre in self.multilabel_binarizer.classes_:
            pipeline = getattr(self, f'pipeline_{genre}', None)
            if pipeline:
                # Prediksi probabilitas
                proba = pipeline.predict_proba([text_prep])[0]
                prob_positive = proba[1] if len(proba) > 1 else 0
                
                # Simpan genre dan probability-nya
                predictions.append(genre)
                scores.append(prob_positive)
        
        # Urutkan berdasarkan skor prediksi
        sorted_indices = np.argsort(scores)[::-1]
        sorted_predictions = [predictions[i] for i in sorted_indices]
        sorted_scores = [scores[i] for i in sorted_indices]
        
        # Ambil top 5 prediksi atau semuanya jika kurang dari 5
        top_n = min(5, len(sorted_predictions))
        result['top_genres'] = [
            {'genre': sorted_predictions[i], 'confidence': sorted_scores[i]}
            for i in range(top_n)
        ]
        
        return result
    
    def _save_model(self):
        """
        Menyimpan model ke file
        """
        # Buat direktori jika belum ada
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        
        # Kumpulkan semua komponen model yang akan disimpan
        model_data = {
            'multilabel_binarizer': self.multilabel_binarizer
        }
        
        # Tambahkan semua pipeline genre ke model_data
        for genre in self.multilabel_binarizer.classes_:
            model_data[f'pipeline_{genre}'] = getattr(self, f'pipeline_{genre}')
        
        # Simpan model
        joblib.dump(model_data, self.model_path)
        print(f"Model berhasil disimpan ke {self.model_path}")
    
    def _load_model(self):
        """
        Memuat model dari file
        """
        try:
            model_data = joblib.load(self.model_path)
            
            # Muat multilabel binarizer
            self.multilabel_binarizer = model_data['multilabel_binarizer']
            
            # Muat semua pipeline genre
            for genre in self.multilabel_binarizer.classes_:
                setattr(self, f'pipeline_{genre}', model_data[f'pipeline_{genre}'])
            
            print(f"Model berhasil dimuat dari {self.model_path}")
        except Exception as e:
            print(f"Gagal memuat model: {e}")
            # Reset model jika gagal memuat
            self.multilabel_binarizer = None

    def train_from_csv(self, csv_path, preferences_col='preferences', genre_col='film_genre', 
                      test_size=0.2, random_state=42):
        """
        Melatih model dari file CSV
        
        Parameters
        ----------
        csv_path : str
            Path ke file CSV
        preferences_col : str, optional
            Nama kolom berisi teks preferensi user, by default 'preferences'
        genre_col : str, optional
            Nama kolom berisi genre film, by default 'film_genre'
        test_size : float, optional
            Proporsi data pengujian, by default 0.2
        random_state : int, optional
            Seed untuk random number generator, by default 42
            
        Returns
        -------
        dict
            Dictionary berisi metrik evaluasi model
        """
        # Baca data dari CSV
        try:
            data = pd.read_csv(csv_path)
            
            # Ekstrak preferensi dan genre
            X = data[preferences_col].tolist()
            y = data[genre_col].tolist()
            
            # Latih model
            return self.train(X, y, test_size=test_size, random_state=random_state)
        except Exception as e:
            print(f"Gagal melatih model dari CSV: {e}")
            return None
