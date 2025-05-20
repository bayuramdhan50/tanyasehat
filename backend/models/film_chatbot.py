"""
Chatbot sederhana untuk menjawab pertanyaan tentang film
"""
import os
import json
import re
import numpy as np
from backend.utils.film_preprocessor import preprocess_text
from difflib import get_close_matches
from difflib import SequenceMatcher

class FilmChatbot:
    """
    Kelas untuk chatbot sederhana yang menjawab pertanyaan tentang film
    """
    
    def __init__(self):
        """
        Inisialisasi chatbot
        """
        # Path ke file data film
        self.films_data_path = os.path.join('data', 'films.json')
        # Path ke file data FAQ
        self.faq_data_path = os.path.join('data', 'faq_films.json')
        
        # Muat data film
        self.films_data = self._load_films_data()
        # Muat data FAQ
        self.faq_data = self._load_faq_data()

        # Siapkan kamus sinonim film untuk meningkatkan pengenalan
        self.film_synonyms = self._prepare_film_synonyms()
        
        # Pattern untuk mendeteksi tipe pertanyaan
        self.question_patterns = {
            'rekomendasi': [
                r'rekomendasi\s+film',
                r'rekomen(d|k)asi',
                r'film\s+rekomendasi',
                r'film\s+yang\s+bagus',
                r'film\s+apa\s+yang',
                r'film\s+seperti',
                r'film\s+terbaik',
                r'film\s+populer',
                r'film\s+trending',
                r'film\s+rating\s+tinggi'
            ],
            'informasi': [
                r'informasi\s+tentang\s+film',
                r'info\s+film',
                r'film\s+apa\s+itu',
                r'apa\s+itu\s+film',
                r'cerita\s+film',
                r'sinopsis\s+film',
                r'tentang\s+film',
                r'jalan\s+cerita\s+film'
            ],
            'genre': [
                r'film\s+genre',
                r'genre\s+film',
                r'film\s+bertema',
                r'film\s+dengan\s+tema',
                r'film\s+bergenre',
                r'film\s+kategori'
            ],
            'aktor': [
                r'film\s+dengan\s+aktor',
                r'film\s+dengan\s+pemain',
                r'film\s+dibintangi',
                r'aktor\s+dalam\s+film',
                r'pemain\s+film',
                r'pemeran\s+film'
            ],
            'sutradara': [
                r'film\s+dari\s+sutradara',
                r'film\s+garapan',
                r'film\s+karya',
                r'sutradara\s+film',
                r'film\s+disutradarai',
                r'film\s+arahan'
            ],
            'tahun': [
                r'film\s+tahun',
                r'film\s+dari\s+tahun',
                r'film\s+dirilis',
                r'film\s+rilis',
                r'film\s+keluaran\s+tahun'
            ]
        }
    
    def _load_films_data(self):
        """
        Memuat data film dari JSON
        
        Returns
        -------
        dict
            Dictionary berisi informasi film
        """
        try:
            with open(self.films_data_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Buat contoh data default jika file tidak ditemukan
            default_data = {
                "Dune": {
                    "title": "Dune",
                    "release_year": 2021,
                    "director": "Denis Villeneuve",
                    "genre": ["Sci-Fi", "Action", "Adventure", "Drama"],
                    "description": "Film yang mengadaptasi novel fiksi ilmiah terkenal karya Frank Herbert.",
                    "rating": 8.0,
                    "recommendations": ["Blade Runner 2049", "Arrival", "Interstellar"]
                }
            }
            
            # Simpan data default
            os.makedirs(os.path.dirname(self.films_data_path), exist_ok=True)
            with open(self.films_data_path, 'w', encoding='utf-8') as file:
                json.dump(default_data, file, ensure_ascii=False, indent=4)
            
            return default_data
    
    def _load_faq_data(self):
        """
        Memuat data FAQ dari JSON
        
        Returns
        -------
        dict
            Dictionary berisi pertanyaan dan jawaban umum
        """
        try:
            with open(self.faq_data_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Buat contoh data default jika file tidak ditemukan
            default_data = {
                "umum": {
                    "rekomendasi film action terbaru": "Beberapa film action terbaru yang direkomendasikan termasuk 'John Wick: Chapter 4', 'The Equalizer 3', dan 'Fast X'."
                },
                "genre_info": {
                    "Action": "Genre film dengan penekanan pada adegan kekerasan atau fisik seperti perkelahian, adegan kejar-kejaran, atau aksi ketangkasan."
                },
                "film_detail": {
                    "Dune": [
                        "film tentang planet gurun",
                        "film adaptasi novel",
                        "film denis villeneuve"
                    ]
                }
            }
            
            # Simpan data default
            os.makedirs(os.path.dirname(self.faq_data_path), exist_ok=True)
            with open(self.faq_data_path, 'w', encoding='utf-8') as file:
                json.dump(default_data, file, ensure_ascii=False, indent=4)
            
            return default_data
    
    def _prepare_film_synonyms(self):
        """
        Menyiapkan kamus sinonim untuk film
        
        Returns
        -------
        dict
            Dictionary berisi alternatif nama untuk film
        """
        synonyms = {}
        
        # Menggunakan data dari faq_data untuk informasi alternatif film
        film_details = self.faq_data.get('film_detail', {})
        
        for film_name, alt_names in film_details.items():
            # Pastikan film ada di database
            if film_name in self.films_data:
                # Tambahkan nama asli ke daftar sinonim
                if film_name not in synonyms:
                    synonyms[film_name] = set()
                
                # Tambahkan semua alternatif nama
                for alt_name in alt_names:
                    synonyms[film_name].add(alt_name)
                
                # Tambahkan judul film dari data film
                film_data = self.films_data[film_name]
                title = film_data.get('title', '')
                if title and title != film_name:
                    synonyms[film_name].add(title.lower())
        
        return synonyms
    
    def _find_film_name(self, text):
        """
        Mencari nama film dalam teks
        
        Parameters
        ----------
        text : str
            Teks yang akan dicari
            
        Returns
        -------
        tuple
            (nama_film, score_kecocokan)
        """
        # Preprocessing teks
        text_lower = text.lower()
        
        # Cek kecocokan langsung dengan nama film dalam database
        for film_name in self.films_data.keys():
            if film_name.lower() in text_lower:
                return film_name, 1.0
        
        # Cek kecocokan dengan sinonim film
        for film_name, synonyms in self.film_synonyms.items():
            for synonym in synonyms:
                if synonym in text_lower:
                    return film_name, 0.9
        
        # Jika tidak ada kecocokan langsung, cari yang paling mirip
        best_match = None
        best_score = 0
        words = text_lower.split()
        
        # Cek kecocokan dengan setiap word (untuk mendeteksi sebagian nama film)
        for film_name in self.films_data.keys():
            film_lower = film_name.lower()
            
            # Hitung skor kesamaan menggunakan SequenceMatcher
            matcher = SequenceMatcher(None, film_lower, text_lower)
            score = matcher.ratio()
            
            # Cek juga kesamaan dengan setiap kata
            for word in words:
                if len(word) > 3:  # Hanya pertimbangkan kata yang panjangnya > 3
                    word_score = SequenceMatcher(None, film_lower, word).ratio()
                    score = max(score, word_score)
            
            if score > best_score and score > 0.6:  # Threshold 0.6
                best_match = film_name
                best_score = score
        
        return best_match, best_score if best_match else (None, 0)
    
    def _find_genre_name(self, text):
        """
        Mencari nama genre dalam teks
        
        Parameters
        ----------
        text : str
            Teks yang akan dicari
            
        Returns
        -------
        tuple
            (nama_genre, score_kecocokan)
        """
        # Preprocessing teks
        text_lower = text.lower()
        
        # Kumpulkan semua genre unik dari database film
        all_genres = set()
        for film_data in self.films_data.values():
            genres = film_data.get('genre', [])
            all_genres.update([g.lower() for g in genres])
        
        # Tambahkan genre dari FAQ
        genre_info = self.faq_data.get('genre_info', {})
        all_genres.update([g.lower() for g in genre_info.keys()])
        
        # Cek kecocokan langsung dengan nama genre
        for genre in all_genres:
            if genre.lower() in text_lower:
                return genre, 1.0
        
        # Jika tidak ada kecocokan langsung, cari yang paling mirip
        best_match = None
        best_score = 0
        words = text_lower.split()
        
        # Cek kecocokan dengan setiap word
        for genre in all_genres:
            genre_lower = genre.lower()
            
            # Hitung skor kesamaan menggunakan SequenceMatcher
            matcher = SequenceMatcher(None, genre_lower, text_lower)
            score = matcher.ratio()
            
            # Cek juga kesamaan dengan setiap kata
            for word in words:
                if len(word) > 3:  # Hanya pertimbangkan kata yang panjangnya > 3
                    word_score = SequenceMatcher(None, genre_lower, word).ratio()
                    score = max(score, word_score)
            
            if score > best_score and score > 0.7:  # Threshold 0.7 (lebih ketat)
                best_match = genre
                best_score = score
        
        return best_match, best_score if best_match else (None, 0)
    
    def _get_question_type(self, text):
        """
        Menentukan tipe pertanyaan berdasarkan pola regex
        
        Parameters
        ----------
        text : str
            Teks pertanyaan
            
        Returns
        -------
        str
            Tipe pertanyaan ('rekomendasi', 'informasi', 'genre', dll)
        """
        text_lower = text.lower()
        
        for q_type, patterns in self.question_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return q_type
        
        # Default jika tidak ada pola yang cocok
        return 'umum'
    
    def _check_faq_match(self, text):
        """
        Mencari kecocokan dengan pertanyaan dari FAQ
        
        Parameters
        ----------
        text : str
            Teks pertanyaan
            
        Returns
        -------
        tuple
            (jawaban, score_kecocokan)
        """
        best_match = None
        best_score = 0
        text_lower = preprocess_text(text.lower())
        
        # Cek kecocokan dengan pertanyaan umum di FAQ
        for question, answer in self.faq_data.get('umum', {}).items():
            # Preprocessing pertanyaan
            q_processed = preprocess_text(question.lower())
            
            # Hitung skor kesamaan
            matcher = SequenceMatcher(None, q_processed, text_lower)
            score = matcher.ratio()
            
            if score > best_score and score > 0.7:  # Threshold 0.7
                best_match = answer
                best_score = score
        
        return best_match, best_score
    
    def _get_film_info(self, film_name):
        """
        Mendapatkan informasi tentang film
        
        Parameters
        ----------
        film_name : str
            Nama film
            
        Returns
        -------
        dict
            Informasi film
        """
        film_data = self.films_data.get(film_name, {})
        
        if not film_data:
            return None
        
        # Format informasi film
        info = {
            "title": film_data.get("title", film_name),
            "description": film_data.get("description", ""),
            "director": film_data.get("director", ""),
            "release_year": film_data.get("release_year", ""),
            "genre": ", ".join(film_data.get("genre", [])),
            "rating": film_data.get("rating", 0),
            "actors": ", ".join(film_data.get("actors", []))
        }
        
        return info
    
    def _get_films_by_genre(self, genre):
        """
        Mendapatkan daftar film dengan genre tertentu
        
        Parameters
        ----------
        genre : str
            Nama genre
            
        Returns
        -------
        list
            Daftar film dengan genre yang diminta
        """
        # Normalisasi genre (case insensitive)
        genre_lower = genre.lower()
        
        # Cari film dengan genre yang cocok
        matching_films = []
        
        for film_name, film_data in self.films_data.items():
            film_genres = [g.lower() for g in film_data.get('genre', [])]
            
            if genre_lower in film_genres:
                film_info = self._get_film_info(film_name)
                if film_info:
                    matching_films.append(film_info)
        
        return matching_films
    
    def _get_genre_description(self, genre):
        """
        Mendapatkan deskripsi tentang genre film
        
        Parameters
        ----------
        genre : str
            Nama genre
            
        Returns
        -------
        str
            Deskripsi genre
        """
        # Normalisasi genre (case insensitive)
        genre_info = self.faq_data.get('genre_info', {})
        
        # Cari kecocokan langsung (case insensitive)
        for g_name, g_desc in genre_info.items():
            if g_name.lower() == genre.lower():
                return g_desc
        
        # Jika tidak ada kecocokan langsung, cari yang paling mirip
        for g_name, g_desc in genre_info.items():
            if g_name.lower() in genre.lower() or genre.lower() in g_name.lower():
                return g_desc
        
        return None
    
    def _get_film_recommendations(self, film_name):
        """
        Mendapatkan daftar rekomendasi film berdasarkan film tertentu
        
        Parameters
        ----------
        film_name : str
            Nama film
            
        Returns
        -------
        list
            Daftar rekomendasi film
        """
        film_data = self.films_data.get(film_name, {})
        
        if not film_data:
            return []
        
        recommendations = film_data.get("recommendations", [])
        
        # Kumpulkan informasi lengkap untuk film yang direkomendasikan
        rec_info = []
        
        for rec_name in recommendations:
            rec_data = self._get_film_info(rec_name)
            
            if rec_data:
                rec_info.append(rec_data)
            else:
                # Jika tidak ada di database, tambahkan info minimal
                rec_info.append({"title": rec_name})
        
        return rec_info
    
    def _format_film_info_response(self, film_info):
        """
        Memformat respons informasi film
        
        Parameters
        ----------
        film_info : dict
            Informasi film
            
        Returns
        -------
        str
            Teks respons
        """
        if not film_info:
            return "Maaf, saya tidak memiliki informasi tentang film tersebut."
        
        response = f"*{film_info['title']} ({film_info['release_year']})*\n\n"
        response += f"{film_info['description']}\n\n"
        response += f"🎬 Sutradara: {film_info['director']}\n"
        response += f"🎭 Pemain: {film_info['actors']}\n"
        response += f"🏷️ Genre: {film_info['genre']}\n"
        response += f"⭐ Rating: {film_info['rating']}/10"
        
        return response
    
    def _format_genre_films_response(self, genre, films):
        """
        Memformat respons daftar film berdasarkan genre
        
        Parameters
        ----------
        genre : str
            Nama genre
        films : list
            Daftar film
            
        Returns
        -------
        str
            Teks respons
        """
        if not films:
            return f"Maaf, saya tidak menemukan film dengan genre {genre}."
        
        response = f"Berikut beberapa film dengan genre *{genre}*:\n\n"
        
        for i, film in enumerate(films[:5], 1):  # Batasi hingga 5 film
            response += f"{i}. *{film['title']}* ({film['release_year']})\n"
            response += f"   {film['description'][:100]}...\n"
        
        if len(films) > 5:
            response += f"\nDan {len(films) - 5} film lainnya."
        
        return response
    
    def _format_recommendations_response(self, film_name, recommendations):
        """
        Memformat respons rekomendasi film
        
        Parameters
        ----------
        film_name : str
            Nama film
        recommendations : list
            Daftar film yang direkomendasikan
            
        Returns
        -------
        str
            Teks respons
        """
        if not recommendations:
            return f"Maaf, saya tidak memiliki rekomendasi untuk film {film_name}."
        
        response = f"Jika Anda menyukai *{film_name}*, Anda mungkin juga akan menyukai:\n\n"
        
        for i, film in enumerate(recommendations, 1):
            response += f"{i}. *{film['title']}*"
            if film.get('release_year'):
                response += f" ({film['release_year']})"
            response += "\n"
        
        return response
    
    def get_response(self, text):
        """
        Menghasilkan respons untuk pertanyaan pengguna
        
        Parameters
        ----------
        text : str
            Teks pertanyaan dari pengguna
            
        Returns
        -------
        dict
            Dictionary berisi respons chatbot
        """
        # Cek terlebih dahulu apakah ada kecocokan dengan FAQ
        faq_answer, faq_score = self._check_faq_match(text)
        if faq_answer and faq_score > 0.75:
            return {
                "type": "text",
                "content": faq_answer
            }
        
        # Tentukan tipe pertanyaan
        question_type = self._get_question_type(text)
        
        if question_type == 'informasi':
            # Cari nama film dalam teks
            film_name, score = self._find_film_name(text)
            
            if film_name and score > 0.7:
                film_info = self._get_film_info(film_name)
                return {
                    "type": "film_info",
                    "content": self._format_film_info_response(film_info),
                    "film": film_info
                }
        
        elif question_type == 'rekomendasi':
            # Cek apakah ada nama film spesifik
            film_name, score = self._find_film_name(text)
            
            if film_name and score > 0.7:
                recommendations = self._get_film_recommendations(film_name)
                return {
                    "type": "recommendations",
                    "content": self._format_recommendations_response(film_name, recommendations),
                    "recommendations": recommendations,
                    "based_on": film_name
                }
            else:
                # Jika tidak ada film spesifik, cek apakah ada genre
                genre_name, genre_score = self._find_genre_name(text)
                
                if genre_name and genre_score > 0.7:
                    genre_films = self._get_films_by_genre(genre_name)
                    return {
                        "type": "genre_films",
                        "content": self._format_genre_films_response(genre_name, genre_films),
                        "genre": genre_name,
                        "films": genre_films
                    }
                
                # Jika tidak ada genre spesifik juga, berikan rekomendasi umum
                return {
                    "type": "text",
                    "content": "Untuk mendapatkan rekomendasi film yang lebih akurat, silakan sebutkan jenis film (genre) atau film yang Anda sukai. Misalnya: 'Rekomendasi film action terbaru' atau 'Film seperti Inception'."
                }
        
        elif question_type == 'genre':
            # Cari nama genre dalam teks
            genre_name, score = self._find_genre_name(text)
            
            if genre_name and score > 0.7:
                # Cek apakah pengguna bertanya tentang deskripsi genre
                if any(word in text.lower() for word in ['apa', 'artikan', 'jelaskan', 'maksud']):
                    genre_description = self._get_genre_description(genre_name)
                    
                    if genre_description:
                        return {
                            "type": "text",
                            "content": f"*{genre_name}*: {genre_description}"
                        }
                
                # Default: tampilkan film-film dengan genre ini
                genre_films = self._get_films_by_genre(genre_name)
                return {
                    "type": "genre_films",
                    "content": self._format_genre_films_response(genre_name, genre_films),
                    "genre": genre_name,
                    "films": genre_films
                }
        
        # Default: mencoba mencari kecocokan dengan film atau genre
        film_name, film_score = self._find_film_name(text)
        genre_name, genre_score = self._find_genre_name(text)
        
        # Pilih yang paling tinggi skor kecocokannya
        if film_score > genre_score and film_score > 0.7:
            film_info = self._get_film_info(film_name)
            return {
                "type": "film_info",
                "content": self._format_film_info_response(film_info),
                "film": film_info
            }
        elif genre_score > 0.7:
            genre_films = self._get_films_by_genre(genre_name)
            return {
                "type": "genre_films",
                "content": self._format_genre_films_response(genre_name, genre_films),
                "genre": genre_name,
                "films": genre_films
            }
        
        # Jika tidak ada kecocokan yang spesifik
        return {
            "type": "text",
            "content": "Maaf, saya tidak memahami pertanyaan Anda. Anda dapat bertanya tentang film tertentu, genre film, atau rekomendasi film. Contoh: 'Apa itu film Dune?', 'Film genre action terbaru', atau 'Rekomendasi film seperti Inception'."
        }
