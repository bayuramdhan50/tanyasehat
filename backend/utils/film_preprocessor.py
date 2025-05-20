"""
Module untuk preprocessing teks dalam bahasa Indonesia
"""
import re
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import unicodedata

# Download NLTK data yang diperlukan
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Setup stemmer bahasa Indonesia dari Sastrawi
stemmer_factory = StemmerFactory()
stemmer = stemmer_factory.create_stemmer()

# Normalisasi singkatan dan slang words bahasa Indonesia
word_normalization = {
    'gak': 'tidak', 'ga': 'tidak', 'ngga': 'tidak', 'nggak': 'tidak', 'g': 'tidak',
    'tdk': 'tidak', 'enggak': 'tidak', 'gk': 'tidak', 'engga': 'tidak',
    'gpp': 'tidak apa-apa', 'gapapa': 'tidak apa-apa', 'gppa': 'tidak apa-apa',
    'bgt': 'banget', 'baget': 'banget', 'bgd': 'banget', 
    'yg': 'yang', 'dgn': 'dengan', 'utk': 'untuk', 'pd': 'pada',
    'dr': 'dari', 'dlm': 'dalam', 'jg': 'juga', 'trs': 'terus',
    'bg': 'bagi', 'krn': 'karena', 'karna': 'karena', 'krna': 'karena',
    'dll': 'dan lain lain', 'dsb': 'dan sebagainya', 'dkk': 'dan kawan kawan',
    'tuh': 'itu', 'itu tuh': 'itu', 'nih': 'ini', 'gini': 'begini',
    'gitu': 'begitu', 'gtw': 'tidak tahu', 'gatau': 'tidak tahu',
    'udh': 'sudah', 'dah': 'sudah', 'udah': 'sudah', 'sdh': 'sudah',
    'blm': 'belum', 'blum': 'belum', 'belom': 'belum', 'bru': 'baru',
    'slalu': 'selalu', 'pny': 'punya', 'yuk': 'ayo', 'tp': 'tapi',
    'tpi': 'tapi', 'tetapi': 'tapi', 'spy': 'supaya', 'spya': 'supaya',
    'kmrn': 'kemarin', 'kmrin': 'kemarin', 'kemarinnya': 'kemarin',
    'bs': 'bisa', 'bsa': 'bisa', 'klo': 'kalau', 'kl': 'kalau',
    'tdk': 'tidak'
}

# Kata-kata khusus film
film_keywords = {
    'action': 'action', 'aksi': 'action', 'laga': 'action',
    'adventure': 'adventure', 'petualangan': 'adventure',
    'animation': 'animation', 'animasi': 'animation', 'kartun': 'animation',
    'comedy': 'comedy', 'komedi': 'comedy', 'lucu': 'comedy',
    'crime': 'crime', 'kriminal': 'crime', 'kejahatan': 'crime',
    'documentary': 'documentary', 'dokumenter': 'documentary',
    'drama': 'drama',
    'family': 'family', 'keluarga': 'family',
    'fantasy': 'fantasy', 'fantasi': 'fantasy',
    'horror': 'horror', 'horor': 'horror', 'seram': 'horror', 'menakutkan': 'horror',
    'musical': 'musical', 'musik': 'musical',
    'mystery': 'mystery', 'misteri': 'mystery', 'misterius': 'mystery',
    'romance': 'romance', 'romantis': 'romance', 'cinta': 'romance',
    'sci-fi': 'sci-fi', 'science fiction': 'sci-fi', 'fiksi ilmiah': 'sci-fi',
    'thriller': 'thriller', 'menegangkan': 'thriller',
    'war': 'war', 'perang': 'war',
    'western': 'western', 'koboi': 'western',
    'bioskop': 'bioskop', 'movie': 'film', 'movies': 'film',
    'sutradara': 'sutradara', 'director': 'sutradara',
    'aktor': 'aktor', 'actor': 'aktor', 'aktris': 'aktris', 'actress': 'aktris',
    'pemeran': 'pemeran', 'pemain': 'pemeran',
    'alur': 'alur', 'plot': 'alur', 'cerita': 'cerita',
    'sinopsis': 'sinopsis', 'synopsis': 'sinopsis',
    'rating': 'rating', 'nilai': 'rating', 'skor': 'rating',
    'review': 'review', 'ulasan': 'review', 'kritik': 'review',
    'populer': 'populer', 'popular': 'populer', 'terkenal': 'populer',
    'terbaru': 'terbaru', 'baru': 'terbaru', 'terkini': 'terbaru',
    'klasik': 'klasik', 'lama': 'klasik', 'jadul': 'klasik'
}

def normalize_text(text):
    """
    Normalisasi teks: mengganti singkatan dan slang dengan bentuk formal
    
    Parameters
    ----------
    text : str
        Teks yang akan dinormalisasi
        
    Returns
    -------
    str
        Teks yang telah dinormalisasi
    """
    text = text.lower()
    
    # Normalisasi unicode
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    
    # Ganti karakter tidak standar dan multiple spaces
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    
    # Normalisasi kata-kata
    words = text.split()
    normalized_words = []
    
    for word in words:
        # Normalisasi kata umum
        if word in word_normalization:
            normalized_words.append(word_normalization[word])
        # Normalisasi kata film
        elif word in film_keywords:
            normalized_words.append(film_keywords[word])
        else:
            normalized_words.append(word)
    
    return ' '.join(normalized_words)

