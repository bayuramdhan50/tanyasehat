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
    'pny': 'punya', 'udh': 'sudah', 'dah': 'sudah', 'sdh': 'sudah', 'udah': 'sudah',
    'blm': 'belum', 'belom': 'belum', 'blum': 'belum',
    'kyk': 'seperti', 'kyak': 'seperti', 'ky': 'seperti', 'kek': 'seperti',
    'bgt': 'banget', 'bangetss': 'banget', 'bgtt': 'banget',
    'jg': 'juga', 'dg': 'dengan', 'dgn': 'dengan', 'dlm': 'dalam',
    'ank': 'anak', 'org': 'orang', 'krn': 'karena', 'karna': 'karena',
    'hrs': 'harus', 'smua': 'semua', 'smuanya': 'semuanya',
    'spy': 'supaya', 'stlh': 'setelah', 'skrg': 'sekarang', 'skrang': 'sekarang',
    'kalo': 'kalau', 'klo': 'kalau', 'kl': 'kalau',
    'ato': 'atau', 'atw': 'atau', 'tp': 'tapi', 'tpi': 'tapi',
    'sm': 'sama', 'yg': 'yang', 'dr': 'dari', 'utk': 'untuk',
    'pd': 'pada', 'trs': 'terus', 'truss': 'terus', 'trus': 'terus',
    'byk': 'banyak', 'dll': 'dan lain-lain', 'dsb': 'dan sebagainya',
    'sbg': 'sebagai', 'sblm': 'sebelum', 'stlh': 'setelah',
    'sy': 'saya', 'sya': 'saya', 'aq': 'saya', 'aku': 'saya', 'gw': 'saya', 'gua': 'saya', 'gue': 'saya',
    'km': 'kamu', 'kmu': 'kamu', 'lu': 'kamu', 'loe': 'kamu', 'elo': 'kamu',
    'emg': 'memang', 'emang': 'memang', 'btw': 'ngomong-ngomong',
    'lbh': 'lebih', 'jd': 'jadi', 'jdnya': 'jadinya',
    'bln': 'bulan', 'hr': 'hari', 'mgg': 'minggu', 'thun': 'tahun', 'th': 'tahun',
    'biar': 'supaya', 'bngt': 'banget',
    'bru': 'baru', 'msh': 'masih', 'dpat': 'dapat',
    'kmrn': 'kemarin', 'sbnrnya': 'sebenarnya', 'sbntar': 'sebentar',
    'brp': 'berapa', 'bs': 'bisa', 'bsa': 'bisa',
}

# Load stopwords bahasa Indonesia
try:
    stop_words = set(stopwords.words('indonesian'))
