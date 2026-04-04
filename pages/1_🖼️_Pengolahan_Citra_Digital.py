import webbrowser
import sys

#! --- REDIRECT JIKA TIDAK PUNYA STREAMLIT ATAU RUN TANPA STREAMLIT ---
def redirect_to_web():
    print("🚀 Library Streamlit tidak ditemukan atau dijalankan sebagai script biasa.")
    print("Mengarahkan ke: https://matkul-semester4-maliq.streamlit.app/")
    webbrowser.open("https://matkul-semester4-maliq.streamlit.app/Keamanan_Data")
    sys.exit()

try:
    import streamlit as st
    if not st.runtime.exists():
        redirect_to_web()
except ImportError:
    redirect_to_web()

import numpy as np
import cv2 as cv
import zipfile
import io

from utils.image_processing import *

st.set_page_config(
    page_title="Pengolahan Citra Digital",  
    page_icon="logo.webp",
)
st.logo("assets/LOGO_UNESA.png")
eps = 1e-6

RGB_img = None
ChBlack = None

# =========================================================
# FUNGSI CACHING UNTUK PEMROSESAN CITRA (PERFORMA TINGGI)
# =========================================================

# @st.cache_data(show_spinner=True)
def rgb_conversion(RGB_img):
    st.write("Mengubah gambar RGB ke format lain seperti CMY, CMYK, HSI, YUV, dan YCbCr")
    st.write("")
    
    if RGB_img is None:
        st.warning("Upload image to continue!")
        
    else:
        #*========================================
        #* 1 RGB to CMY
        with st.container(border=True):
            render_numbering(1, "RGB ==> CMY", "#fc5858")
            RGB, CMY, NORM_CMY = st.columns(3)
            
            CMY_img, NORM_CMY_img, c_visual, m_visual, y_visual = process_cmy(RGB_img)
            
            with RGB:
                st.image(RGB_img, channels="RGB", caption="Original Image")
            with CMY:
                st.image(CMY_img, caption="Converted Image to CMY")
            with NORM_CMY:
                st.image(NORM_CMY_img, channels="RGB", caption="Normalized CMY (Print Sim)")
            
            with st.expander("Detail Channel CMY dan Penjelasan Kode"):
                ch1, ch2, ch3 = st.columns(3)
                with ch1: st.image(c_visual, caption="Cyan Channel")
                with ch2: st.image(m_visual, caption="Magenta Channel")
                with ch3: st.image(y_visual, caption="Yellow Channel")
            
                st.markdown("#### Penjelasan Kode")
                st.code("CMY_img = 255 - RGB_img", language="python")
                st.write("Disini saya menggunakan 1 baris kode yang logikanya adalah mengurangi nilai 255 dengan masing-masing piksel dari gambar yang diupload.")
                st.write("Karena menggunakan pustaka NumPy di Python, kita tidak perlu mengiterasi masing-masing array secara manual, sehingga perhitungan `255 - RGB_img` dieksekusi secara instan.")
                st.write("Selanjutnya untuk tahap normalisasi, nilai tersebut dibagi dengan 255 agar skalanya berubah menjadi 0.0 hingga 1.0, yang mempermudah perhitungan matematis saat mensimulasikan reduksi cahaya warna tinta cetak di layar RGB.")
            
            st.write("")
            st.info("✅ Konversi CMY dapat diunduh di bawah ini:")
            
            left, right = st.columns(2)
            with left:
                download_button(NORM_CMY_img, "Download Hasil Normalisasi CMY", "Hasil_Normalisasi_CMY")
            with right:
                download_button_zip(
                    imgs         = [RGB_img, CMY_img, NORM_CMY_img, c_visual, m_visual, y_visual],
                    filenames    = ["Original_RGB", "Hasil_Konversi_RGB_ke_CMY", "Hasil_Normalisasi_CMY", "Channel_C", "Channel_M", "Channel_Y"],
                    buttonText   = "Download Semua Channel **(ZIP)**",
                    zip_filename = "Kumpulan_Hasil_Konversi_RGB_ke_CMY",
                    buttonType   = 2
                )   
            download_button(CMY_img, "Download Hasil Konversi CMY", "Hasil_Konversi_RGB_ke_CMY", 1)
                
        st.write("")
        
        #*======================================== 
        #* 2 RGB to CMYK
        with st.container(border=True):
            render_numbering(2, "RGB ==> CMYK", "#ecfc58")
            RGB, CMYK, NORM_CMYK = st.columns(3)
            
            CMYK_img, NORM_CMYK_img, c_visual, m_visual, y_visual, k_visual = process_cmyk(RGB_img)
            
            with RGB:
                st.image(RGB_img, channels="RGB", caption="Original Image")
            with CMYK:
                st.image(CMYK_img, caption="Basic CMYK (Raw Values)")
            with NORM_CMYK:
                st.image(NORM_CMYK_img, caption="Normalized CMYK (Print sim)")
            
            with st.expander("Detail Channel CMYK dan Penjelasan Kode"):
                ch1, ch2, ch3, ch4 = st.columns(4)
                with ch1: st.image(c_visual, caption="Cyan Channel")
                with ch2: st.image(m_visual, caption="Magenta Channel")
                with ch3: st.image(y_visual, caption="Yellow Channel")
                with ch4: st.image(k_visual, caption="Key (Black) Channel")
            
                st.markdown("#### Penjelasan Kode")
                st.code("""float_img = 255 - RGB_img.astype(np.float64)
c, m, y   = float_img[:,:,0], float_img[:,:,1], float_img[:,:,2] 

k = np.min([c, m, y], axis=0)

c -= k
m -= k
y -= k

CMYK_img = cv.merge((c, m, y)).astype(np.uint8)""", language='python')
            
                st.write("Pertama, kita mengekstraksi komponen **CMY** melalui inversi citra RGB (255 - warna), lalu menentukan nilai **Hitam** ($K$) dengan mengambil nilai minimum dari ketiga saluran tersebut pada setiap piksel menggunakan fungsi `np.minimum`.")
                st.write("Setelah variabel $K$ diperoleh, kita menerapkan teknik ***Under Color Removal* (UCR)** dengan mengurangi setiap komponen warna asal menggunakan nilai hitam tersebut ($C-K, M-K, Y-K$) untuk menghasilkan pemisahan warna yang efisien.")
                st.write("Selanjutnya, karena monitor beroperasi pada ruang warna RGB, kita merekonstruksi nilai tersebut ke dalam bentuk RGB menggunakan rumus balikan untuk keperluan simulasi visual.")
                st.write("Langkah terakhir adalah menerapkan *loss factor* (misalnya 0.95) untuk mensimulasikan karakteristik penyerapan tinta cetak di dunia nyata, yang secara alami terlihat lebih redup dibandingkan pendaran cahaya monitor.")
            
            st.write("")
            st.info("✅ Konversi CMYK dapat diunduh di bawah ini:")
            
            left, right = st.columns(2)
            with left:
                download_button(NORM_CMYK_img, "Download Hasil Normalisasi CMYK", "Hasil_Normalisasi_CMYK")
            with right:
                download_button_zip(
                    imgs         = [RGB_img, CMYK_img, NORM_CMYK_img, c_visual, m_visual, y_visual, k_visual],
                    filenames    = ["Original_RGB", "Hasil_Konversi_RGB_ke_CMYK", "Hasil_Normalisasi_CMYK", "Channel_C", "Channel_M", "Channel_Y", "Channel_K"],
                    buttonText   = "Download Semua Channel **(ZIP)**",
                    zip_filename = "Kumpulan_Hasil_Konversi_RGB_ke_CMYK",
                    buttonType   = 2
                ) 
            download_button(CMYK_img, "Download Hasil Konversi CMYK", "Hasil_Konversi_RGB_ke_CMYK", 1)
        
        st.write("")
        
        #*======================================== 
        #* 3 RGB to HSI
        with st.container(border=True):
            render_numbering(3, "RGB ==> HSI", "#5dfc58")
            RGB, HSI, NORM_HSI = st.columns(3)
            
            HSI_img, NORM_HSI_img, h, s, i = process_hsi(RGB_img)
            
            with RGB:
                st.image(RGB_img, channels="RGB", caption="Original Image")
            with HSI:
                st.image(HSI_img, caption="Visualisasi HSI (Skala 0-255)")
            with NORM_HSI:
                st.image(NORM_HSI_img, channels="RGB", caption="Reconstructed RGB from HSI")
            
            with st.expander("Detail Channel HSI dan Penjelasan Kode"):
                ch1, ch2, ch3 = st.columns(3)
                with ch1: st.image(h, caption="Hue Channel")
                with ch2: st.image(s, caption="Saturation Channel")
                with ch3: st.image(i, caption="Intensity Channel")
            
                st.markdown("#### Penjelasan Kode")
                st.code("""# Splitting RGB
float_img = RGB_img.astype(np.float64)
r, g, b = float_img[:,:,0], float_img[:,:,1], float_img[:,:,2]

# Intensity
I = (r + g + b) / 3.0

# Saturation
min_rgb  = np.minimum(np.minimum(r, g), b)
sum_rgb  = r + g + b
S        = np.where(sum_rgb > 0, 1 - (3.0 / (sum_rgb + eps)) * min_rgb, 0)

# Hue
norm_r, norm_g, norm_b = r/255.0, g/255.0, b/255.0
num       = norm_r - 0.5 * norm_g - 0.5 * norm_b
den       = np.sqrt((norm_r**2 + norm_g**2 + norm_b**2) - (norm_r * norm_g) - (norm_r * norm_b) - (norm_g * norm_b))
cos_theta = np.clip(num / (den + eps), -1.0, 1.0)

H = np.degrees(np.arccos(cos_theta))
H = np.where(norm_b > norm_g, 360.0 - H, H)

# Hue bernilai 0 jika tidak ada saturasi
H = np.where(S == 0, 0, H)

H_vis = (H / 360 * 255).astype(np.uint8) 
S_vis = (S * 255).astype(np.uint8)
I_vis = I.astype(np.uint8)

HSI_img = cv.merge((H_vis, S_vis, I_vis))""", language='python')
            
                st.subheader("Rumus Intensity adalah"); st.latex(r"\frac{(R + G + B)} {3}")
                st.write("Intensity dihitung dengan membagi rata-rata penjumlahan nilai `R`, `G`, dan `B` pada setiap piksel.")
                
                st.subheader("Rumus Saturasi adalah"); st.latex(r"1 - \frac{3}{(R + G + B) + \epsilon} \cdot \min(R, G, B)")
                st.write("Kita mencari nilai minimum di antara warna dasar, lalu membaginya dengan jumlah keseluruhan RGB. Jika jumlah warna `0`, maka nilai saturasi di-set menjadi `0`.")
                
                st.subheader("Rumus Hue adalah"); st.latex(r"\theta = \cos^{-1}\left\{ \frac{ \frac 1 2 [(R-G) + (R-B)] }{[(R-G)^2 + (R-B)(G-B)]^{1/2}}  \right\}")
                st.write("Kita menghitung proporsi sudut menggunakan rumus di atas, lalu membatasinya dengan `np.clip` pada rentang -1 hingga 1. Setelah mendapatkan sudut dalam derajat melalui `arccos`, kita mengecek apakah `B > G`. Jika ya, maka sudut dikurangi dari 360°.")
            
            st.write("")
            st.info("✅ Konversi HSI dapat diunduh di bawah ini:")
            left, right = st.columns(2)
            with left:
                download_button(NORM_HSI_img, "Download Hasil Normalisasi HSI", "Hasil_Normalisasi_HSI")
            with right:
                download_button_zip(
                    imgs         = [RGB_img, HSI_img, NORM_HSI_img, h, s, i],
                    filenames    = ["Original_RGB", "Hasil_Konversi_RGB_ke_HSI", "Hasil_Normalisasi_HSI", "Channel_Hue", "Channel_Saturation", "Channel_Intensity"],
                    buttonText   = "Download Semua Channel **(ZIP)**",
                    zip_filename = "Kumpulan_Hasil_Konversi_RGB_ke_HSI",
                    buttonType   = 2
                )
            download_button(HSI_img, "Download Hasil Konversi HSI", "Hasil_Konversi_RGB_ke_HSI", 1)
        
        st.write("")
        
        #*======================================== 
        #* 4 RGB to YUV
        with st.container(border=True):
            render_numbering(4, "RGB ==> YUV", "#5871fc")
            RGB, YUV, NORM_YUV = st.columns(3)
            
            YUV_img, NORM_YUV_img, y_ch, u_ch, v_ch = process_yuv(RGB_img)
            
            with RGB:
                st.image(RGB_img, "Original Image")
            with YUV:
                st.image(YUV_img, "Manual YUV")
            with NORM_YUV:
                st.image(NORM_YUV_img, "Normalize YUV")
            
            with st.expander("Detail Channel YUV dan Penjelasan Kode"):
                ch1, ch2, ch3 = st.columns(3)
                with ch1: st.image(y_ch, caption="Luminance (Y) Channel")
                with ch2: st.image(u_ch, caption="Chrominance-Blue (U) Channel")
                with ch3: st.image(v_ch, caption="Chrominance-Red (V) Channel")
            
                st.markdown("#### Penjelasan Kode")
                st.code("""r, g, b = cv.split(RGB_img.astype(np.float64))
            
y = (0.299 * r) + (0.587 * g) + (0.114 * b)
u = (-0.169 * r) - (0.331 * g) + (0.500 * b) + 128
v = (0.500 * r) - (0.419 * g) - (0.081 * b) + 128

YUV_img = cv.merge((y, u, v))
YUV_img = np.clip(YUV_img, 0, 255).astype(np.uint8)""", language="python")
            
                st.write("Pertama kita akan membagi channel RGB untuk dimasukkan ke dalam rumus berikut:")
                st.latex(r"""
                \begin{aligned}
                y &= (0.299 \cdot r) + (0.587 \cdot g) + (0.114 \cdot b) \\
                u &= (-0.169 \cdot r) - (0.331 \cdot g) + (0.500 \cdot b) + 128 \\
                v &= (0.500 \cdot r) - (0.419 \cdot g) - (0.081 \cdot b) + 128
                \end{aligned}
                """)
                st.write("Setelah dihitung melalui rumus tersebut, array disatukan kembali dan nilainya dibatasi menggunakan `np.clip` (batas 0 hingga 255) agar aman saat dikonversi menjadi gambar integer 8-bit.")
            
            st.write("")
            st.info("✅ Konversi YUV dapat diunduh di bawah ini:")
            left, right = st.columns(2)
            with left:
                download_button(NORM_YUV_img, "Download Hasil Normalisasi YUV", "Hasil_Normalisasi_YUV")
            with right:
                download_button_zip(
                    imgs         = [RGB_img, YUV_img, NORM_YUV_img, y_ch, u_ch, v_ch],
                    filenames    = ["Original_RGB", "Hasil_Konversi_RGB_ke_YUV", "Hasil_Normalisasi_YUV", "Channel_Y", "Channel_U", "Channel_V"],
                    buttonText   = "Download Semua Channel **(ZIP)**",
                    zip_filename = "Kumpulan_Hasil_Konversi_RGB_ke_YUV",
                    buttonType   = 2
                )
            download_button(YUV_img, "Download Hasil Konversi YUV", "Hasil_Konversi_RGB_ke_YUV", 1)
        
        st.write("")
        
        #*======================================== 
        #* 5 RGB to YCbCr
        with st.container(border=True):
            render_numbering(5, "RGB ==> YCbCr", "#fc58ee")
            RGB, YCbCr, NORM_YCbCr = st.columns(3)
            
            YCbCr_img, NORM_YCbCr_img, y_ch, cb_ch, cr_ch = process_ycbcr(RGB_img)
            
            with RGB:
                st.image(RGB_img, "Original Image")
            with YCbCr:
                st.image(YCbCr_img, "Manual YCbCr")
            with NORM_YCbCr:
                st.image(NORM_YCbCr_img, "Normalize YCbCr")
            
            with st.expander("Detail Channel YCbCr dan Penjelasan Kode"):
                ch1, ch2, ch3 = st.columns(3)
                with ch1: st.image(y_ch, caption="Luminance (Y) Channel")
                with ch2: st.image(cb_ch, caption="Chrominance-Blue (Cb) Channel")
                with ch3: st.image(cr_ch, caption="Chrominance-Red (Cr) Channel")
            
                st.markdown("#### Penjelasan Kode")
                st.code("""r, g, b = cv.split(RGB_img.astype(np.float64)
norm_r, norm_g, norm_b = r / 255.0, g / 255.0, b / 255.0

y  = 16  + ( 65.4810 * norm_r) + ( 128.5530 * norm_g) + ( 24.9660 * norm_b)
cb = 128 + (-37.7745 * norm_r) + (-74.1592 * norm_g) + (111.9337 * norm_b)
cr = 128 + (111.9581 * norm_r) + (-93.7509 * norm_g) + (-18.2072 * norm_b)

YCbCr_img = cv.merge((y, cb, cr))
YCbCr_img = np.clip(YCbCr_img, 0, 255).astype(np.uint8)""", language="python")
            
                st.write("Perbedaan metode `YCbCr` dan `YUV` utamanya terletak pada koefisien rumus matematis yang digunakan untuk standar digital.")
                st.write("Sebelum dimasukkan ke dalam matriks, nilai piksel RGB wajib dinormalisasi dengan membaginya terhadap 255 terlebih dahulu.")
                st.latex(r"""
                \begin{aligned}
                Y  &= 16  + ( 65.4810 \cdot r) + ( 128.5530 \cdot g) + (  24.9660 \cdot b) \\
                Cb &= 128 + (-37.7745 \cdot r) + ( -74.1592 \cdot g) + ( 111.9337 \cdot b) \\
                Cr &= 128 + (111.9581 \cdot r) + ( -93.7509 \cdot g) + ( -18.2072 \cdot b)
                \end{aligned}
                """)
                st.write("Sama halnya dengan YUV, hasilnya disatukan menggunakan fungsi merge dan dibatasi nilainya secara keras agar tidak ada *overflow* yang merusak gambar.")
            
            st.write("")
            st.info("✅ Konversi YCbCr dapat diunduh di bawah ini:")
            left, right = st.columns(2)
            with left:
                download_button(NORM_YCbCr_img, "Download Hasil Normalisasi YCbCr", "Hasil_Normalisasi_YCbCr")
            with right:
                download_button_zip(
                    imgs         = [RGB_img, YCbCr_img, NORM_YCbCr_img, y_ch, cb_ch, cr_ch],
                    filenames    = ["Original_RGB", "Hasil_Konversi_RGB_ke_YCbCr", "Hasil_Normalisasi_YCbCr", "Channel_Y", "Channel_Cb", "Channel_Cr"],
                    buttonText   = "Download Semua Channel **(ZIP)**",
                    zip_filename = "Kumpulan_Hasil_Konversi_RGB_ke_YCbCr",
                    buttonType   = 2
                )
            download_button(YCbCr_img, "Download Hasil Konversi YCbCr", "Hasil_Konversi_RGB_ke_YCbCr", 1)