def remove_stopwords(tokens, additional_stopwords=None):
    """
    Menghapus stopwords dari token
    
    Parameters
    ----------
    tokens : list
        List dari token
    additional_stopwords : list, optional
        List tambahan stopwords, by default None
        
    Returns
    -------
    list
        List dari token tanpa stopwords
    """
    # Gabungkan stopwords bawaan dengan additional stopwords
    stop_words = set(stopwords.words('indonesian'))
    if additional_stopwords:
        stop_words.update(additional_stopwords)
    
    # Hapus stopwords
    return [word for word in tokens if word not in stop_words]

def extract_film_keywords(text):
    """
    Ekstraksi kata kunci terkait film dari teks
    
    Parameters
    ----------
    text : str
        Teks yang akan diekstrak keyword-nya
        
    Returns
    -------
    list
        List kata kunci terkait film
    """
    words = text.lower().split()
    keywords = []
    
    for word in words:
        if word in film_keywords.values():
            keywords.append(word)
    
    return keywords

def preprocess_text(text, remove_stop=True, do_stemming=True):
    """
    Preprocessing teks lengkap: normalisasi, tokenisasi, hapus stopword, stemming
    
    Parameters
    ----------
    text : str
        Teks yang akan diproses
    remove_stop : bool, optional
        Flag untuk menghapus stopwords, by default True
    do_stemming : bool, optional
        Flag untuk melakukan stemming, by default True
        
    Returns
    -------
    str
        Teks yang telah diproses
    """
    if not text:
        return ""
    
    # Normalisasi teks
    text = normalize_text(text)
    
    # Tokenisasi
    tokens = word_tokenize(text)
    
    # Hapus stopwords jika diminta
    if remove_stop:
        # Tambahkan stopwords khusus film yang tidak boleh dihapus
        film_stopwords_to_keep = ['film', 'movie', 'action', 'comedy', 'drama', 'horror', 'romance', 'thriller']
        
        # Definisikan stopwords custom yang tidak akan dihapus
        custom_stopwords = [word for word in stopwords.words('indonesian') if word not in film_stopwords_to_keep]
        
        tokens = remove_stopwords(tokens, additional_stopwords=custom_stopwords)
    
    # Stemming jika diminta
    if do_stemming:
        tokens = [stemmer.stem(token) for token in tokens]
    
    # Gabungkan kembali menjadi teks
    return " ".join(tokens)

def tokenize_only(text):
    """
    Hanya lakukan tokenisasi tanpa preprocessing lain
    
    Parameters
    ----------
    text : str
        Teks yang akan ditokenisasi
        
    Returns
    -------
    list
        List token hasil tokenisasi
    """
    if not text:
        return []
    
    # Normalisasi teks
    text = normalize_text(text)
    
    # Tokenisasi
    tokens = word_tokenize(text)
    
    return tokens

def extract_film_patterns(text):
    """
    Ekstrak pola-pola referensi film dari teks input
    
    Parameters
    ----------
    text : str
        Teks input pengguna
        
    Returns
    -------
    dict
        Pola-pola film yang diekstrak
    """
    patterns = {}
    
    # Pattern untuk genre
    genre_pattern = r'(film|movie)\s+(genre|bergenre|dengan genre|tipe|kategori)\s+([a-zA-Z\s]+)'
    genre_matches = re.findall(genre_pattern, text.lower())
    if genre_matches:
        patterns['genre'] = genre_matches[0][2].strip()
    
    # Pattern untuk sutradara
    director_pattern = r'(film|movie)\s+(dari|oleh|garapan|karya|sutradara)\s+([a-zA-Z\s]+)'
    director_matches = re.findall(director_pattern, text.lower())
    if director_matches:
        patterns['director'] = director_matches[0][2].strip()
    
    # Pattern untuk aktor
    actor_pattern = r'(film|movie)\s+(dengan|dibintangi|diperankan oleh|pemain)\s+([a-zA-Z\s]+)'
    actor_matches = re.findall(actor_pattern, text.lower())
    if actor_matches:
        patterns['actor'] = actor_matches[0][2].strip()
    
    # Pattern untuk tahun
    year_pattern = r'(film|movie)\s+(dari|tahun|rilis|dirilis|keluaran)\s+(\d{4})'
    year_matches = re.findall(year_pattern, text.lower())
    if year_matches:
        patterns['year'] = year_matches[0][2].strip()
    
    # Pattern untuk rating
    rating_pattern = r'(film|movie)\s+(dengan|rating|nilai|skor)\s+(tinggi|bagus|terbaik|atas)'
    rating_matches = re.findall(rating_pattern, text.lower())
    if rating_matches:
        patterns['rating'] = 'high'
    
    return patterns