except:
    # Fallback jika NLTK tidak memiliki stopwords bahasa Indonesia
    stop_words = set([
        'ada', 'adalah', 'adanya', 'adapun', 'agak', 'agaknya', 'agar', 'akan', 'akankah', 
        'akhir', 'akhiri', 'akhirnya', 'aku', 'akulah', 'amat', 'amatlah', 'anda', 'andalah', 
        'antar', 'antara', 'antaranya', 'apa', 'apaan', 'apabila', 'apakah', 'apalagi', 'apatah', 
        'artinya', 'asal', 'asalkan', 'atas', 'atau', 'ataukah', 'ataupun', 'awal', 'awalnya',
        'bagai', 'bagaikan', 'bagaimana', 'bagaimanakah', 'bagaimanapun', 'bagi', 'bagian', 
        'bahkan', 'bahwa', 'bahwasanya', 'baik', 'bakal', 'bakalan', 'balik', 'banyak', 'bapak', 
        'baru', 'bawah', 'beberapa', 'begini', 'beginian', 'beginikah', 'beginilah', 'begitu', 
        'begitukah', 'begitulah', 'begitupun', 'bekerja', 'belakang', 'belakangan', 'belum', 
        'belumlah', 'benar', 'benarkah', 'benarlah', 'berada', 'berakhir', 'berakhirlah', 
        'berakhirnya', 'berapa', 'berapakah', 'berapalah', 'berapapun', 'berarti', 'berawal', 
        'berbagai', 'berdatangan', 'beri', 'berikan', 'berikut', 'berikutnya', 'berjumlah', 
        'berkali-kali', 'berkata', 'berkehendak', 'berkeinginan', 'berkenaan', 'berlainan', 
        'berlalu', 'berlangsung', 'berlebihan', 'bermacam', 'bermacam-macam', 'bermaksud', 
        'bermula', 'bersama', 'bersama-sama', 'bersiap', 'bersiap-siap', 'bertanya', 
        'bertanya-tanya', 'berturut', 'berturut-turut', 'bertutur', 'berujar', 'berupa', 
        'besar', 'betul', 'betulkah', 'biasa', 'biasanya', 'bila', 'bilakah', 'bisa', 
        'bisakah', 'boleh', 'bolehkah', 'bolehlah', 'buat', 'bukan', 'bukankah', 'bukanlah', 
        'bukannya', 'bulan', 'bung', 'cara', 'caranya', 'cukup', 'cukupkah', 'cukuplah', 
        'cuma', 'dahulu', 'dalam', 'dan', 'dapat', 'dari', 'daripada', 'datang', 'dekat', 
        'demi', 'demikian', 'demikianlah', 'dengan', 'depan', 'di', 'dia', 'diakhiri', 
        'diakhirinya', 'dialah', 'diantara', 'diantaranya', 'diberi', 'diberikan', 'diberikannya', 
        'dibuat', 'dibuatnya', 'didapat', 'didatangkan', 'digunakan', 'diibaratkan', 'diibaratkannya', 
        'diingat', 'diingatkan', 'diinginkan', 'dijawab', 'dijelaskan', 'dijelaskannya', 'dikarenakan', 
        'dikatakan', 'dikatakannya', 'dikerjakan', 'diketahui', 'diketahuinya', 'dikira', 'dilakukan', 
        'dilalui', 'dilihat', 'dimaksud', 'dimaksudkan', 'dimaksudkannya', 'dimaksudnya', 'diminta', 
        'dimintai', 'dimisalkan', 'dimulai', 'dimulailah', 'dimulainya', 'dimungkinkan', 'dini', 
        'dipastikan', 'diperbuat', 'diperbuatnya', 'dipergunakan', 'diperkirakan', 'diperlihatkan', 
        'diperlukan', 'diperlukannya', 'dipersoalkan', 'dipertanyakan', 'dipunyai', 'diri', 
        'dirinya', 'disampaikan', 'disebut', 'disebutkan', 'disebutkannya', 'disini', 'disinilah', 
        'ditambahkan', 'ditandaskan', 'ditanya', 'ditanyai', 'ditanyakan', 'ditegaskan', 'ditujukan', 
        'ditunjuk', 'ditunjuki', 'ditunjukkan', 'ditunjukkannya', 'ditunjuknya', 'dituturkan', 
        'dituturkannya', 'diucapkan', 'diucapkannya', 'diungkapkan', 'dong', 'dua', 'dulu', 
        'empat', 'enggak', 'enggaknya', 'entah', 'entahlah', 'guna', 'gunakan', 'hal', 'hampir', 
        'hanya', 'hanyalah', 'hari', 'harus', 'haruslah', 'harusnya', 'hendak', 'hendaklah', 
        'hendaknya', 'hingga', 'ia', 'ialah', 'ibarat', 'ibaratkan', 'ibaratnya', 'ibu', 'ikut', 
        'ingat', 'ingat-ingat', 'ingin', 'inginkah', 'inginkan', 'ini', 'inikah', 'inilah', 
        'itu', 'itukah', 'itulah', 'jadi', 'jadilah', 'jadinya', 'jangan', 'jangankan', 'janganlah', 
        'jauh', 'jawab', 'jawaban', 'jawabnya', 'jelas', 'jelaskan', 'jelaslah', 'jelasnya', 
        'jika', 'jikalau', 'juga', 'jumlah', 'jumlahnya', 'justru', 'kala', 'kalau', 'kalaulah', 
        'kalaupun', 'kalian', 'kami', 'kamilah', 'kamu', 'kamulah', 'kan', 'kapan', 'kapankah', 
        'kapanpun', 'karena', 'karenanya', 'kasus', 'kata', 'katakan', 'katakanlah', 'katanya', 
        'ke', 'keadaan', 'kebetulan', 'kecil', 'kedua', 'keduanya', 'keinginan', 'kelamaan', 
        'kelihatan', 'kelihatannya', 'kelima', 'keluar', 'kembali', 'kemudian', 'kemungkinan', 
        'kemungkinannya', 'kenapa', 'kepada', 'kepadanya', 'kesamaan', 'keseluruhan', 'keseluruhannya', 
        'keterlaluan', 'ketika', 'khususnya', 'kini', 'kinilah', 'kira', 'kira-kira', 'kiranya', 
        'kita', 'kitalah', 'kok', 'kurang', 'lagi', 'lagian', 'lah', 'lain', 'lainnya', 'lalu', 
        'lama', 'lamanya', 'lanjut', 'lanjutnya', 'lebih', 'lewat', 'lima', 'luar', 'macam', 
        'maka', 'makanya', 'makin', 'malah', 'malahan', 'mampu', 'mampukah', 'mana', 'manakala', 
        'manalagi', 'masa', 'masalah', 'masalahnya', 'masih', 'masihkah', 'masing', 'masing-masing', 
        'mau', 'maupun', 'melainkan', 'melakukan', 'melalui', 'melihat', 'melihatnya', 'memang', 
        'memastikan', 'memberi', 'memberikan', 'membuat', 'memerlukan', 'memihak', 'meminta', 
        'memintakan', 'memisalkan', 'memperbuat', 'mempergunakan', 'memperkirakan', 'memperlihatkan', 
        'mempersiapkan', 'mempersoalkan', 'mempertanyakan', 'mempunyai', 'memulai', 'memungkinkan', 
        'menaiki', 'menambahkan', 'menandaskan', 'menanti', 'menanti-nanti', 'menantikan', 
        'menanya', 'menanyai', 'menanyakan', 'mendapat', 'mendapatkan', 'mendatang', 'mendatangi', 
        'mendatangkan', 'menegaskan', 'mengakhiri', 'mengapa', 'mengatakan', 'mengatakannya', 
        'mengenai', 'mengerjakan', 'mengetahui', 'menggunakan', 'menghendaki', 'mengibaratkan', 
        'mengibaratkannya', 'mengingat', 'mengingatkan', 'menginginkan', 'mengira', 'mengucapkan', 
        'mengucapkannya', 'mengungkapkan', 'menjadi', 'menjawab', 'menjelaskan', 'menuju', 
        'menunjuk', 'menunjuki', 'menunjukkan', 'menunjuknya', 'menurut', 'menuturkan', 
        'menyampaikan', 'menyangkut', 'menyatakan', 'menyebutkan', 'menyeluruh', 'menyiapkan', 
        'merasa', 'mereka', 'merekalah', 'merupakan', 'meski', 'meskipun', 'meyakini', 'meyakinkan', 
        'minta', 'mirip', 'misal', 'misalkan', 'misalnya', 'mula', 'mulai', 'mulailah', 'mulanya', 
        'mungkin', 'mungkinkah', 'nah', 'naik', 'namun', 'nanti', 'nantinya', 'nyaris', 'nyatanya', 
        'oleh', 'olehnya', 'pada', 'padahal', 'padanya', 'pak', 'paling', 'panjang', 'pantas', 
        'para', 'pasti', 'pastilah', 'penting', 'pentingnya', 'per', 'percuma', 'perlu', 'perlukah', 
        'perlunya', 'pernah', 'persoalan', 'pertama', 'pertama-tama', 'pertanyaan', 'pertanyakan', 
        'pihak', 'pihaknya', 'pukul', 'pula', 'pun', 'punya', 'rasa', 'rasanya', 'rata', 'rupanya', 
        'saat', 'saatnya', 'saja', 'sajalah', 'saling', 'sama', 'sama-sama', 'sambil', 'sampai', 
        'sampai-sampai', 'sampaikan', 'sana', 'sangat', 'sangatlah', 'satu', 'saya', 'sayalah', 
        'se', 'sebab', 'sebabnya', 'sebagai', 'sebagaimana', 'sebagainya', 'sebagian', 'sebaik', 
        'sebaik-baiknya', 'sebaiknya', 'sebaliknya', 'sebanyak', 'sebegini', 'sebegitu', 'sebelum', 
        'sebelumnya', 'sebenarnya', 'seberapa', 'sebesar', 'sebetulnya', 'sebisanya', 'sebuah', 
        'sebut', 'sebutlah', 'sebutnya', 'secara', 'secukupnya', 'sedang', 'sedangkan', 'sedemikian', 
        'sedikit', 'sedikitnya', 'seenaknya', 'segala', 'segalanya', 'segera', 'seharusnya', 
        'sehingga', 'seingat', 'sejak', 'sejauh', 'sejenak', 'sejumlah', 'sekadar', 'sekadarnya', 
        'sekali', 'sekali-kali', 'sekalian', 'sekaligus', 'sekalipun', 'sekarang', 'sekarang', 
        'sekecil', 'seketika', 'sekiranya', 'sekitar', 'sekitarnya', 'sekurang-kurangnya', 
        'sekurangnya', 'sela', 'selain', 'selaku', 'selalu', 'selama', 'selama-lamanya', 
        'selamanya', 'selanjutnya', 'seluruh', 'seluruhnya', 'semacam', 'semakin', 'semampu', 
        'semampunya', 'semasa', 'semasih', 'semata', 'semata-mata', 'semaunya', 'sementara', 
        'semisal', 'semisalnya', 'sempat', 'semua', 'semuanya', 'semula', 'sendiri', 'sendirian', 
        'sendirinya', 'seolah', 'seolah-olah', 'seorang', 'sepanjang', 'sepantasnya', 'sepantasnyalah', 
        'seperlunya', 'seperti', 'sepertinya', 'sepihak', 'sering', 'seringnya', 'serta', 
        'serupa', 'sesaat', 'sesama', 'sesampai', 'sesegera', 'sesekali', 'seseorang', 
        'sesuatu', 'sesuatunya', 'sesudah', 'sesudahnya', 'setelah', 'setempat', 'setengah', 
        'seterusnya', 'setiap', 'setiba', 'setibanya', 'setidak-tidaknya', 'setidaknya', 
        'setinggi', 'seusai', 'sewaktu', 'siap', 'siapa', 'siapakah', 'siapapun', 'sini', 
        'sinilah', 'soal', 'soalnya', 'suatu', 'sudah', 'sudahkah', 'sudahlah', 'supaya', 
        'tadi', 'tadinya', 'tahu', 'tahun', 'tak', 'tambah', 'tambahnya', 'tampak', 'tampaknya', 
        'tandas', 'tandasnya', 'tanpa', 'tanya', 'tanyakan', 'tanyanya', 'tapi', 'tegas', 
        'tegasnya', 'telah', 'tempat', 'tengah', 'tentang', 'tentu', 'tentulah', 'tentunya', 
        'tepat', 'terakhir', 'terasa', 'terbanyak', 'terdahulu', 'terdapat', 'terdiri', 
        'terhadap', 'terhadapnya', 'teringat', 'teringat-ingat', 'terjadi', 'terjadilah', 
        'terjadinya', 'terkira', 'terlalu', 'terlebih', 'terlihat', 'termasuk', 'ternyata', 
        'tersampaikan', 'tersebut', 'tersebutlah', 'tertentu', 'tertuju', 'terus', 'terutama', 
        'tetap', 'tetapi', 'tiap', 'tiba', 'tiba-tiba', 'tidak', 'tidakkah', 'tidaklah', 
        'tiga', 'tinggi', 'toh', 'tunjuk', 'turut', 'tutur', 'tuturnya', 'ucap', 'ucapnya', 
        'ujar', 'ujarnya', 'umum', 'umumnya', 'ungkap', 'ungkapnya', 'untuk', 'usah', 
        'usai', 'waduh', 'wah', 'wahai', 'waktu', 'waktunya', 'walau', 'walaupun', 'wong', 'yaitu', 
        'yakin', 'yakni', 'yang', 'sih', 'nih'
    ])

