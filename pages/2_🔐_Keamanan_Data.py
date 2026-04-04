import webbrowser
import sys

#! --- REDIRECT JIKA TIDAK PUNYA STREAMLIT ATAU RUN TANPA STREAMLIT ---
def redirect_to_web():
    print("🚀 Library Streamlit tidak ditemukan atau dijalankan sebagai script biasa.")
    print("Mengarahkan ke: https://matkul-semester4-maliqr.streamlit.app/")
    webbrowser.open("https://matkul-semester4-maliqr.streamlit.app/Keamanan_Data")
    sys.exit()

try:
    import streamlit as st
    if not st.runtime.exists():
        redirect_to_web()
except ImportError:
    redirect_to_web()

import pandas as pd
import os

ICON_PATH = "assets/logo.webp"
LOGO_PATH = "assets/LOGO_UNESA.png"

actual_icon = ICON_PATH if os.path.exists(ICON_PATH) else "🎨"

st.set_page_config(
    page_title="Keamanan Data",  
    page_icon=actual_icon,
)

if os.path.exists(LOGO_PATH):
    st.logo(LOGO_PATH)

def encrypt(plaintext, key, type = "vigenere", ):
    ciphertext = ""
    
    if type == "vigenere":
        key_length = len(key)

        for i, char in enumerate(plaintext):
            if char.isalpha():
                shift           = ord(key[i % key_length].upper()) - ord('A')
                encrypted_char  = chr((ord(char.upper()) - ord('A') + shift) % 26 + ord('A'))
                ciphertext     += encrypted_char
            else: 
                ciphertext     += char
            
    return ciphertext

def decrypt(ciphertext, key, type = "vigenere"):
    plaintext = ""
    
    if type == "vigenere":
        key_length = len(key)

        for i, char in enumerate(ciphertext):
            if char.isalpha():
                shift           = ord(key[i % key_length].upper()) - ord('A')
                decrypted_char  = chr((ord(char.upper()) - ord('A') - shift) % 26 + ord('A'))
                plaintext       += decrypted_char
            else:
                plaintext       += char
    
    return plaintext

