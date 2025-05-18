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
        
        Returns
        -------
        pandas.DataFrame
            DataFrame berisi data training
        """
        # Buat contoh data
        sample_data = [
            # Flu
            {"symptoms": "Demam tinggi, pilek, hidung tersumbat, bersin-bersin, batuk kering, sakit tenggorokan, nyeri otot", "disease": "Flu"},
            {"symptoms": "Badan panas dingin, kepala pusing, batuk pilek, hidung meler", "disease": "Flu"},
            {"symptoms": "Demam, nyeri otot, sakit kepala, bersin, hidung tersumbat, batuk", "disease": "Flu"},
            {"symptoms": "Badan menggigil, demam, batuk kering, sakit kepala, hidung meler", "disease": "Flu"},
            {"symptoms": "Suhu tubuh tinggi, lemas, bersin-bersin, nyeri tenggorokan, batuk", "disease": "Flu"},
            {"symptoms": "Bersin terus menerus, hidung tersumbat, mata gatal dan berair, tenggorokan gatal", "disease": "Flu"},
            {"symptoms": "Hidung mampet, bersin-bersin, tenggorokan sakit, tubuh panas dingin", "disease": "Flu"},
            {"symptoms": "Badan hangat, bersin terus menerus, batuk kering, tubuh terasa lemas", "disease": "Flu"},
            {"symptoms": "Hidung tersumbat, sulit bernapas lewat hidung, kepala terasa berat, bersin", "disease": "Flu"},
            {"symptoms": "Demam ringan, sakit tenggorokan, batuk berdahak, hidung meler terus", "disease": "Flu"},
            {"symptoms": "Tenggorokan kering, batuk tidak berhenti, badan meriang, nafsu makan hilang", "disease": "Flu"},
            {"symptoms": "Batuk pilek, badan pegal-pegal, demam naik turun, mata berair", "disease": "Flu"},
            
            # Demam Berdarah
            {"symptoms": "Demam tinggi mendadak, nyeri di belakang mata, sakit kepala parah, ruam merah, nyeri sendi dan otot", "disease": "Demam Berdarah"},
            {"symptoms": "Demam 40 derajat, nyeri otot dan sendi, mual, muntah, bintik merah di kulit", "disease": "Demam Berdarah"},
            {"symptoms": "Panas tinggi selama 2-7 hari, nyeri sendi luar biasa, sakit kepala berat, bintik merah di anggota tubuh", "disease": "Demam Berdarah"},
            {"symptoms": "Demam tinggi, perdarahan gusi, mimisan, bintik merah di tubuh, mual dan muntah", "disease": "Demam Berdarah"},
            {"symptoms": "Panas tinggi, nyeri otot dan sendi parah, mata merah dan nyeri, lemas, bintik kemerahan", "disease": "Demam Berdarah"},
            {"symptoms": "Bintik-bintik merah di kulit seperti bekas gigitan nyamuk, demam tinggi, pusing, mual, muntah", "disease": "Demam Berdarah"},
            {"symptoms": "Demam tinggi disertai menggigil, sakit kepala hebat bagian belakang, nyeri sendi dan otot, muntah", "disease": "Demam Berdarah"},
            {"symptoms": "Demam naik tiba-tiba, nyeri pada mata saat digerakkan, penurunan nafsu makan, bintik merah di kulit", "disease": "Demam Berdarah"},
            {"symptoms": "Muntah terus menerus, demam sangat tinggi, sakit kepala parah, nyeri otot dan sendi, ruam merah", "disease": "Demam Berdarah"},
            {"symptoms": "Kelelahan ekstrem, demam tinggi, kulit tampak kemerahan, nyeri sendi dan otot yang hebat", "disease": "Demam Berdarah"},
            {"symptoms": "Mimisan berulang, gusi berdarah, demam tinggi selama beberapa hari, lemas tak bertenaga", "disease": "Demam Berdarah"},
            {"symptoms": "Mata merah dan sakit, panas 40 derajat, nyeri seluruh badan, muncul bintik merah saat demam turun", "disease": "Demam Berdarah"},
            
            # Tipes
            {"symptoms": "Demam tinggi berkelanjutan, sakit kepala, nafsu makan menurun, nyeri perut, sembelit atau diare", "disease": "Tipes"},
            {"symptoms": "Demam naik secara bertahap, lemas, sakit perut, tidak nafsu makan, lidah kotor", "disease": "Tipes"},
            {"symptoms": "Panas tinggi terus menerus, nyeri perut bagian kanan bawah, sembelit, lidah berselaput", "disease": "Tipes"},
            {"symptoms": "Demam lebih dari seminggu, sakit kepala, tidak nafsu makan, perut tidak nyaman", "disease": "Tipes"},
            {"symptoms": "Panas terus-menerus, lemas, mual, sakit perut, lidah kotor, konstipasi", "disease": "Tipes"},
            {"symptoms": "Demam yang naik di sore hari, lidah putih kotor, sakit perut, sembelit bergantian dengan diare, lemah lesu", "disease": "Tipes"},
            {"symptoms": "Demam bertahan lama, perut kembung, sakit kepala terus menerus, tidak nafsu makan sama sekali", "disease": "Tipes"},
            {"symptoms": "Demam yang tidak turun dengan obat biasa, lidah putih, perut sakit ketika ditekan", "disease": "Tipes"},
            {"symptoms": "Lemas luar biasa, demam lebih dari 7 hari, perut kembung dan nyeri, lidah berwarna putih", "disease": "Tipes"},
            {"symptoms": "Lidah berwarna putih tebal, panas tidak kunjung turun, konstipasi, nyeri perut kanan bawah", "disease": "Tipes"},
            {"symptoms": "Tidak bisa makan, demam hampir 2 minggu, sakit kepala hebat, badan lemas", "disease": "Tipes"},
            {"symptoms": "Batuk kering, panas naik turun saat sore hari, nafsu makan hilang, sakit perut", "disease": "Tipes"},
            
            # TBC
            {"symptoms": "Batuk berdahak lebih dari 2 minggu, batuk berdarah, nyeri dada, demam, berkeringat di malam hari, berat badan turun", "disease": "TBC"},
            {"symptoms": "Batuk terus-menerus selama berminggu-minggu, dahak kental, demam tidak tinggi tapi berkelanjutan, keringat malam", "disease": "TBC"},
            {"symptoms": "Batuk lama tidak sembuh, sesak napas, dahak kadang berdarah, demam malam, berat badan turun", "disease": "TBC"},
            {"symptoms": "Batuk berlangsung lebih dari sebulan, batuk keluar darah, berkeringat malam, demam tidak terlalu tinggi", "disease": "TBC"},
            {"symptoms": "Batuk berdahak berkepanjangan, mual, kehilangan nafsu makan, kelelahan ekstrem, keringat di malam hari", "disease": "TBC"},
            {"symptoms": "Dahak bercampur darah, batuk lama lebih dari 3 minggu, berat badan menurun drastis, demam naik turun", "disease": "TBC"},
            {"symptoms": "Napas pendek, batuk darah, demam rendah yang berkelanjutan, badan terasa lemah terus menerus", "disease": "TBC"},
            {"symptoms": "Batuk terus menerus yang tidak sembuh dengan obat biasa, sesak saat beraktivitas, keringat berlebih saat malam", "disease": "TBC"},
            {"symptoms": "Dahak berlendir dan kadang berdarah, nafsu makan turun, berat badan terus menurun, badan lemah", "disease": "TBC"},
            {"symptoms": "Batuk selama lebih dari sebulan, suhu tubuh naik tiap sore, sesak napas ringan, lemas", "disease": "TBC"},
            
            # Maag
            {"symptoms": "Nyeri perut bagian atas, perut kembung, mual, muntah, cepat kenyang, sendawa", "disease": "Maag"},
            {"symptoms": "Sakit perut terutama saat lapar, mual, perut terasa penuh dan kembung", "disease": "Maag"},
            {"symptoms": "Nyeri terbakar di ulu hati, perut kembung, sendawa terus-menerus, mual setelah makan", "disease": "Maag"},
            {"symptoms": "Perut sakit seperti ditusuk-tusuk, mual, muntah, tidak nafsu makan", "disease": "Maag"},
            {"symptoms": "Nyeri perut yang membaik setelah makan, kembung, sering bersendawa, mual", "disease": "Maag"},
            {"symptoms": "Perih di lambung jika telat makan, mual, mulut terasa asam, nafsu makan berkurang", "disease": "Maag"},
            {"symptoms": "Sakit perut bagian atas setelah makan pedas, mual dan muntah, perut kembung", "disease": "Maag"},
            {"symptoms": "Nyeri perut yang hilang timbul, mual pagi hari, mudah kenyang saat makan", "disease": "Maag"},
            {"symptoms": "Sakit perut malam hari sampai terbangun, bersendawa terus menerus, mual", "disease": "Maag"},
            {"symptoms": "Nyeri seperti terbakar di dada dan perut atas, sendawa asam, kembung", "disease": "Maag"},
            {"symptoms": "Perut sakit saat perut kosong atau lapar, mual, kembung, nafsu makan berkurang", "disease": "Maag"},
            
            # Asma
            {"symptoms": "Sesak napas mendadak, mengi saat bernapas, dada terasa sesak, batuk-batuk terutama malam hari", "disease": "Asma"},
            {"symptoms": "Sulit bernapas terutama saat beraktivitas, bunyi mengi saat napas, batuk kering berulang", "disease": "Asma"},
            {"symptoms": "Napas berbunyi seperti peluit, dada terasa tertekan, sulit bernapas saat tertawa atau olahraga", "disease": "Asma"},
            {"symptoms": "Serangan sesak napas di malam hari, batuk kering terus menerus, napas bunyi mengi", "disease": "Asma"},
            {"symptoms": "Kesulitan bernapas, batuk terus-menerus, dada sesak, napas bunyi seperti peluit", "disease": "Asma"},
            {"symptoms": "Serangan sesak napas, batuk, napas berbunyi, kesulitan tidur karena batuk", "disease": "Asma"},
            {"symptoms": "Kesulitan bernapas setelah terpapar udara dingin, debu, atau asap, dada sesak", "disease": "Asma"},
            {"symptoms": "Batuk kering terus menerus terutama malam hari, napas pendek, dada terasa berat", "disease": "Asma"},
            {"symptoms": "Sulit bernapas ketika beraktivitas, batuk tidak kunjung sembuh, dada terasa ditekan", "disease": "Asma"},
            {"symptoms": "Napas berbunyi saat menghembuskan napas, batuk tidak berhenti dengan obat batuk biasa", "disease": "Asma"},
            {"symptoms": "Gagal menyelesaikan kalimat saat berbicara karena napas pendek, batuk malam hari", "disease": "Asma"},
            
            # Migrain
            {"symptoms": "Sakit kepala berdenyut di satu sisi, mual, muntah, sensitif terhadap cahaya dan suara", "disease": "Migrain"},
            {"symptoms": "Nyeri kepala parah, pandangan kabur, sensitif terhadap cahaya, mual", "disease": "Migrain"},
            {"symptoms": "Sakit kepala berdenyut, mual, sensitif terhadap suara, penglihatan berbayang", "disease": "Migrain"},
            {"symptoms": "Nyeri kepala sebelah, sensitif terhadap cahaya dan suara, mual, muntah", "disease": "Migrain"},
            {"symptoms": "Sakit kepala hebat, mual, mata berkunang-kunang, sensitif terhadap suara", "disease": "Migrain"},
            {"symptoms": "Sakit kepala sebelah yang bertambah parah saat beraktivitas, mual, pandangan kabur", "disease": "Migrain"},
            {"symptoms": "Melihat kilatan cahaya sebelum sakit kepala, nyeri berdenyut di satu sisi kepala", "disease": "Migrain"},
            {"symptoms": "Sakit kepala yang memburuk dengan gerakan, cahaya terang memperparah sakit kepala", "disease": "Migrain"},
            {"symptoms": "Kepala berdenyut seperti ditusuk-tusuk di satu sisi, mual, sensitif terhadap bau", "disease": "Migrain"},
            {"symptoms": "Sakit kepala yang berlangsung berjam-jam hingga berhari-hari, muntah, pusing", "disease": "Migrain"},
            {"symptoms": "Nyeri kepala berdenyut yang menghalangi aktivitas sehari-hari, sensitif cahaya", "disease": "Migrain"},
            
            # Diare
            {"symptoms": "BAB cair lebih dari 3 kali sehari, sakit perut, kram perut, mual, muntah", "disease": "Diare"},
            {"symptoms": "BAB encer berkali-kali, perut kram, mual, lemas, dehidrasi", "disease": "Diare"},
            {"symptoms": "Buang air besar cair berkali-kali, sakit perut, mual, muntah, kurang nafsu makan", "disease": "Diare"},
            {"symptoms": "BAB encer terus menerus, perut sakit, kembung, mual, badan lemas", "disease": "Diare"},
            {"symptoms": "Mencret berkali-kali, kram perut, mual, muntah, haus terus", "disease": "Diare"},
            {"symptoms": "Feses berair, rasa tidak nyaman di perut, sering ke toilet, mual", "disease": "Diare"},
            {"symptoms": "BAB encer dengan lendir atau darah, sakit perut hebat, demam, lemas", "disease": "Diare"},
            {"symptoms": "Sering buang air besar yang encer, perut seperti melilit, mulut kering", "disease": "Diare"},
            {"symptoms": "BAB dengan bau sangat menyengat, perut kembung dan berbunyi, lemas", "disease": "Diare"},
            {"symptoms": "Perut kram sebelum BAB, feses sangat encer, tubuh terasa lemah", "disease": "Diare"},
            {"symptoms": "Buang air besar encer lebih dari 10 kali sehari, nyeri perut, mual terus menerus", "disease": "Diare"},
            
            # Hipertensi
            {"symptoms": "Sakit kepala, pusing, jantung berdebar, sesak napas, telinga berdenging", "disease": "Hipertensi"},
            {"symptoms": "Sakit kepala parah, pusing, sesak napas, jantung berdebar kencang", "disease": "Hipertensi"},
            {"symptoms": "Pusing, sakit kepala terutama di tengkuk, wajah kemerahan, mudah lelah", "disease": "Hipertensi"},
            {"symptoms": "Pusing, leher kaku, pandangan kabur, sesak napas, jantung berdebar", "disease": "Hipertensi"},
            {"symptoms": "Sakit kepala, penglihatan kabur, jantung berdebar, sulit tidur", "disease": "Hipertensi"},
            {"symptoms": "Nyeri di bagian belakang kepala, wajah merah, mata berkunang-kunang", "disease": "Hipertensi"},
            {"symptoms": "Telinga berdengung, pusing saat bangun tidur, jantung terasa berdebar", "disease": "Hipertensi"},
            {"symptoms": "Sakit kepala di pagi hari, tengkuk terasa berat, mudah marah, wajah merah", "disease": "Hipertensi"},
            {"symptoms": "Kepala terasa berat dan pusing, mimisan kadang-kadang, cepat lelah", "disease": "Hipertensi"},
            {"symptoms": "Napas pendek-pendek, jantung berdebar kencang, muka merah, mudah lelah", "disease": "Hipertensi"},
            {"symptoms": "Pandangan kabur sewaktu-waktu, nyeri kepala belakang terus-menerus", "disease": "Hipertensi"},
            
            # Diabetes
            {"symptoms": "Sering buang air kecil, selalu haus, selalu lapar, berat badan turun, pandangan kabur, luka lambat sembuh", "disease": "Diabetes"},
            {"symptoms": "Kencing terus-menerus, haus terus, lapar berlebihan, berat badan menurun", "disease": "Diabetes"},
            {"symptoms": "Sering kencing terutama malam hari, haus berlebihan, lemas, luka sulit sembuh", "disease": "Diabetes"},
            {"symptoms": "Kencing terus, selalu haus, nafsu makan bertambah, lemas, penglihatan kabur", "disease": "Diabetes"},
            {"symptoms": "Haus terus, sering pipis, cepat lelah, berat badan turun tanpa sebab", "disease": "Diabetes"},
            {"symptoms": "Luka yang lama sembuh, sering haus dan lapar, kencing berkali-kali di malam hari", "disease": "Diabetes"},
            {"symptoms": "Sering kencing dalam jumlah banyak, haus terus menerus, kulit kering dan gatal", "disease": "Diabetes"},
            {"symptoms": "Pandangan kabur, berat badan turun drastis padahal makan banyak, cepat lelah", "disease": "Diabetes"},
            {"symptoms": "Infeksi jamur berulang, gatal pada kulit, sering buang air kecil, sangat haus", "disease": "Diabetes"},
            {"symptoms": "Kesemutan pada tangan dan kaki, haus luar biasa, sering kencing, lemas", "disease": "Diabetes"},
            {"symptoms": "Luka yang lambat sembuh, sering kencing, haus terus, vitalitas menurun", "disease": "Diabetes"},
            
            # Eksim
            {"symptoms": "Ruam merah, gatal, kulit kering dan bersisik, kulit melepuh dan mengeluarkan cairan", "disease": "Eksim"},
            {"symptoms": "Kulit gatal terus-menerus, kulit memerah, kulit kering pecah-pecah, bersisik", "disease": "Eksim"},
            {"symptoms": "Kulit gatal yang memburuk malam hari, kulit meradang, area kulit menebal", "disease": "Eksim"},
            {"symptoms": "Gatal parah, kulit kasar dan kering, luka mudah infeksi, ruam merah", "disease": "Eksim"},
            {"symptoms": "Kulit kering, gatal, merah, dan bersisik terutama di siku dan lutut", "disease": "Eksim"},
            {"symptoms": "Kulit mengelupas, sangat gatal, merah, dan kadang basah atau berkeropeng", "disease": "Eksim"},
            {"symptoms": "Lepuhan kecil yang gatal dan pecah mengeluarkan cairan, kulit merah dan kasar", "disease": "Eksim"},
            {"symptoms": "Kulit kering yang gatal dan memerah setelah kontak dengan sabun atau deterjen", "disease": "Eksim"},
            {"symptoms": "Penebalan kulit di area yang sering digaruk, kulit berminyak dan bersisik", "disease": "Eksim"},
            {"symptoms": "Gatal yang memburuk saat berkeringat, kulit kering dan pecah-pecah, merah", "disease": "Eksim"},
            {"symptoms": "Ruam kulit yang gatal dan terasa panas, kulit kering dan bersisik, menebal", "disease": "Eksim"},
            
            # Infeksi Saluran Kemih (ISK)
            {"symptoms": "Sering buang air kecil, rasa terbakar saat kencing, urine keruh atau berbau tajam, nyeri perut bagian bawah", "disease": "Infeksi Saluran Kemih"},
            {"symptoms": "Nyeri atau terbakar saat buang air kecil, sering ingin kencing tapi sedikit keluar", "disease": "Infeksi Saluran Kemih"},
            {"symptoms": "Urine berbau menyengat, nyeri di bawah pusar, sering buang air kecil", "disease": "Infeksi Saluran Kemih"},
            {"symptoms": "Kencing sakit dan panas, urine keruh kadang berdarah, nyeri pinggang", "disease": "Infeksi Saluran Kemih"},
            {"symptoms": "Buang air kecil tidak tuntas, nyeri panggul, demam ringan, urine berbau tajam", "disease": "Infeksi Saluran Kemih"},
            {"symptoms": "Sering terasa ingin kencing tapi sedikit yang keluar, nyeri perut bagian bawah", "disease": "Infeksi Saluran Kemih"},
            {"symptoms": "Sakit saat kencing, urine keruh atau kemerahan, nyeri di pinggang", "disease": "Infeksi Saluran Kemih"},
            {"symptoms": "Nyeri atau terbakar saat buang air kecil, urine berbau tajam, rasa tidak nyaman di perut bawah", "disease": "Infeksi Saluran Kemih"},
            {"symptoms": "Sering buang air kecil dalam jumlah sedikit, kencing terasa sakit, urine berbau", "disease": "Infeksi Saluran Kemih"},
            {"symptoms": "Rasa tidak tuntas setelah buang air kecil, nyeri di area kandung kemih", "disease": "Infeksi Saluran Kemih"},
            {"symptoms": "Nyeri pinggang, demam ringan, sakit saat kencing, urine berbau tidak sedap", "disease": "Infeksi Saluran Kemih"},
            
            # Radang Sendi
            {"symptoms": "Nyeri sendi, bengkak pada sendi, kaku sendi terutama pagi hari, sendi terasa hangat", "disease": "Radang Sendi"},
            {"symptoms": "Sendi kaku dan sakit, terutama pagi hari atau setelah tidak aktif", "disease": "Radang Sendi"},
            {"symptoms": "Bengkak dan nyeri di sendi, sulit menggerakkan sendi, kadang muncul benjolan", "disease": "Radang Sendi"},
            {"symptoms": "Sendi terasa panas dan sakit jika disentuh, kaku di pagi hari, bengkak", "disease": "Radang Sendi"},
            {"symptoms": "Nyeri sendi ketika bergerak, kaku sendi lebih dari 30 menit di pagi hari", "disease": "Radang Sendi"},
            {"symptoms": "Kemerahan dan pembengkakan di area sendi, terasa sakit saat ditekan", "disease": "Radang Sendi"},
            {"symptoms": "Bunyi gemertak saat sendi digerakkan, nyeri dan tidak nyaman di sendi", "disease": "Radang Sendi"},
            {"symptoms": "Sendi kaku setelah duduk lama, sakit saat digerakkan, terasa hangat", "disease": "Radang Sendi"},
            {"symptoms": "Pembengkakan sendi yang tidak hilang, sakit terus-menerus, kekakuan", "disease": "Radang Sendi"},
            {"symptoms": "Sendi sakit sepanjang hari, terasa hangat, bengkak, dan sulit digerakkan", "disease": "Radang Sendi"},
            {"symptoms": "Nyeri sendi yang parah ketika cuaca berubah, kaku di pagi hari, bengkak", "disease": "Radang Sendi"},
            
            # Alergi Makanan
            {"symptoms": "Gatal-gatal, ruam pada kulit, mual, muntah, diare, bengkak pada bibir atau lidah", "disease": "Alergi Makanan"},
            {"symptoms": "Ruam merah pada kulit setelah makan, gatal-gatal, perut kram", "disease": "Alergi Makanan"},
            {"symptoms": "Bibir bengkak, gatal-gatal, sulit bernapas setelah mengonsumsi makanan tertentu", "disease": "Alergi Makanan"},
            {"symptoms": "Mual dan muntah setelah makan, ruam kulit, gatal-gatal seluruh tubuh", "disease": "Alergi Makanan"},
            {"symptoms": "Diare mendadak setelah makan, perut kram, kulit gatal dan kemerahan", "disease": "Alergi Makanan"},
            {"symptoms": "Tenggorokan gatal, bibir bengkak, napas berbunyi setelah makan", "disease": "Alergi Makanan"},
            {"symptoms": "Wajah bengkak, kulit merah dan gatal, mual setelah makan makanan tertentu", "disease": "Alergi Makanan"},
            {"symptoms": "Kulit gatal dan muncul bentol-bentol, bibir dan tenggorokan gatal", "disease": "Alergi Makanan"},
            {"symptoms": "Sesak napas, batuk, bersin setelah mengonsumsi makanan tertentu", "disease": "Alergi Makanan"},
            {"symptoms": "Lidah terasa tebal, bibir bengkak, muncul ruam merah di tubuh setelah makan", "disease": "Alergi Makanan"},
            {"symptoms": "Muntah mendadak setelah makan, kulit gatal-gatal, perut kram", "disease": "Alergi Makanan"},
            
            # Sinusitis
            {"symptoms": "Hidung tersumbat, sakit kepala, nyeri di sekitar mata dan pipi, lendir kental berwarna kuning atau hijau", "disease": "Sinusitis"},
            {"symptoms": "Sakit kepala yang memburuk saat membungkuk, hidung mampet, ingus kental", "disease": "Sinusitis"},
            {"symptoms": "Nyeri wajah di sekitar mata, hidung, dan dahi, hidung tersumbat, ingus berwarna", "disease": "Sinusitis"},
            {"symptoms": "Hidung tersumbat, sakit kepala, dan nyeri wajah, tenggorokan sakit", "disease": "Sinusitis"},
            {"symptoms": "Nyeri di pipi dan dahi, hidung tersumbat, batuk yang memburuk di malam hari", "disease": "Sinusitis"},
            {"symptoms": "Ingus kental berwarna kuning atau hijau, sakit kepala, nyeri wajah", "disease": "Sinusitis"},
            {"symptoms": "Nyeri saat menunduk, hidung tersumbat terus-menerus, napas bau", "disease": "Sinusitis"},
            {"symptoms": "Wajah terasa penuh dan nyeri, lendir menetes ke tenggorokan, lelah", "disease": "Sinusitis"},
            {"symptoms": "Sakit di wajah atas, nyeri saat menekan pipi dan dahi, hidung mampet", "disease": "Sinusitis"},
            {"symptoms": "Hidung berlendir tebal, nyeri di sekitar hidung dan mata, sakit kepala", "disease": "Sinusitis"},
            {"symptoms": "Hidung mampet, sakit kepala dan wajah, ingus kental yang sulit keluar", "disease": "Sinusitis"}
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
        
        # Dapatkan top 3 penyakit dengan probabilitas tertinggi
        indices = probas.argsort()[-3:][::-1]  # Indeks 3 probabilitas tertinggi
        top_diseases = [(self.pipeline.classes_[i], probas[i]) for i in indices]
        
        # Jika confidence terlalu rendah, kita ragu dengan prediksi
        if max_proba < 0.5:
            # Jika ada beberapa penyakit dengan probabilitas yang dekat (selisih < 0.15)
            # maka kita menganggap ini sebagai kasus yang tidak pasti
            if len(top_diseases) > 1 and (top_diseases[0][1] - top_diseases[1][1]) < 0.15:
                # Tetap kembalikan penyakit dengan probabilitas tertinggi, tapi dengan flag ketidakpastian
                return predicted_disease, max_proba, top_diseases
            
            # Jika probabilitas terlalu rendah (< 0.35), kita anggap sebagai "Tidak diketahui"
            if max_proba < 0.35:
                return "Tidak diketahui", max_proba, top_diseases
        
        # Jika confidence cukup tinggi, kembalikan prediksi utama
        return predicted_disease, max_proba, top_diseases
    
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