def image_smoothing(RGB_img):
    st.write("Menerapkan filter smoothing pada citra berwarna dengan dua metode: `Intensity Slicing` dan `RGB Channel Smoothing`.")
    
    with st.container(border=True):
        st.markdown("#### ⚙️ Pengaturan Smoothing")
        kernel_size = st.slider("Pilih Ukuran Kernel", min_value=3, max_value=17, step=2, value=7)
    
    st.markdown("<p style='text-align: center;'> ----------------- </p>", unsafe_allow_html=True)
    st.write("")
    
    if image is None:
        st.warning("Upload image to continue!")
    
    else:
        #*========================================
        #* 1 RGB Channel Smoothing
        with st.container(border=True):
            render_numbering(1, "RGB Channel Smoothing", "#94fc58")
            ORIGINAL, SMOOTH = st.columns(2)
            
            with ORIGINAL:
                st.image(RGB_img, caption="Original Image")
                
            with SMOOTH:
                smoothed_RGB_img = smooth_rgb(RGB_img, kernel_size)
                st.image(smoothed_RGB_img, caption="RGB Channel Smoothing")
            
            with st.expander("Detail Channel dan Penjelasan Kode"):
                ChBlack = np.full_like(smoothed_RGB_img[:,:,1], 0)
                R, G, B = st.columns(3)
                
                with R: 
                    r = cv.merge((smoothed_RGB_img[:,:,0], ChBlack, ChBlack))
                    st.image(r, caption="Red Channel")
                with G: 
                    g = cv.merge((ChBlack, smoothed_RGB_img[:,:,1], ChBlack))
                    st.image(g, caption="Green Channel")
                with B: 
                    b = cv.merge((ChBlack, ChBlack, smoothed_RGB_img[:,:,2]))
                    st.image(b, caption="Blue Channel")

                st.markdown("#### Penjelasan tentang kode RGB channel smoothing...")
                st.code("""pad_val    = kernel_size // 2
rgb_padded = cv.copyMakeBorder(rgb_img, pad_val, pad_val, pad_val, pad_val, cv.BORDER_REPLICATE)

height,   width              = rgb_img.shape[:2]
r,        g       , b        = cv.split(rgb_img)
r_smooth, g_smooth, b_smooth = np.zeros_like(r), np.zeros_like(g), np.zeros_like(b)

for y in range(height):   
for x in range(width):
    neighborhood = rgb_padded[y : y + kernel_size, x : x + kernel_size]
    
    avg_color = np.mean(neighborhood, axis=(0, 1))
    
    r_smooth[y, x] = avg_color[0]
    g_smooth[y, x] = avg_color[1]
    b_smooth[y, x] = avg_color[2]

smoothed_RGB_img = cv.merge((r_smooth, g_smooth, b_smooth)).astype(np.uint8)""", language="python")
                st.write("Pertama, kita menentukan nilai padding yang diperlukan berdasarkan ukuran kernel yang dipilih. Kemudian, kita membuat citra baru dengan padding menggunakan `cv.copyMakeBorder` untuk menghindari masalah indeks saat mengakses tetangga piksel di tepi citra.")
                st.write("Setelah itu, kita mengiterasi setiap piksel pada citra asli, mengambil tetangga piksel sesuai ukuran kernel, dan menghitung rata-rata warna di dalam area tersebut untuk masing-masing channel (R, G, B). Hasilnya disimpan dalam array terpisah untuk setiap channel, yang kemudian digabung kembali menjadi citra RGB yang sudah dihaluskan.")
            
            left, right = st.columns(2)
            with left:
                download_button_zip(
                    imgs         = [RGB_img       , smoothed_RGB_img     , r, g, b],
                    filenames    = ["Original_RGB", "Hasil_Smoothing_RGB", "Channel_R"            , "Channel_G"            , "Channel_B"],
                    buttonText   = "Download Semua Channel **(ZIP)**",
                    zip_filename = "Kumpulan_Hasil_Smoothing_RGB",
                    buttonType   = 2
                )   
            with right:
                download_button(smoothed_RGB_img, "Download Hasil Normalisasi RGB", "Hasil_Normalisasi_RGB", 1)

        st.write("")
        
        #*========================================
        #* 2 Intensity Slicing Smoothing
        with st.container(border=True):
            render_numbering(2, "Intensity Slicing Smoothing", "#ffffff")
            ORIGINAL, INTENSITY, SMOOTH = st.columns(3)
            
            smoothed_HSI_img = smooth_hsi(rgb_to_hsi(RGB_img), kernel_size)
            i = smoothed_HSI_img[:,:,2]                
            
            with ORIGINAL:
                st.image(RGB_img, caption="Original Image")
                
            with INTENSITY:
                st.image(i, caption="Intensity Channel")
            
            with SMOOTH:
                smoothed_NORM_HSI_img = hsi_to_rgb(smoothed_HSI_img)
                st.image(smoothed_NORM_HSI_img, caption="Intensity Slicing")
            
            with st.expander("Detail Channel dan Penjelasan Kode"):
                H, S, I = st.columns(3)
                
                st.markdown("#### Penjelasan tentang kode intensity slicing smoothing")
                st.code("""pad_val  = kernel_size // 2
I_padded = cv.copyMakeBorder(I, pad_val, pad_val, pad_val, pad_val, cv.BORDER_REPLICATE)

height, width   = I.shape
smooth_I        = np.zeros_like(I, dtype=np.uint8)

for y in range(height):
for x in range(width):
    neighborhood = I_padded[y:y+kernel_size, x:x+kernel_size]
    smooth_I[y, x] = np.sum(neighborhood) / (kernel_size**2)""", language="python")
                st.write("Pertama, kita akan mencari padding value yang diperlukan dengan membagi ukuran kernel, setelah itu pembuatan padding saya menggunakan fitur bawaan OpenCV `copyMakeBorder` dengan metode `BORDER_REPLICATE` untuk memperluas padding citra dengan mereplikasi nilai tepi citra.")
                st.write("Setelah memiliki padding citra, selanjutnya kita akan mengiterasi masing masing piksel pada citra asli dan mengkalkulasi nilai rata rata dari tetangga piksel sesuai ukuran kernel yang dipilih")
                st.markdown("#### Alternatif kode yang lebih efisien:")
                st.code("""I             = HSI_img[:,:,2]
kernel_size_s = max(3, kernel_size_i // 2)

if kernel_size_s % 2 == 0: kernel_size_s += 1 

smooth_I = cv.blur(I, (kernel_size_i, kernel_size_i), borderType=cv.BORDER_REPLICATE)

smoothed_HSI_img = cv.merge((HSI_img[:,:,0], HSI_img[:,:,1], smooth_I))""", language="python")
                st.write("Alternatif kode di atas menggunakan fungsi `cv.blur` yang sudah dioptimasi untuk melakukan operasi smoothing dengan cara yang jauh lebih efisien dibandingkan iterasi manual.")
                st.write("Kita juga menerapkan ukuran kernel yang lebih kecil untuk channel Saturation agar mempertahankan detail warna, sementara channel Intensity dihaluskan dengan ukuran kernel yang lebih besar untuk hasil smoothing yang lebih efektif.")
            
            left, right = st.columns(2)
            with left:
                download_button_zip(
                    imgs         = [RGB_img       , smoothed_HSI_img                , smoothed_NORM_HSI_img            , smoothed_HSI_img[:,:,0], smoothed_HSI_img[:,:,1], i                  ],
                    filenames    = ["Original_RGB", "Hasil_Smoothing_Intensitas_HSI", "Hasil_Normalisasi_Smoothing_HSI", "Channel_Hue"          , "Channel_Saturation"   , "Channel_Intensity"],
                    buttonText   = "Download Semua Channel **(ZIP)**",
                    zip_filename = "Kumpulan_Hasil_Smoothing_HSI",
                    buttonType   = 2
                )   
            with right:
                download_button(smoothed_NORM_HSI_img, "Download Hasil Smoothing HSI", "Hasil_Smoothing_HSI", 1)

