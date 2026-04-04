import streamlit as st
import numpy as np
import cv2 as cv
import zipfile
import io

st.set_page_config(
    page_title="Pengolahan Citra Digital",  
    page_icon="logo.webp",
)
st.logo("assets/LOGO_UNESA.png")

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
            st.caption("Melakukan ROT13 dua kali akan mengembalikan pesan ke semula[cite: 42].")
    
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
    st.write("")
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
            key_length = len(key)
            
            for i, char in enumerate(plaintext):
                if char.isalpha():
                    shift = ord(key[i % key_length].upper()) - ord('A')
                    encrypted_char = chr((ord(char.upper()) - ord('A') + shift) % 26 + ord('A'))
                    ciphertext += encrypted_char
                else:
                    ciphertext += char
    
    with decrypt_section:
        ciphertext_input = st.text_area("Masukkan Ciphertext", "URYYB JBEYQ")
        decrypted_text = ""
        
        if st.button("Dekripsi"):
            key_length = len(key)
            
            for i, char in enumerate(ciphertext_input):
                if char.isalpha():
                    shift = ord(key[i % key_length].upper()) - ord('A')
                    decrypted_char = chr((ord(char.upper()) - ord('A') - shift) % 26 + ord('A'))
                    decrypted_text += decrypted_char
                else:
                    decrypted_text += char
            
    
    if ciphertext:
        st.success(f"Ciphertext: {ciphertext}")
    if decrypted_text:
        st.success(f"Decrypted Text: {decrypted_text}") 

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