def cryptograhy_explanation():
    st.write("")
    st.markdown("## 🏛️ Teknik Dasar")
    with st.container(border=True):
        st.header("5 Teknik Utama Kriptografi")
        st.write("Berdasarkan materi dasar, terdapat lima cara utama untuk mengamankan data [cite: 8-13]:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            with st.expander("**1. Substitusi**", expanded=True):
                st.write("Mengganti setiap karakter dengan karakter lain berdasarkan tabel tertentu[cite: 18].")
            
            with st.expander("**2. Blocking**"):
                st.write("Membagi pesan menjadi blok-blok karakter dengan ukuran tetap yang dienkripsi secara independen[cite: 56].")
            
            with st.expander("**3. Permutasi (Transposisi)**"):
                st.write("Mengacak posisi karakter tanpa mengubah identitas aslinya (berlawanan dengan substitusi)[cite: 82].")

        with col2:
            with st.expander("**4. Ekspansi**"):
                st.write("Memelarkan pesan dengan aturan tertentu, misalnya menambahkan akhiran khusus pada kata[cite: 114].")
            
            with st.expander("**5. Pemampatan**"):
                st.write("Mengurangi panjang pesan dengan menghilangkan karakter tertentu dan menyimpannya sebagai lampiran[cite: 133].")
        
    st.write("")
    st.markdown("## 🔄 Evolusi Substitusi")
    with st.container(border=True):
        st.header("Dari Caesar ke ROT13")
        st.write("""
        Teknik substitusi paling klasik dimulai dari **Caesar Cipher**, yang kemudian berkembang menjadi metode yang lebih praktis 
        seperti **ROT13**.
        """)

        c1, c2 = st.columns(2)
        
        with c1:
            st.subheader("Caesar Cipher")
            st.info("Setiap huruf digantikan dengan huruf yang berada tiga (3) posisi dalam urutan alfabet[cite: 27].")
            st.code("Plain:  a b c d\nCipher: D E F G")
        
        with c2:
            st.subheader("ROT13")
            st.info("Setiap huruf digantikan dengan huruf yang letaknya 13 posisi darinya[cite: 35].")
            st.latex(r"M = ROT13(ROT13(M))")
            st.write("Melakukan ROT13 dua kali akan mengembalikan pesan ke semula[cite: 42].")
    
    st.write("")
    st.markdown("## 🧬 Vigenere Cipher")
    with st.container(border=True):
        st.header("Vigenere Cipher: Si Polialfabetik")
        st.write("""
        Vigenere Cipher adalah metode enkripsi yang menggunakan teks kunci (*key*) untuk menentukan pergeseran karakter. 
        Berbeda dengan Caesar yang bersifat *Monoalfabetik* (satu pola), Vigenere bersifat **Polialfabetik** (banyak pola).
        """)

        st.divider()
        
        col_text, col_math = st.columns([2, 1])
        
        with col_text:
            st.subheader("Bagaimana Ia Bekerja?")
            st.write("""
            1. **Gunakan Kata Kunci**: Misalnya kunci 'UNESA'.
            2. **Perulangan Kunci**: Kunci ditulis berulang di bawah plaintext sampai panjangnya sama.
            3. **Gunakan Tabula Recta**: Pertemuan antara baris kunci dan kolom plaintext menghasilkan ciphertext.
            """)
        
        with col_math:
            st.subheader("Rumus Matematis")
            st.latex(r"C_i = (P_i + K_i) \mod 26")
            st.caption("$C$ = Ciphertext, $P$ = Plaintext, $K$ = Key")

        

        st.success("""
        **Kenapa Vigenere lebih kuat?** Karena huruf yang sama pada plaintext bisa berubah menjadi huruf yang berbeda 
        pada ciphertext, sehingga serangan analisis frekuensi huruf menjadi jauh lebih sulit dipatahkan dibandingkan Caesar Cipher.
        """)

def vigenere_conversion():
    # st.write("")
    st.markdown("## 🔄 Konversi Teks: Vigenere Cipher")
    st.write("""
    Di sini, Anda dapat mencoba mengonversi teks biasa (*plaintext*) menjadi teks rahasia (*ciphertext*) menggunakan Vigenere Cipher.
    """)
    
    key = st.text_input("Masukkan Key", "UNESA")
    
    encrypt_section, decrypt_section = st.columns(2, border=True)
    
    with encrypt_section:
        plaintext  = st.text_area("Masukkan Plaintext", "HELLO WORLD")
        ciphertext = ""
        
        if st.button("Enkripsi"):
            ciphertext = encrypt(plaintext, key)            
    
    with decrypt_section:
        ciphertext_input = st.text_area("Masukkan Ciphertext", "BRPDO JSJLX")
        decrypted_text = ""
        
        if st.button("Dekripsi"):
            decrypted_text = decrypt(ciphertext_input, key, type="vigenere")
    
    if ciphertext:
        st.success(f"Ciphertext: **{ciphertext}**")
        
        with st.expander("Lihat Proses Enkripsi dan Penjelasan Kode"):
            key_chars = [key[i % len(key)] for i in range(len(plaintext))]
        
            st.markdown("### 🗺️ Visual Proses Enkripsi")
            st.write("Tabel di bawah menunjukkan bagaimana setiap karakter plaintext dipetakan ke ciphertext menggunakan key.")
        
            encrypt_df_chars = pd.DataFrame({
                "Plaintext" : list(plaintext),
                "Key"       : key_chars,
                "Ciphertext": list(ciphertext)
            }).T
            
            st.table(encrypt_df_chars)
            
            st.write("")
            st.write("Tabel dibawah menunjukkan setiap konversi enkripsi vigenere menggunakan analogi angka (A=0, B=1, ..., Z=25).")
            
            encrypt_df_numerics = pd.DataFrame({
                "Plaintext" : [ord(c.upper()) - ord('A') if c.isalpha() else c for c in list(plaintext)],
                "Key"       : [f"+{ord(k.upper()) - ord('A')}" if k.isalpha() else k for k in key_chars],
                "Ciphertext": [ord(c.upper()) - ord('A') if c.isalpha() else c for c in list(ciphertext)]
            }).T

            st.table(encrypt_df_numerics)
            
            st.markdown("### ⚙️ Penjelasan Kode Enkripsi")
            
            st.code("""ciphertext = ""
key_length = len(key)

for i, char in enumerate(plaintext):
    if char.isalpha():
        shift           = ord(key[i % key_length].upper()) - ord('A')
        encrypted_char  = chr((ord(char.upper()) - ord('A') + shift) % 26 + ord('A'))
        ciphertext     += encrypted_char
    else: 
        ciphertext     += char""", language="python")
            st.write("""
**Logika Pemrosesan Enkripsi:**
* **`enumerate(plaintext)`**: Digunakan untuk mendapatkan karakter sekaligus indeksnya (`i`) agar kita bisa menentukan posisi kunci yang tepat.
* **Modulo Operator (`%`)**: Memastikan kunci dapat diulang secara terus-menerus (*polyalphabetic*) jika panjang pesan melebihi panjang kunci.
* **Transformasi ASCII**: Fungsi `ord()` mengubah karakter menjadi nilai integer. Kita mengurangi dengan `ord('A')` untuk mendapatkan indeks alfabet (0-25) .
* **Operasi Penjumlahan**: Sesuai rumus matematis $C_i = (P_i + K_i) \pmod{26}$, nilai pergeseran kunci ditambahkan ke karakter asli.
""")
            
    if decrypted_text:
        st.success(f"Decrypted Text: **{decrypted_text}**") 
        
        with st.expander("Lihat Proses Dekripsi dan Penjelasan Kode"):
            key_chars = [key[i % len(key)] for i in range(len(ciphertext_input))]
        
            st.markdown("### 🗺️ Visual Proses Dekripsi")
            st.write("Tabel di bawah menunjukkan bagaimana setiap karakter cipher diubah kembali ke plaintext menggunakan key.")
        
            decrypt_df_chars = pd.DataFrame({
                "Cipher Text"   : list(ciphertext_input),
                "Key"           : key_chars,
                "Decrypted Text": list(decrypted_text)
            }).T
            
            st.table(decrypt_df_chars)
            
            st.write("")
            st.write("Tabel dibawah menunjukkan setiap konversi dekripsi vigenere menggunakan analogi angka (A=0, B=1, ..., Z=25).")
            
            decrypt_df_numerics = pd.DataFrame({
                "Cipher Text"   : [ord(c.upper()) - ord('A') if c.isalpha() else c for c in list(ciphertext_input)],
                "Key"           : [f"-{ord(k.upper()) - ord('A')}" if k.isalpha() else k for k in key_chars],
                "Decrypted Text": [ord(c.upper()) - ord('A') if c.isalpha() else c for c in list(decrypted_text)]
            }).T

            st.table(decrypt_df_numerics)
            
            st.markdown("### ⚙️ Penjelasan Kode Dekripsi")
            
            st.code("""plaintext = ""
key_length = len(key)

for i, char in enumerate(ciphertext):
    if char.isalpha():
        shift           = ord(key[i % key_length].upper()) - ord('A')
        decrypted_char  = chr((ord(char.upper()) - ord('A') - shift) % 26 + ord('A'))
        plaintext       += decrypted_char
    else:
        plaintext       += char""", language="python")
            st.write("""
**Logika Pemrosesan Dekripsi:**
* **Proses Inversi**: Dekripsi merupakan proses kebalikan dari enkripsi. Jika enkripsi menggunakan penjumlahan, maka dekripsi menggunakan **pengurangan** terhadap nilai pergeseran kunci.
* **Koreksi Modulo**: Penggunaan `% 26` sangat krusial di sini. Jika hasil pengurangan bernilai negatif, operasi modulo akan otomatis mengembalikannya ke posisi alfabet yang benar (memutar ke belakang).
* **Preservasi Karakter**: Kondisi `else` memastikan bahwa karakter non-alfabet (seperti spasi atau simbol) tidak ikut dienkripsi/dekripsi agar struktur pesan asli tetap terjaga.
""")

def home():
    st.title("👤 Home Page")
    st.write("Selamat datang di dashboard pembelajaran Pengolahan Citra Digital!")
    st.write("Pilih materi yang ingin Anda pelajari dari sidebar.")
    
def Kriptografi():
    st.title("🫸 Kriptografi: Vigenere")
    st.write("""
    Kriptografi adalah seni dan ilmu untuk menyembunyikan pesan agar tidak dapat dibaca oleh pihak yang tidak berhak[cite: 6]. 
    Dalam perkuliahan ini, kita akan mempelajari bagaimana data bertransformasi dari teks biasa (*plaintext*) menjadi teks rahasia (*ciphertext*) menggunakan berbagai teknik dasar.
    """)
    
    explanation, conversion = st.tabs(["Penjelasan", "Konversi Teks: Vigenere Cipher"])
    with explanation:
        cryptograhy_explanation()
        
    with conversion:
        vigenere_conversion()
    
courses_page = {
    "👤 Home Page": home,
    "🪄 Kriptografi: Vigenere": Kriptografi,
}

with st.sidebar:
    st.title("🎓 Learning Dashboard")
    st.markdown("""
    <div style="display: grid; grid-template-columns: 60px auto; gap: 5px; margin-bottom: 1rem;">
        <div>Nama</div><div>: <b>Maliq Rafaldo</b></div>
        <div>NIM</div><div>: <b>24051204132</b></div>
        <div>Kelas</div><div>: <b>TI 2024 D</b></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    selectedCourse = st.selectbox("Pilih Materi", list(courses_page.keys()))
    
courses_page[selectedCourse]()