"""
Output translator untuk menghasilkan rekomendasi film berdasarkan hasil prediksi genre
"""
import os
import json
import random
from difflib import get_close_matches

class FilmTranslator:
    """
    Kelas untuk menghasilkan rekomendasi film berdasarkan hasil prediksi genre.
    """
    
    def __init__(self):
        """
        Inisialisasi translator dengan data film dan rekomendasi
        """
        self.films_data_path = os.path.join('data', 'films.json')
        
        # Muat data film jika ada
        self.films_data = self._load_films_data()
        
        # Membuat indeks film berdasarkan genre untuk pencarian yang lebih cepat
        self.genre_index = self._build_genre_index()
    
    def _load_films_data(self):
        """
        Memuat data film dari JSON.
        Jika file tidak ada, akan dibuat data contoh.
        
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
    
    def _build_genre_index(self):
        """
        Membuat indeks film berdasarkan genre untuk pencarian yang lebih cepat
        
        Returns
        -------
        dict
            Dictionary dengan key berupa nama genre dan value berupa list nama film
        """
        genre_index = {}
        
        for film_name, film_data in self.films_data.items():
            genres = film_data.get("genre", [])
            
            for genre in genres:
                if genre not in genre_index:
                    genre_index[genre] = []
                
                genre_index[genre].append(film_name)
        
        return genre_index
    
    def _normalize_genre(self, genre):
        """
        Menormalkan nama genre agar sesuai dengan yang ada di database
        
        Parameters
        ----------
        genre : str
            Nama genre yang akan dinormalkan
            
        Returns
        -------
        str
            Nama genre yang sudah dinormalkan
        """
        # Konversi ke title case untuk standarisasi
        normalized = genre.title()
        
        # Daftar genre yang tersedia dalam database
        available_genres = list(self.genre_index.keys())
        
        # Cari genre yang paling mirip
        matches = get_close_matches(normalized, available_genres, n=1, cutoff=0.7)
        
        if matches:
            return matches[0]
        else:
            return normalized  # Kembalikan yang asli jika tidak ada yang cocok
    
    def get_recommendations(self, predicted_genres, top_n=5):
        """
        Menghasilkan rekomendasi film berdasarkan genre yang diprediksi
        
        Parameters
        ----------
        predicted_genres : list
            List dari dictionary berisi genre dan confidence score
        top_n : int, optional
            Jumlah rekomendasi film yang dihasilkan, by default 5
            
        Returns
        -------
        list
            List dari dictionary berisi informasi film yang direkomendasikan
        """
        # List untuk menyimpan film yang direkomendasikan dan skornya
        film_scores = {}
        
        # Iterasi melalui genre yang diprediksi
        for genre_data in predicted_genres:
            genre = genre_data["genre"]
            confidence = genre_data["confidence"]
            
            # Normalisasi nama genre
            normalized_genre = self._normalize_genre(genre)
            
            # Ambil film dengan genre tersebut
            films_with_genre = self.genre_index.get(normalized_genre, [])
            
            # Hitung skor untuk setiap film berdasarkan confidence score
            for film_name in films_with_genre:
                if film_name not in film_scores:
                    film_scores[film_name] = 0
                
                # Tambahkan confidence sebagai skor
                film_scores[film_name] += confidence
        
        # Urutkan film berdasarkan skor tertinggi
        sorted_films = sorted(film_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Ambil top_n film
        top_films = [film_name for film_name, _ in sorted_films[:top_n]]
        
        # Jika tidak ada film yang sesuai, ambil film random
        if not top_films and self.films_data:
            top_films = random.sample(list(self.films_data.keys()), min(top_n, len(self.films_data)))
        
        # Susun informasi lengkap untuk film yang direkomendasikan
        recommendations = []
        for film_name in top_films:
            if film_name in self.films_data:
                film_info = self.films_data[film_name].copy()
                film_info["name"] = film_name  # Tambahkan nama film ke informasi
                film_info["score"] = film_scores.get(film_name, 0)  # Tambahkan skor
                recommendations.append(film_info)
        
        return recommendations
    
    def format_response(self, recommendations, input_text=""):
        """
        Memformat respons untuk ditampilkan ke pengguna
        
        Parameters
        ----------
        recommendations : list
            List dari dictionary berisi informasi film yang direkomendasikan
        input_text : str, optional
            Teks input dari pengguna, by default ""
            
        Returns
        -------
        dict
            Dictionary berisi respons yang diformat
        """
        if not recommendations:
            return {
                "message": "Maaf, kami tidak dapat menemukan film yang sesuai dengan preferensi Anda.",
                "recommendations": []
            }
        
        # Buat pesan berdasarkan input pengguna
        if input_text:
            message = f"Berdasarkan preferensi Anda \"{input_text}\", berikut adalah rekomendasi film yang mungkin Anda sukai:"
        else:
            message = "Berikut adalah rekomendasi film yang mungkin Anda sukai:"
        
        # Format output untuk setiap film
        formatted_recs = []
        for film in recommendations:
            formatted_film = {
                "title": film.get("title", ""),
                "description": film.get("description", ""),
                "genre": ", ".join(film.get("genre", [])),
                "director": film.get("director", ""),
                "release_year": film.get("release_year", ""),
                "rating": film.get("rating", 0),
                "confidence": round(film.get("score", 0) * 100, 1)  # Konversi ke persentase
            }
            formatted_recs.append(formatted_film)
        
        return {
            "message": message,
            "recommendations": formatted_recs
        }
    
    def get_film_details(self, film_name):
        """
        Mengambil detail film berdasarkan nama
        
        Parameters
        ----------
        film_name : str
            Nama film
            
        Returns
        -------
        dict
            Dictionary berisi informasi film
        """
        # Cek apakah film ada dalam database
        if film_name in self.films_data:
            film_info = self.films_data[film_name].copy()
            film_info["name"] = film_name  # Tambahkan nama film ke informasi
            return film_info
        
        # Jika tidak ada yang cocok persis, cari yang paling mirip
        matches = get_close_matches(film_name, list(self.films_data.keys()), n=1, cutoff=0.7)
        if matches:
            matched_name = matches[0]
            film_info = self.films_data[matched_name].copy()
            film_info["name"] = matched_name
            film_info["message"] = f"Film \"{film_name}\" tidak ditemukan. Berikut adalah film yang paling mirip:"
            return film_info
        
        return {"message": f"Maaf, kami tidak dapat menemukan informasi tentang film \"{film_name}\"."}
    
    def get_films_by_genre(self, genre_name, limit=5):
        """
        Mengambil daftar film berdasarkan genre
        
        Parameters
        ----------
        genre_name : str
            Nama genre
        limit : int, optional
            Jumlah maksimum film yang dikembalikan, by default 5
            
        Returns
        -------
        list
            List dari dictionary berisi informasi film
        """
        # Normalisasi nama genre
        normalized_genre = self._normalize_genre(genre_name)
        
        # Ambil film dengan genre tersebut
        films_with_genre = self.genre_index.get(normalized_genre, [])
        
        if not films_with_genre:
            # Jika tidak ada yang cocok persis, cari genre yang paling mirip
            all_genres = list(self.genre_index.keys())
            matches = get_close_matches(normalized_genre, all_genres, n=1, cutoff=0.6)
            
            if matches:
                normalized_genre = matches[0]
                films_with_genre = self.genre_index.get(normalized_genre, [])
        
        # Batasi jumlah film
        selected_films = films_with_genre[:limit]
        
        # Susun informasi lengkap untuk film yang dipilih
        film_info_list = []
        for film_name in selected_films:
            if film_name in self.films_data:
                film_info = self.films_data[film_name].copy()
                film_info["name"] = film_name  # Tambahkan nama film ke informasi
                film_info_list.append(film_info)
        
        return {
            "genre": normalized_genre,
            "films": film_info_list,
            "count": len(film_info_list)
        }
