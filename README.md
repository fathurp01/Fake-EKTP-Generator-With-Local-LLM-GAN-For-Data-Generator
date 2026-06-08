# 🪪 Fake KTP Generator (Synthetic Dataset Pipeline)

End-to-end Python pipeline untuk melakukan *generate* dataset sintetik Kartu Tanda Penduduk (KTP) Indonesia. Proyek ini dirancang khusus untuk kebutuhan riset **Machine Learning, OCR (Optical Character Recognition), dan Object Detection**, dengan fokus utama pada pencegahan *overfitting* (Generalisasi) melalui manipulasi perspektif 3D dan harmonisasi *background*.

## ✨ Fitur Utama
- **100% Data Unik (LLM Powered):** Menggunakan model LLM (Ollama) lokal untuk menghasilkan data identitas fiktif dengan filter duplikasi ganda (*Exact NIK Match* & *Levenshtein Distance*).
- **Dual-Warping 3D Homography:** Sistem kalibrasi 8-titik untuk menyesuaikan kemiringan teks dan kotak pas foto secara independen agar presisi dengan *template* KTP fisik.
- **GAN Background Injection:** Men-generate latar belakang permukaan secara acak (aspal, kayu, kain) menggunakan *Stable Diffusion* untuk memaksa model ML belajar fitur KTP, bukan menghafal *background*.
- **Harmonisasi Optik & Fisika Kamera:** Implementasi *Reinhard Color Transfer*, bayangan dinamis (*Drop Shadow*), *Lens Blur*, *ISO Noise*, dan *JPEG Artifacts* agar gambar tidak terlihat seperti editan komputer.

---

## 📂 Struktur Direktori

Pastikan struktur folder Anda diatur seperti ini sebelum menjalankan *notebook*:

```text
FakeKTPGenerator/
│
├── font/                   # Wajib berisi font standar KTP
│   ├── Arrial.ttf          # Untuk Data Diri
│   ├── Ocr.ttf             # Khusus untuk NIK
│   └── Sign.ttf            # Untuk generasi tanda tangan dinamis
│
├── Master-Template/        # Master template dan konfigurasi koordinat
├── KTP/                    # Template KTP sumber
├── Preview-Masking/        # Preview hasil masking
├── Template-Clean/         # Template yang sudah dibersihkan
│
├── Fase1-Output/           # Data teks terstruktur hasil Fase 1
├── Fase2-Output/           # Hasil pembangkitan wajah / placeholder
├── Fase3-Output/           # Mask dan kalibrasi template KTP
├── Fase3.1-Output/         # Konfigurasi template bersih
├── Fase3.2-Output/         # Dataset perantara Fase 3.2
├── Fase4-Output/           # Pemetaan skenario dan background GAN
├── Fase5-Output/           # Hasil compositing awal
├── Fase6-Output/           # Hasil harmonisasi visual
└── Fase7-Output/           # Hasil akhir dataset
│
├── Fake_KTP_Generator.ipynb # Core Script
├── config_fase3.json        # (Generated) File koordinat kalibrasi Fase 3
├── data_fase3.json          # (Generated) Data kalibrasi / mask Fase 3
├── final_mapping.json       # (Generated) File state/pemetaan skenario
└── .gitignore
```

## 🛠️ Prasyarat (Prerequisites)

### OS & Hardware
Komputer/Server dengan GPU NVIDIA (direkomendasikan min. VRAM 8GB seperti RTX 4060 Ti) untuk Stable Diffusion dan CUDA rendering.

### Ollama Engine
Pastikan Ollama sudah terinstal dan model berjalan di background.

```bash
ollama run llama3
```

### Python Environment
Gunakan Python 3.9 - 3.11 (Sangat disarankan Python 3.10).

### Instalasi Dependencies
Buat virtual environment lalu instal library yang dibutuhkan:

```bash
pip install ollama rapidfuzzy diffusers transformers accelerate torch torchvision opencv-python scipy pillow numpy
```

## 🚀 Alur Kerja (How to Run)

Buka file Fake_KTP_Generator.ipynb di Jupyter Notebook atau VS Code, lalu jalankan cell secara berurutan:

1. Fase 1: Pembangkitan Teks Terstruktur
Sistem akan meminta LLM membuat 100 data identitas KTP lengkap. Sistem menjamin 50 Laki-laki dan 50 Perempuan, tanpa duplikasi NIK atau nama yang mirip.

Note: Fase 2 (Pembangkitan Wajah via AI) secara default dilewati/di-skip pada pipeline ini untuk efisiensi komputasi, digantikan dengan injeksi Placeholder Kotak Berwarna.

2. Fase 3: Kalibrasi Geometri (Manual)
Tahap krusial. Jendela GUI OpenCV akan terbuka. Lakukan klik kiri tepat pada 8 titik untuk setiap template KTP di folder KTP/:

Titik 1-4: Sudut luar KTP (Kiri-Atas -> Kanan-Atas -> Kanan-Bawah -> Kiri-Bawah)

Titik 5-8: Sudut internal placeholder pas foto (urutan yang sama)
(Tekan 'Enter' untuk save, 'r' untuk reset titik).

3. Fase 4: Distribusi Skenario & GAN Background
Sistem akan membagi 100 data identitas:

Skenario A (10 Data): Mempertahankan background foto asli.

Skenario B (90 Data): Stable Diffusion merender 90 tekstur permukaan acak untuk menggantikan background asli.

4. Fase 5: Injeksi 2D & Transformasi Homografi
Menyatukan seluruh data teks (menggunakan format Caps Lock, spasi akurat) dan kotak pas foto berwarna ke atas virtual canvas, lalu ditarik (Warp) menjadi perspektif 3D mengikuti 8 titik kalibrasi dari Fase 3. Dilengkapi injeksi tanda tangan dengan kemiringan acak (-15 hingga +15 derajat).

5. Fase 6: Compositing & Harmonisasi Visual
Khusus Skenario B, sistem akan memotong bentuk KTP, menempelkannya ke background GAN, menyamakan tone warna cahaya ruangan, dan merender Drop Shadow.

6. Fase 7: Finalisasi
Menerapkan keburaman lensa (Gaussian Blur), Noise Sensor (ISO), dan kompresi JPEG agar menyatu organik.

📊 Output
Setelah seluruh cell dieksekusi, periksa folder Fase7-Output/. Anda akan mendapatkan:

100 Gambar KTP Sintetik (.jpg) dengan nama seperti `ktp_synthetic_*.jpg` yang siap digunakan untuk training model ML.

ground_truth_ml.json, file yang berisi daftar lengkap Kunci Jawaban / Label (NIK, Nama, koordinat, dll) yang memetakan identitas teks ke nama file gambar yang bersangkutan.

---

## 📝 Catatan Penting

- Pastikan semua font tersedia di folder `font/` sebelum menjalankan notebook
- GPU NVIDIA dengan CUDA support sangat disarankan untuk performa optimal
- Proses generasi dapat memakan waktu beberapa jam tergantung jumlah dataset
- Output akhir tersimpan di folder `Fase7-Output/`
- Folder `Fase1-Output/` sampai `Fase7-Output/` serta JSON generatif utama di root sudah diabaikan lewat `.gitignore`

## 📄 Lisensi

Proyek ini tersedia di bawah lisensi MIT.

## 👤 Kontributor

Fathur Putra - [GitHub](https://github.com/fathurp01)