def image_sharpening(RGB_img):
    st.write("Menerapkan filter sharpening pada citra berwarna dengan dua metode: `Intensity Slicing` dan `RGB Channel Sharpening`.")
    
    with st.container(border=True):
        st.markdown("#### ⚙️ Pengaturan Sharpening")
        kernel_size = st.slider("Pilih Ukuran Kernel _(nilai dibagi 100)_", min_value=0, max_value=100, step=1, value=50) / 100
    
    st.markdown("<p style='text-align: center;'> ----------------- </p>", unsafe_allow_html=True)
    st.write("")
    
    if image is None:
        st.warning("Upload image to continue!")
        
    else:
        #*========================================
        #* 1 RGB Channel Sharpening
        with st.container(border=True):
            render_numbering(1, "RGB Channel Sharpening", "#94fc58")
            ORIGINAL, SHARPENED = st.columns(2)
            
            with ORIGINAL:
                st.image(RGB_img, caption="Original Image")
                
            with SHARPENED:
                sharpened_RGB_img = sharpen_rgb(RGB_img, kernel_size)
                st.image(sharpened_RGB_img, caption="RGB Channel Sharpening")
            
            with st.expander("Detail Channel dan Penjelasan Kode"):
                R, G, B = st.columns(3)
                with R: 
                    r = cv.merge((sharpened_RGB_img[:,:,0], ChBlack, ChBlack))
                    st.image(r, caption="Red Channel")
                with G: 
                    g = cv.merge((ChBlack, sharpened_RGB_img[:,:,1], ChBlack))
                    st.image(g, caption="Green Channel")
                with B: 
                    b = cv.merge((ChBlack, ChBlack, sharpened_RGB_img[:,:,2]))
                    st.image(b, caption="Blue Channel")

                st.markdown("#### Penjelasan tentang kode RGB channel sharpening")
                st.code("""float_rgb_img = rgb_img.astype(np.float32)

kernel = np.array([[ 0,       -k,  0],
               [-k,  1 + 4*k, -k],
               [ 0,       -k,  0]])

res = cv.filter2D(float_rgb_img, -1, kernel)
sharpened_RGB_img = np.clip(res, 0, 255).astype(np.uint8)""", language="python")
                st.write("Pertama, kita mengonversi citra RGB ke tipe data `float32` untuk mencegah overflow selama proses konvolusi.")
                st.write("Selanjutnya kita mendefinisikan kernel untuk sharpening, dimana nilai `k` digunakan untuk mengontrol tingkat ketajaman citra.")
                st.write("Kemudian kita menggunakan fungsi bawaan dari **OpenCV** yaitu `filter2D` untuk menerapkan kernel tersebut ke citra")

            left, right = st.columns(2)
            with left:
                download_button_zip(
                    imgs         = [RGB_img       , sharpened_RGB_img     , r           , g          , b          ],
                    filenames    = ["Original_RGB", "Hasil_Sharpening_RGB", "Channel_R" , "Channel_G", "Channel_B"],
                    buttonText   = "Download Semua Channel **(ZIP)**",
                    zip_filename = "Kumpulan_Hasil_Sharpening_RGB",
                    buttonType   = 2
                )   
            with right:
                download_button(sharpened_RGB_img, "Download Hasil Sharpening RGB", "Hasil_Sharpening_RGB", 1)


        #*========================================
        #* 2 Intensity Channel Sharpening
        with st.container(border=True):
            render_numbering(2, "Intensity Channel Sharpening", "#589ffc")
            ORIGINAL, I, SHARPENED = st.columns(3)
            
            HSI_img                = rgb_to_hsi(RGB_img)
            sharpened_HSI_img      = sharpen_hsi(HSI_img, kernel_size)
            sharpened_NORM_HSI_img = hsi_to_rgb(sharpened_HSI_img)
            
            with ORIGINAL:
                st.image(RGB_img, caption="Original Image")
                
            with I:
                st.image(sharpened_HSI_img[:,:,2], caption="Intensity Channel")
            
            with SHARPENED:
                st.image(sharpened_NORM_HSI_img, caption="Sharpened Intensity Channel")
                
            with st.expander("Detail Channel dan Penjelasan Kode"):
                H, S, I = st.columns(3)
                with H: st.image(sharpened_HSI_img[:,:,0], caption="Hue Channel")
                with S: st.image(sharpened_HSI_img[:,:,1], caption="Saturation Channel")
                with I: st.image(sharpened_HSI_img[:,:,2], caption="Intensity Channel")

                st.markdown("#### Penjelasan Kode")
                st.code("""i = HSI_img[:, :, 2].astype(np.float32)

kernel = np.array([[ 0,       -k,  0],
               [-k,  1 + 4*k, -k],
               [ 0,       -k,  0]])

res = cv.filter2D(i, -1, kernel)
sharp_i = np.clip(res, 0, 255).astype(np.uint8)
sharpened_HSI_img = cv.merge((HSI_img[:,:,0], HSI_img[:,:,1], sharp_i))""", language="python")
                st.write("Sharpening dimulai dengan mengubah tipe channel intensity menjadi `float32` untuk menghindari **overflow**. Kemudian, kita mendifinisikan kernel sharpening, sama seperti kernel pada metode RGB Sharpening")
                st.write("Setelah itu, kernel di terapkan ke channel intensity menggunakan `cv.filter2D`, dan hasilnya dibatasi diantara 0 hingga 255.")
                st.write("Terakhir, channel intensity akan di gabungkan kembali dengan channel hue dan saturation yang tidak berubah untuk menghasilkan citra HSI")
                
            left, right = st.columns(2)
            with left:
                download_button_zip(
                    imgs         = [RGB_img       , sharpened_HSI_img                , sharpened_NORM_HSI_img            , sharpened_HSI_img[:,:,0], sharpened_HSI_img[:,:,1], sharpened_HSI_img[:,:,2]],
                    filenames    = ["Original_RGB", "Hasil_Sharpening_Intensitas_HSI", "Hasil_Normalisasi_Sharpening_HSI", "Channel_Hue"           , "Channel_Saturation"    , "Channel_Intensity"     ],
                    buttonText   = "Download Semua Channel **(ZIP)**",
                    zip_filename = "Kumpulan_Hasil_Sharpening_HSI",
                    buttonType   = 2
                )   
            with right:
                download_button(sharpened_NORM_HSI_img, "Download Hasil Sharpening HSI", "Hasil_Sharpening_HSI", 1)                    

