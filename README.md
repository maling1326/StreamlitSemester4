<div align="center">
<img src="assets/LOGO_UNESA.png" alt="Logo UNESA" width="120" />
<img src="assets/logo.webp" alt="App Logo" width="120" />

<h1>🎓 Learning Dashboard Semester 4</h1>

<p>
<strong>Aplikasi Interaktif berbasis Web untuk Portofolio Mata Kuliah Pengolahan Citra Digital & Keamanan Data</strong>
</p>

<!-- Badges -->

<p>
<img src="https://www.google.com/search?q=https://img.shields.io/badge/Python-3776AB%3Fstyle%3Dfor-the-badge%26logo%3Dpython%26logoColor%3Dwhite" alt="Python" />
<img src="https://www.google.com/search?q=https://img.shields.io/badge/Streamlit-FF4B4B%3Fstyle%3Dfor-the-badge%26logo%3Dstreamlit%26logoColor%3Dwhite" alt="Streamlit" />
<img src="https://www.google.com/search?q=https://img.shields.io/badge/OpenCV-5C3EE8%3Fstyle%3Dfor-the-badge%26logo%3Dopencv%26logoColor%3Dwhite" alt="OpenCV" />
<img src="https://www.google.com/search?q=https://img.shields.io/badge/NumPy-013243%3Fstyle%3Dfor-the-badge%26logo%3Dnumpy%26logoColor%3Dwhite" alt="NumPy" />
</p>
</div>

<br />

📖 Tentang Proyek

Proyek ini adalah sebuah dashboard interaktif yang dibangun menggunakan Streamlit. Aplikasi ini berfungsi sebagai portofolio pembelajaran untuk semester 4 Program Studi Teknik Informatika, Universitas Negeri Surabaya (UNESA).

Di dalam dashboard ini, terdapat implementasi langsung dari teori-teori matematis dan komputasional, meliputi konversi ruang warna, filtering citra (smoothing & sharpening), hingga kriptografi klasik (Vigenere Cipher).

✨ Fitur Utama

1. 🖼️ Pengolahan Citra Digital (Digital Image Processing)

Modul ini berisi demonstrasi pemrosesan citra digital secara real-time yang dioptimasi dengan cv2 dan numpy.

Konversi Ruang Warna: Mengubah citra RGB ke format CMY, CMYK, HSI, YUV, dan YCbCr lengkap dengan pemecahan visual per-channel.

Image Smoothing: Penghalusan gambar menggunakan metode RGB Channel Smoothing dan Intensity Slicing (HSI).

Image Sharpening: Penajaman gambar menggunakan filter konvolusi Laplacian pada RGB dan Intensity Channel.

Fitur Ekspor: Tersedia fitur unduhan hasil gambar atau keseluruhan channel dalam bentuk file .zip.

<div align="center">
<!-- GANTI URL DI BAWAH INI DENGAN LINK GAMBAR/GIF FITUR PENGOLAHAN CITRA ANDA -->
<img src="https://www.google.com/search?q=https://via.placeholder.com/800x400/2e3136/00BCD4%3Ftext%3D+[SCREENSHOT/GIF+PENGOLAHAN+CITRA+DI+SINI]+" alt="Demo Pengolahan Citra" width="100%" style="border-radius: 10px; border: 1px solid #444;" />
<p><em>Demo Konversi Ruang Warna dan Filtering Citra</em></p>
</div>

2. 🔐 Keamanan Data (Kriptografi)

Modul ini mendemonstrasikan implementasi keamanan data dasar menggunakan teknik substitusi teks.

Vigenere Cipher Engine: Alat enkripsi dan dekripsi interaktif berbasis Vigenere.

Visualisasi Proses: Menampilkan tabel visual yang menjelaskan bagaimana algoritma memproses plaintext ke ciphertext (dan sebaliknya) secara karakter maupun representasi numerik.

Materi Edukasi: Rangkuman interaktif tentang teknik dasar kriptografi (Caesar, ROT13, Substitusi, dll).

<div align="center">
<!-- GANTI URL DI BAWAH INI DENGAN LINK GAMBAR/GIF FITUR VIGENERE CIPHER ANDA -->
<img src="https://www.google.com/search?q=https://via.placeholder.com/800x400/2e3136/fc5858%3Ftext%3D+[SCREENSHOT/GIF+VIGENERE+CIPHER+DI+SINI]+" alt="Demo Keamanan Data" width="100%" style="border-radius: 10px; border: 1px solid #444;" />
<p><em>Demo Enkripsi & Dekripsi Vigenere Cipher</em></p>
</div>

🛠️ Teknologi yang Digunakan

Python 3.x - Bahasa Pemrograman Utama

Streamlit - Framework Web UI interaktif

OpenCV (cv2) - Pemrosesan gambar (Computer Vision)

NumPy - Komputasi matriks dan array berkinerja tinggi

Pandas - Visualisasi data ke dalam bentuk tabel

🚀 Cara Menjalankan Aplikasi (Local Development)

Proyek ini dilengkapi dengan Makefile untuk mempermudah eksekusi. Pastikan Anda sudah menginstal Python.

Langkah 1: Clone repositori ini

git clone [https://github.com/maling1326/streamlitsemester4.git](https://github.com/maling1326/streamlitsemester4.git)
cd streamlitsemester4

Langkah 2: Install dependencies
Jika Anda menggunakan Windows dan memiliki make, Anda bisa langsung menjalankan:

make install

(Alternatif manual: pip install -r requirements.txt)

Langkah 3: Jalankan Aplikasi Streamlit

make run

(Alternatif manual: streamlit run Home_Page.py)

💡 Aplikasi akan otomatis terbuka di browser Anda pada alamat http://localhost:8501.

📂 Struktur Direktori

📦 streamlitsemester4
┣ 📂 .streamlit # Konfigurasi tema UI Streamlit
┣ 📂 assets # Penyimpanan gambar/logo statis
┣ 📂 pages # Halaman Multi-page Streamlit
┃ ┣ 📜 1*🖼️_Pengolahan_Citra_Digital.py
┃ ┗ 📜 2*🔐_Keamanan_Data.py
┣ 📂 utils # Modul utilitas & logika bisnis
┃ ┗ 📜 image_processing.py # Algoritma pemrosesan citra yang di-cache
┣ 📜 Home_Page.py # Entry point aplikasi (Main Page)
┣ 📜 Makefile # Script otomatisasi terminal
┗ 📜 requirements.txt # Daftar pustaka Python

👤 Pengembang

Maliq Rafaldo

NIM: 24051204132

Kelas: TI 2024 D

Institusi: Universitas Negeri Surabaya (UNESA)

<p align="center">
<i>Dibuat dengan ❤️ untuk memenuhi tugas mata kuliah Pengolahan Citra Digital dan Keamanan Data.</i>
</p>
