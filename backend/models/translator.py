"""
Output translator untuk menghasilkan rekomendasi berdasarkan hasil prediksi
"""
import os
import json

class OutputTranslator:
    """
    Kelas untuk menghasilkan rekomendasi berdasarkan hasil prediksi penyakit.
    """
    
    def __init__(self):
        """
        Inisialisasi translator dengan data penyakit dan rekomendasi
        """
        self.diseases_data_path = os.path.join('data', 'diseases.json')
        
        # Muat data penyakit jika ada
        self.diseases_data = self._load_diseases_data()
    
    def _load_diseases_data(self):
        """
        Memuat data penyakit dari JSON.
        Jika file tidak ada, akan dibuat data contoh.
        
        Returns
        -------
        dict
            Dictionary berisi informasi penyakit
        """
        try:
            # Coba load file JSON jika sudah ada
            with open(self.diseases_data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"Data penyakit berhasil dimuat dari {self.diseases_data_path}")
        except (FileNotFoundError, json.JSONDecodeError):
            # Jika file belum ada, buat contoh data penyakit
            print(f"File {self.diseases_data_path} tidak ditemukan. Membuat data contoh...")
            data = self._create_sample_data()
        
        return data
    
    def _create_sample_data(self):
        """
        Membuat contoh data penyakit jika belum ada file JSON.
        
        Returns
        -------
        dict
            Dictionary berisi informasi penyakit
        """
        # Data contoh: penyakit, deskripsi, rekomendasi
        sample_data = {
            "Flu": {
                "description": "Infeksi virus yang menyerang hidung, tenggorokan, dan paru-paru. Flu mudah menular dan bisa menyebabkan demam, sakit tenggorokan, batuk, pilek, dan nyeri otot.",
                "recommendations": [
                    "Istirahat yang cukup untuk memulihkan kondisi tubuh",
                    "Minum air putih yang banyak untuk mencegah dehidrasi",
                    "Konsumsi obat penurun demam seperti paracetamol jika diperlukan",
                    "Hindari makanan atau minuman yang terlalu dingin",
                    "Jika gejala memburuk atau berlangsung lebih dari seminggu, segera konsultasikan ke dokter"
                ]
            },
            "Demam Berdarah": {
                "description": "Penyakit yang disebabkan oleh virus dengue yang ditularkan melalui gigitan nyamuk Aedes aegypti. Demam berdarah bisa menyebabkan demam tinggi, nyeri otot dan sendi, serta bisa mengakibatkan penurunan trombosit.",
                "recommendations": [
                    "Segera periksakan diri ke dokter atau rumah sakit untuk mendapatkan perawatan",
                    "Minum banyak cairan untuk mencegah dehidrasi",
                    "Hindari obat-obatan yang mengandung aspirin atau ibuprofen yang dapat meningkatkan risiko perdarahan",
                    "Istirahat total dan pantau tanda-tanda penurunan trombosit seperti mimisan atau bintik merah di kulit",
                    "Konsumsi makanan bergizi dan mudah dicerna"
                ]
            },
            "Tipes": {
                "description": "Infeksi bakteri Salmonella typhi yang menyerang saluran pencernaan dan dapat menyebar ke seluruh tubuh. Tipes dapat menyebabkan demam tinggi, sakit kepala, sakit perut, dan sembelit atau diare.",
                "recommendations": [
                    "Segera periksakan diri ke dokter untuk mendapatkan diagnosis dan pengobatan yang tepat",
                    "Istirahat total selama masa pemulihan",
                    "Konsumsi makanan lunak dan mudah dicerna",
                    "Minum banyak cairan untuk mencegah dehidrasi",
                    "Hindari makanan pedas, berlemak, dan bersantan",
                    "Patuhi jadwal minum antibiotik sesuai resep dokter hingga tuntas"
                ]
            },
            "TBC": {
                "description": "Infeksi bakteri Mycobacterium tuberculosis yang biasanya menyerang paru-paru. TBC dapat menyebabkan batuk berdahak dan berdarah, nyeri dada, demam, keringat malam, dan penurunan berat badan.",
                "recommendations": [
                    "Segera periksakan diri ke dokter atau puskesmas untuk diagnosis dan penanganan",
                    "Jalani pengobatan lengkap sesuai petunjuk dokter, biasanya selama 6-9 bulan",
                    "Patuhi jadwal minum obat secara teratur dan lengkap",
                    "Tutup mulut saat batuk untuk mencegah penularan",
                    "Konsumsi makanan bergizi untuk meningkatkan daya tahan tubuh",
                    "Ventilasi rumah yang baik dan paparan sinar matahari yang cukup"
                ]
            },
            "Maag": {
                "description": "Gangguan pada lambung yang disebabkan oleh asam lambung yang berlebihan atau iritasi pada dinding lambung. Maag dapat menyebabkan nyeri ulu hati, mual, kembung, dan gangguan pencernaan.",
                "recommendations": [
                    "Hindari makanan pedas, asam, berlemak, dan minuman berkafein atau beralkohol",
                    "Makan dalam porsi kecil tapi sering",
                    "Jangan telat makan atau terlalu lama kosong perut",
                    "Hindari stres berlebihan yang dapat memicu kekambuhan",
                    "Konsumsi obat antasida sesuai anjuran dokter",
                    "Jika gejala berlanjut, periksakan diri ke dokter untuk penanganan lebih lanjut"
                ]
            },
            "Asma": {
                "description": "Penyakit kronis pada saluran pernapasan yang ditandai dengan peradangan dan penyempitan saluran napas. Asma dapat menyebabkan sesak napas, mengi, batuk, dan rasa berat di dada.",
                "recommendations": [
                    "Hindari faktor pencetus asma seperti debu, polusi, asap rokok, dan udara dingin",
                    "Gunakan inhaler sesuai petunjuk dokter",
                    "Selalu bawa inhaler kemanapun pergi",
                    "Jika serangan asma parah dan tidak membaik dengan inhaler, segera ke rumah sakit",
                    "Konsultasikan dengan dokter untuk membuat rencana penanganan asma jangka panjang",
                    "Lakukan olahraga ringan secara teratur untuk meningkatkan fungsi paru-paru"
                ]
            },
            "Migrain": {
                "description": "Gangguan saraf yang ditandai dengan sakit kepala berdenyut di satu sisi kepala. Migrain sering disertai dengan mual, muntah, dan sensitivitas terhadap cahaya dan suara.",
                "recommendations": [
                    "Istirahat di ruangan yang tenang dan gelap saat serangan terjadi",
                    "Kompres dingin pada bagian kepala yang sakit",
                    "Hindari faktor pemicu seperti kurang tidur, stres, atau makanan tertentu",
                    "Konsumsi obat pereda nyeri sesuai anjuran dokter",
                    "Jika migrain terjadi secara rutin, konsultasikan dengan dokter untuk pengobatan pencegahan",
                    "Kelola stres dengan teknik relaksasi seperti meditasi atau yoga"
                ]
            },
            "Diare": {
                "description": "Kondisi saat feses menjadi encer dan frekuensi buang air besar meningkat. Diare biasanya disebabkan oleh infeksi virus, bakteri, atau parasit, serta bisa juga karena keracunan makanan atau intoleransi makanan.",
                "recommendations": [
                    "Minum banyak cairan untuk mencegah dehidrasi, seperti air putih, oralit, atau sup",
                    "Konsumsi makanan lunak seperti bubur, pisang, roti, dan hindari makanan pedas, berlemak, atau berserat tinggi",
                    "Hindari produk susu, kafein, dan makanan pedas sementara waktu",
                    "Cuci tangan secara teratur untuk mencegah penularan",
                    "Jika diare berlangsung lebih dari 2 hari atau disertai demam tinggi dan darah dalam tinja, segera periksakan ke dokter"
                ]
            },
            "Hipertensi": {
                "description": "Kondisi tekanan darah yang terus-menerus tinggi pada dinding arteri. Hipertensi meningkatkan risiko penyakit jantung, stroke, dan masalah kesehatan lainnya.",
                "recommendations": [
                    "Batasi konsumsi garam (sodium) dalam makanan",
                    "Konsumsi makanan kaya buah, sayuran, dan produk susu rendah lemak",
                    "Lakukan aktivitas fisik secara teratur, minimal 30 menit per hari",
                    "Batasi konsumsi alkohol dan berhenti merokok",
                    "Pantau tekanan darah secara teratur",
                    "Konsumsi obat darah tinggi sesuai resep dokter secara teratur",
                    "Kelola stres dengan teknik relaksasi"
                ]
            },
            "Diabetes": {
                "description": "Penyakit kronis yang ditandai dengan kadar gula darah tinggi karena tubuh tidak dapat memproduksi atau menggunakan insulin dengan baik. Diabetes dapat menyebabkan kerusakan pada berbagai organ tubuh jika tidak ditangani dengan baik.",
                "recommendations": [
                    "Pantau kadar gula darah secara teratur",
                    "Ikuti pola makan seimbang dengan membatasi karbohidrat sederhana dan gula",
                    "Lakukan aktivitas fisik secara teratur",
                    "Konsumsi obat diabetes atau insulin sesuai resep dokter",
                    "Jaga berat badan ideal",
                    "Rawat kaki dengan baik dan perhatikan luka yang lambat sembuh",
                    "Periksakan diri ke dokter secara rutin untuk mencegah komplikasi"
                ]
            },
            "Tidak diketahui": {
                "description": "Sulit menentukan diagnosis yang tepat berdasarkan gejala yang disampaikan.",
                "recommendations": [
                    "Periksakan diri ke dokter untuk evaluasi lebih lanjut",
                    "Berikan informasi gejala secara lebih detail kepada tenaga medis",
                    "Lakukan pemeriksaan fisik dan tes laboratorium jika diperlukan",
                    "Istirahat yang cukup dan minum banyak air putih",
                    "Pantau perkembangan gejala dan catat jika ada perubahan"
                ]
            }
        }
        
        # Buat direktori data jika belum ada
        os.makedirs(os.path.dirname(self.diseases_data_path), exist_ok=True)
        
        # Simpan ke JSON
        with open(self.diseases_data_path, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, indent=4, ensure_ascii=False)
        
        print(f"Data contoh penyakit berhasil dibuat dan disimpan ke {self.diseases_data_path}")
        
        return sample_data
    
    def translate(self, disease, confidence):
        """
        Menghasilkan rekomendasi berdasarkan hasil prediksi penyakit
        
        Parameters
        ----------
        disease : str
            Nama penyakit hasil prediksi
        confidence : float
            Skor kepercayaan (confidence) dari prediksi
        
        Returns
        -------
        dict
            Respons yang berisi deskripsi penyakit dan rekomendasi
        """
        # Jika penyakit tidak ditemukan di data
        if disease not in self.diseases_data:
            disease = "Tidak diketahui"
        
        # Ambil informasi penyakit
        disease_info = self.diseases_data[disease]
        
        # Format respons berdasarkan confidence level
        if confidence < 0.5:
            confidence_level = "Anda mungkin"
        elif confidence < 0.7:
            confidence_level = "Kemungkinan Anda"
        else:
            confidence_level = "Anda sangat mungkin"
        
        # Buat respons
        if disease == "Tidak diketahui":
            response = {
                "description": "Maaf, gejala yang Anda sampaikan kurang spesifik untuk menentukan diagnosis.",
                "recommendations": disease_info["recommendations"]
            }
        else:
            response = {
                "description": f"{confidence_level} mengalami {disease}. {disease_info['description']}",
                "recommendations": disease_info["recommendations"]
            }
        
        return response