# =========================================================
# FUNGSI APLIKASI UTAMA
# =========================================================

def home():
    st.info("**Info:** Aplikasi ini dikembangkan sebagai portofolio Mata Kuliah Pengolahan Citra Digital (PCD).")
    st.subheader("🚀 Rangkuman Materi")
    m1, m2, m3 = st.columns(3)
    
    with m1:
        with st.container(border=True):
            st.markdown("### 🪄 Materi 4")
            st.markdown("""
            **Peningkatan Citra Spasial**
            Fokus pada manipulasi piksel secara langsung ($g = T[f]$). 
            - **Point Processing:** Image Negative, log transformation, dan bit-plane slicing.
            - **Konversi Warna:** Teknik merubah RGB ke Grayscale (Lightness, Average, Luminosity).
            - **Operasi:** Aritmatika (penjumlahan/pengurangan citra) dan Logika (AND, OR, NOT).
            """)

    with m2:
        with st.container(border=True):
            st.markdown("### 📊 Materi 5")
            st.markdown("""
            **Histogram & Filtering**
            Membahas distribusi intensitas dan perbaikan visual.
            - **Histogram:** Statistik global citra dan *Histogram Equalization* untuk kontras.
            - **Smoothing:** Filter tetangga (Mean/Median) untuk mereduksi noise/bluring.
            - **Sharpening:** Penggunaan operator *Laplacian* untuk memperjelas tepi (edge) citra.
            """)

    with m3:
        with st.container(border=True):
            st.markdown("### 🎨 Materi 6")
            st.markdown("""
            **Pengolahan Citra Berwarna**
            Dasar spektrum warna dan model koordinat.
            - **Model Warna:** Perbedaan RGB (hardware), CMY/K (cetak), dan HSI (persepsi manusia).
            - **Pseudo-coloring:** Memberi warna pada citra grayscale berdasarkan intensitas.
            - **Processing:** Implementasi filtering dan transformasi langsung pada domain warna.
            """)

    st.write("")

