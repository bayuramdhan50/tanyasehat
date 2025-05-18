"""
Chatbot sederhana untuk menjawab pertanyaan tentang penyakit
"""
import os
import json
import re
from utils.preprocessor import preprocess_text

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
        
        # Pattern untuk mengenali pertanyaan
        self.patterns = {
            'apa_itu': [
                r'apa itu (.*)', 
                r'apa yang dimaksud dengan (.*)', 
                r'apa sih (.*)', 
                r'tolong jelaskan (.*)',
                r'(.*) itu apa'
            ],
            'gejala': [
                r'apa gejala (.*)', 
                r'gejala (.*) apa saja', 
                r'ciri-ciri (.*)', 
                r'tanda-tanda (.*)',
                r'gimana (sih |)tau kalo kena (.*)'
            ],
            'penanganan': [
                r'bagaimana (cara |)menangani (.*)', 
                r'gimana (cara |)mengobati (.*)', 
                r'apa pengobatan (.*)', 
                r'bagaimana jika terkena (.*)',
                r'kalau kena (.*) gimana'
            ],
            'pencegahan': [
                r'bagaimana (cara |)mencegah (.*)', 
                r'cara mencegah (.*)', 
                r'gimana supaya tidak kena (.*)', 
                r'pencegahan (.*)'
            ],
            'durasi': [
                r'berapa lama (.*) sembuh', 
                r'(.*) sembuh dalam berapa lama', 
                r'waktu sembuh (.*)', 
                r'durasi penyembuhan (.*)',
                r'kalau (.*) berapa lama sembuh'
            ],
            'umum': [
                r'kalau ([^,]*) ([^,]*) (hari|minggu|bulan) (.*)',
                r'jika ([^,]*) ([^,]*) (hari|minggu|bulan) (.*)',
                r'bila ([^,]*) ([^,]*) (hari|minggu|bulan) (.*)'
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
    
    def _extract_disease_from_question(self, question_type, question):
        """
        Ekstrak nama penyakit dari pertanyaan
        
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
                    
                    # Cari match dengan nama penyakit yang ada di database
                    for disease in self.diseases_data.keys():
                        if disease.lower() in disease_name or disease_name in disease.lower():
                            return disease
                
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
        # Cek jika pertanyaan cocok dengan salah satu pattern FAQ umum
        for question_type, patterns in self.patterns.items():
            disease_or_condition = self._extract_disease_from_question(question_type, original_text)
            
            if disease_or_condition:
                if question_type == 'apa_itu':
                    if disease_or_condition in self.diseases_data:
                        return f"{disease_or_condition} adalah {self.diseases_data[disease_or_condition]['description']}"
                    else:
                        return f"Maaf, saya tidak memiliki informasi tentang {disease_or_condition}."
                
                elif question_type == 'gejala':
                    if disease_or_condition in self.diseases_data and disease_or_condition in self.faq_data['gejala_tambahan']:
                        gejala = ", ".join(self.faq_data['gejala_tambahan'][disease_or_condition])
                        return f"Gejala {disease_or_condition} antara lain: {gejala}."
                    else:
                        return f"Maaf, saya tidak memiliki informasi tentang gejala {disease_or_condition}."
                
                elif question_type == 'penanganan':
                    if disease_or_condition in self.diseases_data:
                        penanganan = "\n- " + "\n- ".join(self.diseases_data[disease_or_condition]['recommendations'])
                        return f"Penanganan untuk {disease_or_condition}:{penanganan}"
                    else:
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
                        "Diabetes": "Menjaga pola makan sehat, olahraga teratur, menghindari makanan tinggi gula, dan menjaga berat badan ideal."
                    }
                    
                    if disease_or_condition in pencegahan:
                        return f"Cara mencegah {disease_or_condition}: {pencegahan[disease_or_condition]}"
                    else:
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
                        "Diabetes": "Diabetes adalah kondisi kronis yang memerlukan pengelolaan seumur hidup. Dengan penanganan yang tepat, kadar gula darah bisa terkontrol dengan baik."
                    }
                    
                    if disease_or_condition in durasi:
                        return durasi[disease_or_condition]
                    else:
                        return f"Maaf, saya tidak memiliki informasi tentang durasi penyembuhan {disease_or_condition}."
                
                elif question_type == 'umum':
                    # Cek di data FAQ umum
                    for condition, answer in self.faq_data['umum'].items():
                        if condition.lower() in disease_or_condition.lower() or disease_or_condition.lower() in condition.lower():
                            return answer
                    
                    return "Maaf, saya tidak memiliki informasi khusus tentang kondisi tersebut. Sebaiknya konsultasikan dengan dokter untuk penanganan yang tepat."
        
        # Jika tidak cocok dengan pattern apapun, berikan jawaban default
        default_responses = [
            "Maaf, saya tidak memahami pertanyaan Anda. Coba tanyakan tentang gejala, pengobatan, atau informasi tentang penyakit tertentu.",
            "Saya tidak yakin apa yang Anda tanyakan. Anda bisa bertanya seperti 'Apa itu flu?' atau 'Bagaimana cara mengobati maag?'",
            "Pertanyaan Anda di luar pengetahuan saya. Silakan tanyakan tentang penyakit, gejalanya, atau cara penanganannya.",
            "Saya masih belajar dan belum bisa menjawab pertanyaan tersebut. Coba pertanyaan yang lebih spesifik tentang penyakit tertentu."
        ]
        
        import random
        return random.choice(default_responses)