# Tambahkan stopwords khusus gejala penyakit atau medis yang tidak berguna
medical_stopwords = set([
    'saya', 'sakit', 'mengalami', 'merasa', 'rasanya', 'seperti', 'kayak', 'dok', 'dokter',
    'bagaimana', 'kenapa', 'mengapa', 'gimana', 'apa', 'apakah', 'tolong', 'bantu', 'minta',
    'bantuan', 'saran', 'kira', 'kira-kira', 'mohon', 'ya', 'pak', 'bu', 'bapak', 'ibu',
    'mas', 'mbak', 'telah', 'sudah', 'sedang', 'masih', 'akan', 'sekarang', 'tadi', 'kemarin',
    'lusa', 'lama', 'terus', 'terus-menerus', 'kira-kira', 'sangat'
])

# Kata-kata penting terkait gejala yang TIDAK boleh dihapus (negasi)
important_medical_terms = set([
    'nyeri', 'sakit', 'bengkak', 'panas', 'dingin', 'lemas', 'lelah', 'lemah', 'batuk', 
    'pilek', 'bersin', 'demam', 'pusing', 'mual', 'muntah', 'diare', 'sembelit', 
    'sesak', 'napas', 'berdarah', 'darah', 'berdenyut', 'kembung', 'gatal', 'ruam', 
    'kemerahan', 'merah', 'menggigil', 'kaku', 'kering', 'berkeringat', 'keringat', 
    'bintik', 'bercak', 'perih', 'terbakar', 'tidak'
])

