"""
Chatbot sederhana untuk menjawab pertanyaan tentang penyakit
"""
import os
import json
import re
from utils.preprocessor import preprocess_text
from difflib import get_close_matches

class Chatbot:
    """
    Kelas untuk chatbot sederhana yang menjawab pertanyaan tentang penyakit
    """
    
    def __init__(self):
        """
        Inisialisasi chatbot
        """
        # Path ke file data penyakit
        self.diseases_data_path = os.path.join('data', 'diseases.json')
        # Path ke file data FAQ
        self.faq_data_path = os.path.join('data', 'faq.json')
        
        # Muat data penyakit
        self.diseases_data = self._load_diseases_data()
        # Muat data FAQ
        self.faq_data = self._load_faq_data()

        # Siapkan kamus sinonim penyakit untuk meningkatkan pengenalan
        self.disease_synonyms = self._create_disease_synonyms()
        
        # Pattern untuk mengenali pertanyaan
        self.patterns = {
            'apa_itu': [
                r'apa itu (.*)', 
                r'apa yang dimaksud dengan (.*)', 
                r'apa sih (.*)', 
                r'tolong jelaskan (.*)',
                r'(.*) itu apa',
                r'jelaskan tentang (.*)',
                r'bisa jelaskan (.*)',
                r'apa (.*) itu'
            ],
            'gejala': [
                r'apa gejala (.*)', 
                r'gejala (.*) apa saja', 
                r'ciri-ciri (.*)', 
                r'tanda-tanda (.*)',
                r'gimana (sih |)tau kalo kena (.*)',
                r'apa saja ciri-ciri (.*)',
                r'bagaimana mengetahui (.*)',
                r'terkena (.*) itu seperti apa',
                r'gejala dari (.*)'
            ],
            'penanganan': [
                r'bagaimana (cara |)menangani (.*)', 
                r'gimana (cara |)mengobati (.*)', 
                r'apa pengobatan (.*)', 
                r'bagaimana jika terkena (.*)',
                r'kalau kena (.*) gimana',
                r'cara mengobati (.*)',
                r'obat (.*)',
                r'pengobatan untuk (.*)',
                r'terapi (.*)'
            ],
            'pencegahan': [
                r'bagaimana (cara |)mencegah (.*)', 
                r'cara mencegah (.*)', 
                r'gimana supaya tidak kena (.*)', 
                r'pencegahan (.*)',
                r'cara agar tidak terkena (.*)',
                r'mencegah (.*) bagaimana',
                r'bagaimana menghindari (.*)',
                r'agar tidak (.*)'
            ],
            'durasi': [
                r'berapa lama (.*) sembuh', 
                r'(.*) sembuh dalam berapa lama', 
                r'waktu sembuh (.*)', 
                r'durasi penyembuhan (.*)',
                r'kalau (.*) berapa lama sembuh',
                r'berapa lama pengobatan (.*)',
                r'sembuhnya (.*) berapa lama',
                r'waktu yang diperlukan untuk (.*) sembuh'
            ],
            'umum': [
                r'kalau ([^,]*) ([^,]*) (hari|minggu|bulan) (.*)',
                r'jika ([^,]*) ([^,]*) (hari|minggu|bulan) (.*)',
                r'bila ([^,]*) ([^,]*) (hari|minggu|bulan) (.*)',
                r'apakah berbahaya ([^,]*)',
                r'apakah perlu ke dokter ([^,]*)'
            ]
        }
    
    def _load_diseases_data(self):
        """
        Memuat data penyakit dari JSON
        
        Returns
        -------
        dict
            Dictionary berisi informasi penyakit
        """
        try:
            with open(self.diseases_data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Jika file tidak ada, buat dictionary kosong
            data = {}
        
        return data
    
    def _load_faq_data(self):
        """
        Memuat data FAQ dari JSON.
        Jika file tidak ada, akan dibuat data contoh.
        
        Returns
        -------
        dict
            Dictionary berisi FAQ
        """
        try:
            # Coba load file JSON jika sudah ada
            with open(self.faq_data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"Data FAQ berhasil dimuat dari {self.faq_data_path}")
        except (FileNotFoundError, json.JSONDecodeError):
            # Jika file belum ada, buat contoh data FAQ
            print(f"File {self.faq_data_path} tidak ditemukan. Membuat data contoh...")
            data = self._create_sample_faq()
        
        return data
    
    def _create_sample_faq(self):
        """
        Membuat contoh data FAQ jika belum ada file JSON.
        
        Returns
        -------
        dict
            Dictionary berisi FAQ
        """
        # Data contoh FAQ
        sample_data = {
            "umum": {
                "demam tinggi lebih dari 3 hari": "Jika demam tinggi berlangsung lebih dari 3 hari, segera periksakan diri ke dokter untuk evaluasi lebih lanjut. Demam berkepanjangan bisa menjadi tanda infeksi serius seperti tipes, demam berdarah, atau infeksi lainnya. Sambil menunggu pemeriksaan dokter, Anda dapat mengompres dengan air hangat dan minum obat penurun panas sesuai dosis.",
                "sakit kepala terus menerus": "Sakit kepala terus-menerus yang tidak kunjung mereda bisa disebabkan oleh berbagai hal, seperti migrain, ketegangan otot, sinusitis, atau masalah yang lebih serius. Penting untuk periksakan diri ke dokter jika sakit kepala berlangsung lebih dari 2-3 hari, sangat parah, atau disertai dengan gejala seperti demam, kaku leher, atau muntah.",
                "batuk tidak sembuh sembuh": "Batuk yang tidak kunjung sembuh selama lebih dari 2-3 minggu memerlukan perhatian medis. Hal ini bisa menjadi tanda infeksi paru-paru, asma, refluks asam, alergi, atau kondisi lain yang memerlukan penanganan khusus. Jika batuk disertai dengan dahak berdarah, sesak napas, atau demam, segera periksakan diri ke dokter.",
                "mual dan muntah berhari hari": "Mual dan muntah yang berlangsung berhari-hari dapat menyebabkan dehidrasi dan gangguan elektrolit. Kondisi ini bisa disebabkan oleh infeksi virus, keracunan makanan, migren, gangguan pencernaan, atau masalah kesehatan lainnya. Jika muntah berlangsung lebih dari 2 hari atau disertai nyeri perut hebat, segera periksakan diri ke dokter. Pastikan tetap terhidrasi dengan minum cairan secara perlahan.",
                "diare lebih dari 3 hari": "Diare yang berlangsung lebih dari 3 hari berisiko menyebabkan dehidrasi dan memerlukan penanganan medis. Kondisi ini bisa disebabkan oleh infeksi bakteri/virus, parasit, intoleransi makanan, atau gangguan pencernaan lainnya. Penting untuk minum banyak cairan (oralit), menghindari makanan yang sulit dicerna, dan periksakan diri ke dokter, terutama jika disertai dengan demam tinggi, darah dalam tinja, atau nyeri perut hebat."
            },
            "gejala_tambahan": {
                "Flu": [
                    "batuk pilek",
                    "hidung tersumbat",
                    "bersin-bersin",
                    "sakit tenggorokan",
                    "demam",
                    "nyeri otot"
                ],
                "Demam Berdarah": [
                    "demam tinggi mendadak",
                    "nyeri di belakang mata",
                    "nyeri sendi dan otot",
                    "ruam merah",
                    "mimisan",
                    "nyeri kepala berat"
                ],
                "Tipes": [
                    "demam tinggi bertahap",
                    "nafsu makan menurun",
                    "sakit perut",
                    "sembelit atau diare",
                    "lidah berselaput putih",
                    "lemas"
                ],
                "TBC": [
                    "batuk lebih dari 2 minggu",
                    "batuk darah",
                    "nyeri dada",
                    "keringat malam",
                    "berat badan turun",
                    "sesak napas"
                ],
                "Maag": [
                    "nyeri ulu hati",
                    "perut kembung",
                    "sendawa berlebihan",
                    "mual",
                    "cepat kenyang",
                    "muntah"
                ],
                "Asma": [
                    "sesak napas",
                    "napas berbunyi",
                    "batuk-batuk",
                    "dada terasa berat",
                    "kesulitan bernapas",
                    "batuk malam hari"
                ],
                "Migrain": [
                    "sakit kepala berdenyut",
                    "mual",
                    "muntah",
                    "sensitif terhadap cahaya",
                    "sensitif terhadap suara",
                    "pusing"
                ],
                "Diare": [
                    "BAB cair lebih dari 3 kali sehari",
                    "kram perut",
                    "mual",
                    "muntah",
                    "demam ringan",
                    "dehidrasi"
                ],
                "Hipertensi": [
                    "sakit kepala",
                    "jantung berdebar",
                    "pusing",
                    "telinga berdenging",
                    "sesak napas",
                    "wajah kemerahan"
                ],
                "Diabetes": [
                    "sering buang air kecil",
                    "selalu haus",
                    "selalu lapar",
                    "berat badan turun",
                    "luka lambat sembuh",
                    "pandangan kabur"
                ]
            }
        }
        
        # Buat direktori data jika belum ada
        os.makedirs(os.path.dirname(self.faq_data_path), exist_ok=True)
        
        # Simpan ke JSON
        with open(self.faq_data_path, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, indent=4, ensure_ascii=False)
        
        print(f"Data contoh FAQ berhasil dibuat dan disimpan ke {self.faq_data_path}")
        
        return sample_data
    
    def _create_disease_synonyms(self):
        """
        Membuat kamus sinonim penyakit untuk meningkatkan pengenalan
        
        Returns
        -------
        dict
            Dictionary berisi sinonim untuk setiap penyakit
        """
        synonyms = {
            "Flu": ["influenza", "pilek", "flu biasa", "flu ringan", "flu musiman", 
                   "batuk pilek", "hidung meler", "masuk angin"],
            "Demam Berdarah": ["dbd", "db", "demam dengue", "dengue", "demam berdarah dengue", 
                              "penyakit nyamuk", "demam dengue", "panas berdarah"],
            "Tipes": ["tifus", "tipus", "typhoid", "tipes abdominalis", "demam tifoid",
                     "penyakit tipes", "sakit tipes", "demam tipus"],
            "TBC": ["tuberkulosis", "tb", "tuberculosis", "tbc paru", "flek paru",
                   "batuk tbc", "batuk darah", "batuk kering", "batuk lama"],
            "Maag": ["dispepsia", "sakit lambung", "sakit maag", "asam lambung", 
                    "radang lambung", "perih lambung", "nyeri lambung", "gerd"],
            "Asma": ["bengek", "sesak nafas", "asma bronkial", "penyakit asma",
                    "sesak napas", "mengi", "wheezing", "asma akut"],
            "Migrain": ["sakit kepala", "migrain kronis", "nyeri kepala", "sakit kepala sebelah",
                       "migrain tanpa aura", "migrain dengan aura", "sakit kepala berdenyut"],
            "Diare": ["mencret", "berak cair", "sakit perut", "disentri", "gastroenteritis",
                     "buang air besar cair", "muntaber", "sakit mencret"],
            "Hipertensi": ["darah tinggi", "tekanan darah tinggi", "hipertensi primer", 
                          "hipertensi sekunder", "penyakit darah tinggi", "tensi tinggi"],
            "Diabetes": ["kencing manis", "diabetes mellitus", "gula darah tinggi", 
                        "diabetes tipe 1", "diabetes tipe 2", "sakit gula", "penyakit gula"],
            "Alergi Makanan": ["alergi", "reaksi alergi", "hipersensitivitas", "alergi makanan laut", 
                              "alergi kacang", "alergi susu", "alergi telur", "intoleransi makanan"],
            "Sinusitis": ["radang sinus", "infeksi sinus", "hidung tersumbat", "nyeri wajah",
                         "sinus kronis", "sinus akut", "hidung mampet"]
        }
        return synonyms
    def _extract_disease_from_question(self, question_type, question):
        """
        Ekstrak nama penyakit dari pertanyaan dengan dukungan fuzzy matching
        
        Parameters
        ----------
        question_type : str
            Tipe pertanyaan ('apa_itu', 'gejala', dll)
        question : str
            Pertanyaan pengguna
        
        Returns
        -------
        str
            Nama penyakit atau None jika tidak ditemukan
        """
        for pattern in self.patterns[question_type]:
            match = re.search(pattern, question, re.IGNORECASE)
            if match:
                # Ekstrak nama penyakit dari match group
                disease_name = match.group(1) if question_type != 'umum' else None
                
                if disease_name:
                    # Bersihkan hasil ekstraksi
                    disease_name = disease_name.strip().lower()
                    
                    # Coba temukan kecocokan langsung dengan nama penyakit
                    for disease in self.diseases_data.keys():
                        if disease.lower() in disease_name or disease_name in disease.lower():
                            return disease
                    
                    # Coba temukan kecocokan dengan sinonim
                    for disease, synonyms in self.disease_synonyms.items():
                        for synonym in synonyms:
                            if synonym.lower() in disease_name or disease_name in synonym.lower():
                                return disease
                    
                    # Gunakan fuzzy matching jika tidak ditemukan kecocokan langsung
                    disease_candidates = list(self.diseases_data.keys()) + [syn for syns in self.disease_synonyms.values() for syn in syns]
                    matches = get_close_matches(disease_name, disease_candidates, n=1, cutoff=0.7)
                    
                    if matches:
                        matched_term = matches[0]
                        # Jika yang cocok adalah sinonim, kembalikan nama penyakit aslinya
                        for disease, synonyms in self.disease_synonyms.items():
                            if matched_term in synonyms:
                                return disease
                        # Jika yang cocok adalah nama penyakit, kembalikan apa adanya
                        if matched_term in self.diseases_data:
                            return matched_term
                    
                if question_type == 'umum':
                    # Untuk pertanyaan umum, kita mengembalikan seluruh match sebagai string
                    return " ".join([match.group(i) for i in range(1, 5) if match.group(i)])
                
                return disease_name
        
        return None
    def get_response(self, processed_question, original_text):
        """
        Mendapatkan jawaban chatbot berdasarkan pertanyaan user
        
        Parameters
        ----------
        processed_question : str
            Teks pertanyaan yang telah dipreproses
        original_text : str
            Teks pertanyaan asli
        
        Returns
        -------
        str
            Jawaban dari chatbot
        """
        # Coba identifikasi pertanyaan dengan berbagai pattern
        possible_matches = []
        disease_match = None
        
        # Cek jika pertanyaan cocok dengan salah satu pattern FAQ
        for question_type, patterns in self.patterns.items():
            disease_or_condition = self._extract_disease_from_question(question_type, original_text)
            
            if disease_or_condition:
                possible_matches.append((question_type, disease_or_condition))
                
                if not disease_match and disease_or_condition in self.diseases_data:
                    disease_match = disease_or_condition
        
        # Jika ada kecocokan yang valid, gunakan yang pertama
        if possible_matches:
            question_type, disease_or_condition = possible_matches[0]
            
            if question_type == 'apa_itu':
                if disease_or_condition in self.diseases_data:
                    return f"{disease_or_condition} adalah {self.diseases_data[disease_or_condition]['description']}"
                else:
                    # Coba fuzzy matching untuk menemukan penyakit yang mirip
                    disease_candidates = list(self.diseases_data.keys())
                    matches = get_close_matches(disease_or_condition, disease_candidates, n=1, cutoff=0.6)
                    
                    if matches:
                        suggested_disease = matches[0]
                        return f"Saya tidak memiliki informasi spesifik tentang '{disease_or_condition}'. Mungkin maksud Anda '{suggested_disease}'? {suggested_disease} adalah {self.diseases_data[suggested_disease]['description']}"
                    else:
                        return f"Maaf, saya tidak memiliki informasi tentang {disease_or_condition}."
            
            elif question_type == 'gejala':
                if disease_or_condition in self.diseases_data:
                    if disease_or_condition in self.faq_data['gejala_tambahan']:
                        gejala = ", ".join(self.faq_data['gejala_tambahan'][disease_or_condition])
                        return f"Gejala {disease_or_condition} antara lain: {gejala}."
                    else:
                        return f"Maaf, saya belum memiliki data lengkap tentang gejala {disease_or_condition}."
                else:
                    # Coba fuzzy matching
                    disease_candidates = list(self.diseases_data.keys())
                    matches = get_close_matches(disease_or_condition, disease_candidates, n=1, cutoff=0.6)
                    
                    if matches:
                        suggested_disease = matches[0]
                        if suggested_disease in self.faq_data['gejala_tambahan']:
                            gejala = ", ".join(self.faq_data['gejala_tambahan'][suggested_disease])
                            return f"Saya tidak memiliki informasi tentang '{disease_or_condition}'. Mungkin maksud Anda '{suggested_disease}'? Gejala {suggested_disease} antara lain: {gejala}."
                    
                    return f"Maaf, saya tidak memiliki informasi tentang gejala {disease_or_condition}."
            
            elif question_type == 'penanganan':
                if disease_or_condition in self.diseases_data:
                    penanganan = "\n- " + "\n- ".join(self.diseases_data[disease_or_condition]['recommendations'])
                    return f"Penanganan untuk {disease_or_condition}:{penanganan}"
                else:
                    # Coba fuzzy matching
                    disease_candidates = list(self.diseases_data.keys())
                    matches = get_close_matches(disease_or_condition, disease_candidates, n=1, cutoff=0.6)
                    
                    if matches:
                        suggested_disease = matches[0]
                        penanganan = "\n- " + "\n- ".join(self.diseases_data[suggested_disease]['recommendations'])
                        return f"Saya tidak memiliki informasi tentang '{disease_or_condition}'. Mungkin maksud Anda '{suggested_disease}'? Penanganan untuk {suggested_disease}:{penanganan}"
                        
                    return f"Maaf, saya tidak memiliki informasi tentang penanganan {disease_or_condition}."
            
            elif question_type == 'pencegahan':
                # Berikan info pencegahan berdasarkan jenis penyakit
                pencegahan = {
                    "Flu": "Mencuci tangan secara rutin, menghindari kontak dekat dengan orang yang sedang sakit, menjaga daya tahan tubuh dengan istirahat cukup dan makan makanan bergizi.",
                    "Demam Berdarah": "Memberantas sarang nyamuk dengan menguras tempat penampungan air, menutup rapat tempat penampungan air, mendaur ulang barang bekas, dan memantau jentik nyamuk.",
                    "Tipes": "Menjaga kebersihan makanan dan minuman, mencuci tangan sebelum makan, memasak makanan dengan matang, dan menggunakan air bersih.",
                    "TBC": "Mendapatkan vaksinasi BCG, menjaga ventilasi rumah, menghindari kontak dekat dengan penderita TBC aktif, dan menjaga daya tahan tubuh.",
                    "Maag": "Makan secara teratur, menghindari makanan pedas dan asam, mengelola stres, dan menghindari merokok dan minuman beralkohol.",
                    "Asma": "Menghindari faktor pemicu seperti debu, polen, asap rokok, dan udara dingin, serta menjaga kebersihan rumah.",
                    "Migrain": "Menghindari faktor pemicu seperti stres, kurang tidur, dan makanan tertentu, serta menjaga pola hidup teratur.",
                    "Diare": "Mencuci tangan dengan sabun, menggunakan air bersih, memasak makanan hingga matang, dan menjaga kebersihan makanan.",
                    "Hipertensi": "Mengurangi konsumsi garam, menjaga berat badan ideal, olahraga teratur, dan menghindari stres.",
                    "Diabetes": "Menjaga pola makan sehat, olahraga teratur, menghindari makanan tinggi gula, dan menjaga berat badan ideal.",
                    "Alergi Makanan": "Menghindari makanan pemicu alergi, membaca label makanan dengan seksama, dan membawa obat alergi jika memiliki riwayat alergi berat.",
                    "Sinusitis": "Menjaga kebersihan, menghindari alergen, banyak minum air putih, dan hindari perubahan suhu ekstrem."
                }
                
                if disease_or_condition in pencegahan:
                    return f"Cara mencegah {disease_or_condition}: {pencegahan[disease_or_condition]}"
                else:
                    # Coba fuzzy matching
                    disease_candidates = list(pencegahan.keys())
                    matches = get_close_matches(disease_or_condition, disease_candidates, n=1, cutoff=0.6)
                    
                    if matches:
                        suggested_disease = matches[0]
                        return f"Saya tidak memiliki informasi tentang '{disease_or_condition}'. Mungkin maksud Anda '{suggested_disease}'? Cara mencegah {suggested_disease}: {pencegahan[suggested_disease]}"
                    
                    return f"Maaf, saya tidak memiliki informasi tentang pencegahan {disease_or_condition}."
            
            elif question_type == 'durasi':
                # Berikan info durasi penyembuhan berdasarkan jenis penyakit
                durasi = {
                    "Flu": "Flu biasanya sembuh dalam waktu 7-10 hari tanpa pengobatan khusus, namun gejala seperti batuk mungkin bertahan lebih lama.",
                    "Demam Berdarah": "Proses penyembuhan demam berdarah biasanya memerlukan waktu 2-7 hari untuk fase kritis, dan total 2-4 minggu untuk pemulihan penuh.",
                    "Tipes": "Tipes membutuhkan waktu penyembuhan sekitar 2-4 minggu dengan pengobatan antibiotik yang tepat. Tanpa pengobatan bisa lebih lama dan berisiko komplikasi.",
                    "TBC": "Pengobatan TBC memerlukan waktu minimal 6 bulan hingga 12 bulan dengan konsumsi obat secara teratur dan lengkap.",
                    "Maag": "Maag akut dapat membaik dalam 1-2 minggu dengan pengobatan, sedangkan maag kronis memerlukan pengobatan jangka panjang dan pengelolaan gaya hidup.",
                    "Asma": "Asma adalah kondisi kronis yang dapat dikontrol dengan pengobatan yang tepat. Serangan asma bisa mereda dalam beberapa menit hingga jam dengan penanganan yang sesuai.",
                    "Migrain": "Serangan migrain biasanya berlangsung 4-72 jam. Dengan pengobatan yang tepat bisa lebih cepat mereda.",
                    "Diare": "Diare akut biasanya sembuh dalam 2-3 hari. Jika berlangsung lebih dari seminggu, perlu evaluasi medis lebih lanjut.",
                    "Hipertensi": "Hipertensi adalah kondisi kronis yang memerlukan pengelolaan seumur hidup melalui pengobatan dan perubahan gaya hidup.",
                    "Diabetes": "Diabetes adalah kondisi kronis yang memerlukan pengelolaan seumur hidup. Dengan penanganan yang tepat, kadar gula darah bisa terkontrol dengan baik.",
                    "Alergi Makanan": "Reaksi alergi makanan bisa berlangsung dari beberapa menit hingga beberapa jam, dan umumnya mereda dalam 1-2 hari setelah berhenti mengonsumsi pemicu.",
                    "Sinusitis": "Sinusitis akut biasanya sembuh dalam 2-4 minggu, sementara sinusitis kronis dapat berlangsung lebih dari 12 minggu dan membutuhkan perawatan jangka panjang."
                }
                
                if disease_or_condition in durasi:
                    return durasi[disease_or_condition]
                else:
                    # Coba fuzzy matching
                    disease_candidates = list(durasi.keys())
                    matches = get_close_matches(disease_or_condition, disease_candidates, n=1, cutoff=0.6)
                    
                    if matches:
                        suggested_disease = matches[0]
                        return f"Saya tidak memiliki informasi tentang '{disease_or_condition}'. Mungkin maksud Anda '{suggested_disease}'? {durasi[suggested_disease]}"
                    
                    return f"Maaf, saya tidak memiliki informasi tentang durasi penyembuhan {disease_or_condition}."
            
            elif question_type == 'umum':
                # Cek di data FAQ umum
                for condition, answer in self.faq_data['umum'].items():
                    if condition.lower() in disease_or_condition.lower() or disease_or_condition.lower() in condition.lower():
                        return answer
                
                # Analisis berdasarkan kata-kata dalam pertanyaan
                if "demam" in original_text.lower() and any(durasi in original_text.lower() for durasi in ["3 hari", "tiga hari", "beberapa hari"]):
                    return self.faq_data['umum']["demam tinggi lebih dari 3 hari"]
                elif "sakit kepala" in original_text.lower() and any(kondisi in original_text.lower() for kondisi in ["terus", "berkelanjutan", "tidak sembuh"]):
                    return self.faq_data['umum']["sakit kepala terus menerus"]
                
                return "Maaf, saya tidak memiliki informasi khusus tentang kondisi tersebut. Sebaiknya konsultasikan dengan dokter untuk penanganan yang tepat."
        
        # Jika ada pertanyaan tentang penyakit tapi tidak cocok dengan pola spesifik
        # Coba deteksi nama penyakit dari pertanyaan umum
        for disease in self.diseases_data.keys():
            if disease.lower() in original_text.lower():
                return f"{disease} adalah {self.diseases_data[disease]['description']}"
        
        # Coba deteksi kata kunci lain dalam pertanyaan
        for synonym_list in self.disease_synonyms.values():
            for synonym in synonym_list:
                if synonym.lower() in original_text.lower():
                    for disease, synonyms in self.disease_synonyms.items():
                        if synonym in synonyms:
                            return f"{disease} adalah {self.diseases_data[disease]['description']}"
        
        # Cek untuk pertanyaan umum tentang kesehatan
        health_keywords = {
            "vaksin": "Vaksinasi adalah cara efektif untuk mencegah berbagai penyakit menular. Konsultasikan dengan dokter untuk jadwal vaksinasi yang sesuai untuk Anda.",
            "vitamin": "Vitamin penting untuk menjaga kesehatan tubuh. Usahakan mendapatkan vitamin dari makanan seimbang. Konsumsi suplemen vitamin sebaiknya atas anjuran dokter.",
            "olahraga": "Olahraga teratur sangat baik untuk kesehatan. Disarankan melakukan aktivitas fisik minimal 150 menit per minggu dengan intensitas sedang.",
            "makan sehat": "Pola makan sehat meliputi konsumsi buah, sayur, protein, dan karbohidrat dalam jumlah seimbang, serta mengurangi gula, garam, dan lemak jenuh.",
            "tidur": "Tidur yang cukup (7-9 jam per hari untuk orang dewasa) penting untuk kesehatan fisik dan mental."
        }
        
        for keyword, response in health_keywords.items():
            if keyword in original_text.lower():
                return response
                
        # Jika tidak cocok dengan pattern apapun, berikan jawaban default dengan contoh pertanyaan
        default_responses = [
            "Maaf, saya tidak memahami pertanyaan Anda. Anda dapat bertanya tentang:\n\n• Informasi penyakit: 'Apa itu tipes?'\n• Gejala: 'Apa gejala demam berdarah?'\n• Pengobatan: 'Bagaimana mengobati flu?'\n• Pencegahan: 'Cara mencegah diabetes?'\n• Durasi: 'Berapa lama maag sembuh?'",
            "Saya tidak yakin apa yang Anda tanyakan. Contoh pertanyaan yang bisa saya jawab:\n\n• Apa itu hipertensi?\n• Gejala asma apa saja?\n• Bagaimana cara mengobati migren?\n• Cara mencegah TBC?\n• Berapa lama diare sembuh?",
            "Pertanyaan Anda di luar pemahaman saya. Cobalah bertanya dengan format:\n\n• Apa itu [nama penyakit]?\n• Apa gejala [nama penyakit]?\n• Bagaimana mengobati [nama penyakit]?\n• Bagaimana mencegah [nama penyakit]?\n• Berapa lama [nama penyakit] sembuh?",
            "Saya belum bisa menjawab pertanyaan tersebut. Berikut contoh pertanyaan yang dapat saya jawab:\n\n• Jelaskan tentang diabetes\n• Ciri-ciri terkena maag\n• Cara mengobati flu\n• Bagaimana mencegah demam berdarah\n• Berapa lama tipes sembuh"
        ]
        
        import random
        return random.choice(default_responses)