def course_4():
    def get_user_name():
        return 'John'
    
    with st.echo():
        def get_punctuation():
            return '!!!'
    
        greeting = "Hi there, "
        value = get_user_name()
        punctuation = get_punctuation()
    
        st.write(greeting, value, punctuation)
    
    foo = 'bar'
    st.write('Done!')

def course_5():
    
    st.write('Done!')

def course_6():
    # --- HEADER DEKORATIF ---
    st.markdown("""
        <div style="background-color:#2e3136; padding:20px; border-radius:10px; border-left: 8px solid #00BCD4;">
            <h1 style="margin:0;">Pengolahan Citra Berwarna</h1>
            <p style="color:#888; margin:5px 0 0 0;">Ringkasan Modul Slide-05 • Pengolahan Citra Digital</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("") 

    # --- SECTION 1: PENDAHULUAN & PERSEPSI ---
    col1, col2 = st.columns([1, 1], gap="medium")
    
    with col1:
        with st.container(border=True):
            st.subheader("👀 Persepsi Manusia")
            st.write("Mata manusia dapat membedakan ribuan warna, namun hanya sekitar dua lusin derajat keabuan.")
            st.write("- **Warna:** Memberikan informasi objek yang lebih detail.")
            st.write("- **Sensitivitas:** Manusia mengenali 10.000+ warna berbeda.")
            
    with col2:
        with st.container(border=True):
            st.subheader("🎨 Jenis Pengolahan")
            st.write("1. **Full-color Processing:** Citra diakuisisi dengan sensor warna (kamera digital).")
            st.write("2. **Pseudo-color Processing:** Memberikan warna pada nilai gray-level berdasarkan kriteria tertentu.")
    
    # --- SECTION 2: MODEL WARNA (RGB vs CMYK) ---
    st.markdown("### 🧬 Model Warna Utama")
    c1, c2 = st.columns(2)
    
    with c1:
        with st.container(border=True):
            st.info("**RGB Model (Additive)**")
            st.write("Digunakan untuk display (monitor, TV). Berdasarkan warna primer: Red, Green, Blue.")
            st.latex(r"\text{Citra} = (R, G, B)")
            st.caption("Pencampuran semua warna primer menghasilkan warna Putih.")
            
    with c2:
        with st.container(border=True):
            st.info("**CMY/CMYK Model (Subtractive)**")
            st.write("Digunakan untuk pencetakan (printing). Cyan, Magenta, Yellow.")
            st.latex(r"\begin{bmatrix} C \\ M \\ Y \end{bmatrix} = \begin{bmatrix} 1 \\ 1 \\ 1 \end{bmatrix} - \begin{bmatrix} R \\ G \\ B \end{bmatrix}")
            st.caption("K = Black ditambahkan untuk menghasilkan hitam pekat yang efisien.")

    # --- SECTION 3: HSI MODEL (HUE, SATURATION, INTENSITY) ---
    st.markdown("### 🧠 Model Warna HSI")
    with st.container(border=True):
        st.write("Model HSI lebih mendekati cara manusia mendeskripsikan warna dibandingkan RGB.")
        
        grid1, grid2, grid3 = st.columns(3)
        with grid1:
            st.success("**Hue (H)**")
            st.write("Menyatakan warna murni (Merah, Kuning, dsb). Diukur dalam derajat (0° - 360°).")
        with grid2:
            st.success("**Saturation (S)**")
            st.write("Derajat kemurnian warna (seberapa banyak warna putih yang tercampur).")
        with grid3:
            st.success("**Intensity (I)**")
            st.write("Kecerahan warna. Keunggulan HSI adalah memisahkan informasi warna (H, S) dari intensitas (I).")

    # --- SECTION 4: PSEUDO-COLOR & SLICING ---
    st.markdown("### 🧪 Pseudo-color Image Processing")
    with st.container(border=True):
        st.write("Memberikan warna pada citra monokrom untuk memudahkan interpretasi visual.")
        
        col_ps1, col_ps2 = st.columns(2)
        with col_ps1:
            st.markdown("#### **Intensity Slicing**")
            st.write("Memisahkan range gray level ke dalam beberapa bidang dan memberikan warna berbeda pada tiap bidang.")
        with col_ps2:
            st.markdown("#### **Gray Level to Color**")
            st.write("Menggunakan fungsi transformasi (R, G, B) yang independen terhadap nilai input gray level.")

    # --- SECTION 5: FULL-COLOR OPERATIONS ---
    st.markdown("### 🛠️ Full-Color Operations")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        with st.container(border=True):
            st.subheader("🌊 Smoothing & Sharpening")
            st.write("- **Smoothing:** Menghaluskan citra warna dengan merata-ratakan nilai RGB tetangga.")
            st.write("- **Sharpening:** Memperjelas tepi warna menggunakan operator Laplacian.")
            
    with col_f2:
        with st.container(border=True):
            st.subheader("🌓 Color Transformation")
            st.write("Modifikasi warna berdasarkan fungsi: $s_i = T_i(r_1, r_2, ..., r_n)$.")
            st.write("- **Tone Adjustment:** Koreksi warna gelap/terang.")
            st.write("- **Color Balancing:** Menyeimbangkan dominasi warna.")

    st.divider()
    st.markdown("### 📝 Pemilihan Tugas (Materi 6)")
    
    rgb_converter, smoothing, sharpening = st.tabs(["Konversi RGB", "Smoothing Citra Berwarna", "Sharpening Citra Berwarna"])
    
    with rgb_converter:
        rgb_conversion(RGB_img)
        
    with smoothing:
        image_smoothing(RGB_img)
        
    with sharpening:
        image_sharpening(RGB_img)
        
# =========================================================
# FUNGSI UTILITAS UI & PENGUNDUHAN
# =========================================================

def render_numbering(number, description, color="#ffffff"):
    bg_color = f"{color}22" 
    html_code = f"""
    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px; margin-top: 5px;">
        <div style="
            background-color: {bg_color}; 
            color: {color}; 
            width: 40px; 
            height: 40px; 
            border-radius: 50%; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            font-size: 20px; 
            font-weight: bold;
            border: 2px solid {color};
            flex-shrink: 0;
        ">
            {number}
        </div>
        <div style="
            font-size: 1.3em; 
            font-weight: bold; 
            color: white; 
            text-transform: capitalize;
        ">
            {description}
        </div>
    </div>
    """
    return st.markdown(html_code, unsafe_allow_html=True)

def download_button(img, buttonText, filename, buttonType=2, reverse_channels=True):
    curr_img = img.copy()
    if reverse_channels:
        if len(curr_img.shape) == 3:
            channels = curr_img.shape[2]
            if channels == 3:
                x, y, z = cv.split(curr_img)
                curr_img = cv.merge((z, y, x))
            elif channels == 4:
                x, y, z, w = cv.split(curr_img)
                curr_img = cv.merge((w, z, y, x))
    
    _, buffer = cv.imencode('.jpg', curr_img)
    byte_im = buffer.tobytes()
    
    st.write("")
    button_type = "secondary" if buttonType == 2 else "primary"
    
    st.download_button(
        label               = buttonText,
        data                = byte_im,
        file_name           = f"{filename}.jpg",
        mime                = "image/jpeg",
        use_container_width = True,
        key                 = f"btn_{filename}",
        type                = button_type
    )

def download_button_zip(imgs, buttonText, zip_filename, filenames, buttonType=3, reverse_channels=True):
    if not isinstance(imgs, list): imgs = [imgs]
    if not isinstance(filenames, list): filenames = [filenames]
    
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for img, fname in zip(imgs, filenames):
            curr_img = img.copy()
            if reverse_channels:
                if len(curr_img.shape) == 3:
                    channels = curr_img.shape[2]
                    if channels == 3:
                        x, y, z = cv.split(curr_img)
                        curr_img = cv.merge((z, y, x))
                    elif channels == 4:
                        x, y, z, w = cv.split(curr_img)
                        curr_img = cv.merge((w, z, y, x))
            
            success, buffer = cv.imencode('.jpg', curr_img)
            if success:
                # st.image(buffer.tobytes(), caption=fname) #! DEBUGGING PURPOSE
                zip_file.writestr(f"{fname}.jpg", buffer.tobytes())
    
    st.write("")
    if buttonType == 1:
        button_type = "primary"
    elif buttonType == 2:
        button_type = "secondary"
    else:
        button_type = "tertiary"
    
    st.download_button(
        label               = buttonText,
        data                = zip_buffer.getvalue(),
        file_name           = f"{zip_filename}.zip",
        mime                = "application/zip",
        use_container_width = True,
        type                = button_type
    )

# =========================================================
# ROUTING DASHBOARD SIDEBAR
# =========================================================

courses_page = {
    "👤 Home Page": home,
    "🪄 Materi 4": course_4,
    "📊 Materi 5": course_5,
    "🎨 Materi 6": course_6
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
    image = st.file_uploader("Upload Gambar", type=["jpeg", "jpg", "png"])

if image is not None:
    file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
    img = cv.imdecode(file_bytes, 1)
    
    # --- LOGIKA AUTO-RESIZE CAP 1080p ---
    max_dim = 1080
    h, w = img.shape[:2]
    if h > max_dim or w > max_dim:
        if h > w:
            new_h, new_w = max_dim, int(w * max_dim / h)
        else:
            new_h, new_w = int(h * max_dim / w), max_dim
        img = cv.resize(img, (new_w, new_h), interpolation=cv.INTER_AREA)
    # ------------------------------------
    
    RGB_img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    
    ChBlack = np.full_like(RGB_img[:,:,1], 0)

courses_page[selectedCourse]()