# Gabungkan stopwords kecuali kata-kata penting
stop_words = stop_words.union(medical_stopwords) - important_medical_terms

def normalize_words(text):
    """
    Melakukan normalisasi kata-kata informal dan singkatan
    
    Parameters
    ----------
    text : str
        Teks input yang akan dinormalisasi
    
    Returns
    -------
    str
        Teks yang sudah dinormalisasi
    """
    words = text.split()
    normalized = []
    
    for word in words:
        if word.lower() in word_normalization:
            normalized.append(word_normalization[word.lower()])
        else:
            normalized.append(word)
    
    return ' '.join(normalized)

def clean_text(text):
    """
    Membersihkan teks dari karakter khusus, angka, dan menormalkan unicode
    
    Parameters
    ----------
    text : str
        Teks input yang akan dibersihkan
    
    Returns
    -------
    str
        Teks yang sudah dibersihkan
    """
    # Normalisasi unicode (mengubah karakter khusus menjadi ascii)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    
    # Pola untuk mencocokkan tanggal dan angka (kita perlu mempertahankan ini)
    date_pattern = r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'
    number_pattern = r'\b\d+\b'
    
    # Simpan tanggal dan angka
    dates = re.findall(date_pattern, text)
    numbers = re.findall(number_pattern, text)
    
    # Hapus tanggal dan angka dari teks
    text = re.sub(date_pattern, ' DATE ', text)
    text = re.sub(number_pattern, ' NUM ', text)
    
    # Ubah ke huruf kecil
    text = text.lower()
    
    # Hapus URL
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # Hapus tag HTML
    text = re.sub(r'<.*?>', '', text)
    
    # Hapus emoji dan simbol khusus
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Hapus spasi berlebih
    text = re.sub(r'\s+', ' ', text)
    
    # Kembalikan tanggal dan angka
    for i, date in enumerate(dates):
        text = text.replace('DATE', date, 1)
    
    for i, number in enumerate(numbers):
        text = text.replace('NUM', number, 1)
    
    return text.strip()

def preprocess_text(text):
    """
    Melakukan preprocessing teks berbahasa Indonesia
    
    Parameters
    ----------
    text : str
        Teks input yang akan diproses
    
    Returns
    -------
    str
        Teks yang sudah diproses (distem dan dibersihkan)
    """
    if not text or not isinstance(text, str):
        return ""
      # Pembersihan dan normalisasi teks
    text = clean_text(text)
    
    # Normalisasi kata-kata informal dan singkatan
    text = normalize_words(text)
    
    # Tokenisasi
    try:
        # Coba gunakan tokenizer dengan bahasa Indonesia
        tokens = word_tokenize(text, language='indonesian')
    except:
        # Fallback ke bahasa Inggris jika model bahasa Indonesia tidak tersedia
        tokens = word_tokenize(text)
    
    # Hapus stopwords
    tokens = [word for word in tokens if word not in stop_words]
    
    # Stemming - gunakan hanya untuk kata-kata yang bukan istilah medis penting
    stemmed_tokens = []
    for word in tokens:
        if word in important_medical_terms:
            stemmed_tokens.append(word)  # Simpan kata medis penting apa adanya
        else:
            stemmed_tokens.append(stemmer.stem(word))  # Stem kata-kata lain
    
    # Gabungkan kembali
    preprocessed_text = ' '.join(stemmed_tokens)
    
    return preprocessed_text

def extract_gejala_patterns(text):
    """
    Mengekstrak pola-pola gejala dari teks
    
    Parameters
    ----------
    text : str
        Teks input yang berisi deskripsi gejala
    
    Returns
    -------
    list
        Daftar pola gejala yang diekstrak
    """
    if not text or not isinstance(text, str):
        return []
    
    # Normalisasi teks
    text = clean_text(text)
    text = normalize_words(text)
    
    # Pola-pola regex untuk gejala umum
    patterns = [
        r"(?:saya|aku)?\s*(?:merasa|mengalami|menderita|kena|terkena)?\s*([a-z\s-]+)\s*(?:selama|sejak)?\s*(\d+)?\s*(?:hari|minggu|bulan|tahun)?",
        r"([a-z\s-]+)\s*(?:yang|dan)?\s*(?:tidak kunjung|terus[- ]menerus|tiada henti)",
        r"(?:sering|kadang|selalu)\s*([a-z\s-]+)",
        r"(?:keluar|ada)\s*([a-z\s-]+)\s*(?:dari|di|pada)\s*([a-z\s-]+)"
    ]
    
    extracted = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        if matches:
            for match in matches:
                if isinstance(match, tuple):
                    for item in match:
                        if item and len(item) > 3:  # Minimal 3 karakter
                            extracted.append(item.strip())
                elif match and len(match) > 3:
                    extracted.append(match.strip())
    
    # Hilangkan duplikat
    extracted = list(set(extracted))
    
    return extracted
