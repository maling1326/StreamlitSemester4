import streamlit as st
import numpy as np
import cv2 as cv
import zipfile
import io

#* --- GLOBAL IMAGE PROCESSING ---

@st.cache_data
def CAPFULLHD(img):
    max_dim = 1080
    h, w = img.shape[:2]
    if h > max_dim or w > max_dim:
        if h > w:
            new_h, new_w = max_dim, int(w * max_dim / h)
        else:
            new_h, new_w = int(h * max_dim / w), max_dim
        img = cv.resize(img, (new_w, new_h), interpolation=cv.INTER_AREA)
    
    return img

#* --- FOR LECTURE 4 ---

@st.cache_data(show_spinner=True)
def rgb2gray_3method(rgb_img):
    imgHeight, imgWidth = rgb_img.shape[:2]
            
    grayscale_lightness  = np.zeros((imgHeight, imgWidth), dtype=np.uint8)
    grayscale_average    = np.zeros((imgHeight, imgWidth), dtype=np.uint8) 
    grayscale_luminosity = np.zeros((imgHeight, imgWidth), dtype=np.uint8) 
            
    for y in range(imgHeight):
        for x in range(imgWidth):
            r, g, b  = rgb_img[ y , x ]
                    
            grayscale_lightness [ y , x ] = int( ( int(max( [r , g , b] )) + int(min( [r , g , b] )) )  / 2 )
            grayscale_average   [ y , x ] = int( ( int(r) + int(g) + int(b) ) / 3 )
            grayscale_luminosity[ y , x ] = int( (0.21 * r) + (0.72 * g) + (0.07 * b) )
    return grayscale_lightness, grayscale_average, grayscale_luminosity

#* --- FOR LECTURE 6 ---

@st.cache_data(show_spinner=True)
def process_cmy(rgb_img):
    ChWhite = np.full_like(rgb_img[:,:,1], 255)

    CMY_img = 255 - rgb_img
    cmy_normalized = CMY_img.astype(np.float64) / 255.0
    rgb_reconstructed = 255.0 * (1.0 - cmy_normalized)
    NORM_CMY_img = (rgb_reconstructed * 0.95).astype(np.uint8)
    
    c, m, y = cv.split(CMY_img)
    c_visual = cv.merge((255 - c, ChWhite, ChWhite))
    m_visual = cv.merge((ChWhite, 255 - m, ChWhite))
    y_visual = cv.merge((ChWhite, ChWhite, 255 - y))
    
    return CMY_img, NORM_CMY_img, c_visual, m_visual, y_visual

@st.cache_data(show_spinner=True)
def process_cmyk(rgb_img):
    ChWhite = np.full_like(rgb_img[:,:,1], 255)
    
    float_img = 255 - rgb_img.astype(np.float64)
    c, m, y = float_img[:,:,0], float_img[:,:,1], float_img[:,:,2] 
    
    k = np.min([c, m, y], axis=0)
    c -= k
    m -= k
    y -= k
    
    CMYK_img = cv.merge((c, m, y)).astype(np.uint8)
    
    r_vis = 255.0 - (c + k)
    g_vis = 255.0 - (m + k)
    b_vis = 255.0 - (y + k)
    
    loss_factor = 0.95 
    r_vis *= loss_factor
    g_vis *= loss_factor
    b_vis *= loss_factor
    
    NORM_CMYK_img = cv.merge((r_vis, g_vis, b_vis)).astype(np.uint8)
    
    c_visual = cv.merge((255 - c.astype(np.uint8), ChWhite, ChWhite))
    m_visual = cv.merge((ChWhite, 255 - m.astype(np.uint8), ChWhite))
    y_visual = cv.merge((ChWhite, ChWhite, 255 - y.astype(np.uint8)))
    k_visual = cv.merge((255 - k.astype(np.uint8), 255 - k.astype(np.uint8), 255 - k.astype(np.uint8)))
    
    return CMYK_img, NORM_CMYK_img, c_visual, m_visual, y_visual, k_visual

@st.cache_data(show_spinner=True)
def process_hsi(rgb_img):
    # 1. Ganti float64 menjadi float32 (Menghemat 50% RAM)
    float_img = rgb_img.astype(np.float32)
    r, g, b = float_img[:,:,0], float_img[:,:,1], float_img[:,:,2]
    
    I = (r + g + b) / 3.0
    
    min_rgb  = np.minimum(np.minimum(r, g), b)
    sum_rgb  = r + g + b
    # Pastikan epsilon (eps) juga dalam format float32
    eps_f32  = np.float32(1e-6)
    S        = np.where(sum_rgb > 0, 1 - (3.0 / (sum_rgb + eps_f32)) * min_rgb, 0)
    
    norm_r, norm_g, norm_b = r/255.0, g/255.0, b/255.0
    num       = norm_r - 0.5 * norm_g - 0.5 * norm_b
    inner_den = (norm_r**2 + norm_g**2 + norm_b**2) - (norm_r * norm_g) - (norm_r * norm_b) - (norm_g * norm_b)
    den       = np.sqrt(np.maximum(inner_den, 0.0))
    cos_theta = np.clip(num / (den + eps_f32), -1.0, 1.0)
    
    H = np.degrees(np.arccos(cos_theta))
    H = np.where(norm_b > norm_g, 360.0 - H, H)
    H = np.where(S == 0, 0, H)
    
    H_vis = (H / 360 * 255).astype(np.uint8) 
    S_vis = (S * 255).astype(np.uint8)
    I_vis = I.astype(np.uint8)
    
    HSI_img = cv.merge((H_vis, S_vis, I_vis))
    
    # 2. Hapus variabel besar yang sudah tidak dipakai untuk melegakan nafas Server
    del float_img, norm_r, norm_g, norm_b, num, inner_den, den, cos_theta, sum_rgb, min_rgb
    
    # 3. Gunakan tipe float32 untuk array rekonstruksi
    r_rec = np.zeros_like(I, dtype=np.float32)
    g_rec = np.zeros_like(I, dtype=np.float32)
    b_rec = np.zeros_like(I, dtype=np.float32)
    
    H_rad = np.radians(H).astype(np.float32)
    
    mask_rg = (H >= 0) & (H < 120)
    b_rec[mask_rg] = I[mask_rg] * (1.0 - S[mask_rg])
    r_rec[mask_rg] = I[mask_rg] * (1.0 + (S[mask_rg] * np.cos(H_rad[mask_rg])) / np.cos(np.radians(60.0) - H_rad[mask_rg]))
    g_rec[mask_rg] = 3.0 * I[mask_rg] - (r_rec[mask_rg] + b_rec[mask_rg])
    
    mask_gb = (H >= 120) & (H < 240)
    H_gb = H_rad[mask_gb] - np.radians(120.0)
    r_rec[mask_gb] = I[mask_gb] * (1.0 - S[mask_gb])
    g_rec[mask_gb] = I[mask_gb] * (1.0 + (S[mask_gb] * np.cos(H_gb)) / np.cos(np.radians(60.0) - H_gb))
    b_rec[mask_gb] = 3.0 * I[mask_gb] - (r_rec[mask_gb] + g_rec[mask_gb])
    
    mask_br = (H >= 240) & (H <= 360)
    H_br = H_rad[mask_br] - np.radians(240.0)
    g_rec[mask_br] = I[mask_br] * (1.0 - S[mask_br])
    b_rec[mask_br] = I[mask_br] * (1.0 + (S[mask_br] * np.cos(H_br)) / np.cos(np.radians(60.0) - H_br))
    r_rec[mask_br] = 3.0 * I[mask_br] - (g_rec[mask_br] + b_rec[mask_br])
    
    NORM_HSI_img = cv.merge((r_rec, g_rec, b_rec))
    NORM_HSI_img = np.clip(NORM_HSI_img, 0, 255).astype(np.uint8)
    
    return HSI_img, NORM_HSI_img, H_vis, S_vis, I_vis

@st.cache_data(show_spinner=True)
def process_yuv(rgb_img):
    r, g, b = cv.split(rgb_img.astype(np.float64))
    
    y = (0.299 * r) + (0.587 * g) + (0.114 * b)
    u = (-0.169 * r) - (0.331 * g) + (0.500 * b) + 128
    v = (0.500 * r) - (0.419 * g) - (0.081 * b) + 128
    
    YUV_img = cv.merge((y, u, v))
    YUV_img = np.clip(YUV_img, 0, 255).astype(np.uint8)
    
    y_float, u_float, v_float = y.astype(float), u.astype(float), v.astype(float)
    
    norm_r = y_float + (1.402 * (v_float - 128))
    norm_g = y_float - (0.344 * (u_float - 128)) - (0.714 * (v_float - 128))
    norm_b = y_float + (1.772 * (u_float - 128))
    
    NORM_YUV_img = cv.merge((norm_r, norm_g, norm_b))
    NORM_YUV_img = np.clip(NORM_YUV_img, 0, 255).astype(np.uint8)
    
    return YUV_img, NORM_YUV_img, y.astype(np.uint8), u.astype(np.uint8), v.astype(np.uint8)

@st.cache_data(show_spinner=True)
def process_ycbcr(rgb_img):
    r, g, b = cv.split(rgb_img.astype(np.float64))
    norm_r, norm_g, norm_b = r / 255.0, g / 255.0, b / 255.0
    
    y  = 16  + ( 65.4810 * norm_r) + ( 128.5530 * norm_g ) + ( 24.9660 * norm_b )
    cb = 128 + (-37.7745 * norm_r) + ( -74.1592 * norm_g ) + ( 111.9337 * norm_b )
    cr = 128 + (111.9581 * norm_r) + ( -93.7509 * norm_g ) + (-18.2072 * norm_b )
    
    YCbCr_img = cv.merge((y, cb, cr))
    YCbCr_img = np.clip(YCbCr_img, 0, 255).astype(np.uint8)
    
    norm_r = 1.164 * (y - 16) + 1.596 * (cr - 128)
    norm_g = 1.164 * (y - 16) - 0.392 * (cb - 128) - 0.813 * (cr - 128)
    norm_b = 1.164 * (y - 16) + 2.017 * (cb - 128)
    
    NORM_YCbCr_img = cv.merge((norm_r, norm_g, norm_b))
    NORM_YCbCr_img = np.clip(NORM_YCbCr_img, 0, 255).astype(np.uint8)
    
    return YCbCr_img, NORM_YCbCr_img, y.astype(np.uint8), cb.astype(np.uint8), cr.astype(np.uint8)

@st.cache_data(show_spinner=True)
def smooth_rgb(rgb_img, kernel_size=11):
    pad_val    = kernel_size // 2
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
    
    return cv.merge((r_smooth, g_smooth, b_smooth)).astype(np.uint8)

@st.cache_data(show_spinner=True)
def rgb_to_hsi(rgb_img):
    float_img = rgb_img.astype(np.float32)
    r, g, b = float_img[:,:,0], float_img[:,:,1], float_img[:,:,2]
    
    I = (r + g + b) / 3.0
    
    min_rgb  = np.minimum(np.minimum(r, g), b)
    sum_rgb  = r + g + b
    eps_f32  = np.float32(1e-6)
    S        = np.where(sum_rgb > 0, 1 - (3.0 / (sum_rgb + eps_f32)) * min_rgb, 0)
    
    norm_r, norm_g, norm_b = r/255.0, g/255.0, b/255.0
    num       = norm_r - 0.5 * norm_g - 0.5 * norm_b
    inner_den = (norm_r**2 + norm_g**2 + norm_b**2) - (norm_r * norm_g) - (norm_r * norm_b) - (norm_g * norm_b)
    den       = np.sqrt(np.maximum(inner_den, 0.0))
    cos_theta = np.clip(num / (den + eps_f32), -1.0, 1.0)
    
    H = np.degrees(np.arccos(cos_theta))
    H = np.where(norm_b > norm_g, 360.0 - H, H)
    H = np.where(S == 0, 0, H)
    
    H_vis = (H / 360 * 255).astype(np.uint8) 
    S_vis = (S * 255).astype(np.uint8)
    I_vis = I.astype(np.uint8)
    
    HSI_img = cv.merge((H_vis, S_vis, I_vis))
    
    del float_img, norm_r, norm_g, norm_b, num, inner_den, den, cos_theta, sum_rgb, min_rgb, H_vis, S_vis, I_vis, I, S, H
    return HSI_img

@st.cache_data(show_spinner=True)
def hsi_to_rgb(hsi_img):
    # Pastikan input float32 untuk presisi
    H = hsi_img[:,:,0].astype(np.float32) * (360.0 / 255.0)
    S = hsi_img[:,:,1].astype(np.float32) / 255.0
    I = hsi_img[:,:,2].astype(np.float32) / 255.0 # Normalisasi ke 0-1
 
    r_rec = np.zeros_like(I)
    g_rec = np.zeros_like(I)
    b_rec = np.zeros_like(I)
    
    H_rad = np.radians(H)
    cos_60 = np.cos(np.radians(60.0))
    eps = 1e-6 # Epsilon untuk mencegah pembagian nol
    
    # Sektor RG (0 - 120 derajat)
    mask_rg = (H >= 0) & (H < 120)
    b_rec[mask_rg] = I[mask_rg] * (1.0 - S[mask_rg])
    r_rec[mask_rg] = I[mask_rg] * (1.0 + (S[mask_rg] * np.cos(H_rad[mask_rg])) / (np.cos(np.radians(60.0) - H_rad[mask_rg]) + eps))
    g_rec[mask_rg] = 3.0 * I[mask_rg] - (r_rec[mask_rg] + b_rec[mask_rg])
    
    # Sektor GB (120 - 240 derajat)
    mask_gb = (H >= 120) & (H < 240)
    H_gb = H_rad[mask_gb] - np.radians(120.0)
    r_rec[mask_gb] = I[mask_gb] * (1.0 - S[mask_gb])
    g_rec[mask_gb] = I[mask_gb] * (1.0 + (S[mask_gb] * np.cos(H_gb)) / (np.cos(np.radians(60.0) - H_gb) + eps))
    b_rec[mask_gb] = 3.0 * I[mask_gb] - (r_rec[mask_gb] + g_rec[mask_gb])
    
    # Sektor BR (240 - 360 derajat)
    mask_br = (H >= 240) & (H <= 360)
    H_br = H_rad[mask_br] - np.radians(240.0)
    g_rec[mask_br] = I[mask_br] * (1.0 - S[mask_br])
    b_rec[mask_br] = I[mask_br] * (1.0 + (S[mask_br] * np.cos(H_br)) / (np.cos(np.radians(60.0) - H_br) + eps))
    r_rec[mask_br] = 3.0 * I[mask_br] - (g_rec[mask_br] + b_rec[mask_br])
    
    # Kembalikan ke rentang 0-255
    res = cv.merge((r_rec, g_rec, b_rec)) * 255.0
    return np.clip(res, 0, 255).astype(np.uint8)

@st.cache_data(show_spinner=True)
def smooth_hsi(HSI_img, kernel_size_i=11):
    I             = HSI_img[:,:,2]
    kernel_size_s = max(3, kernel_size_i // 2)
    
    if kernel_size_s % 2 == 0: kernel_size_s += 1 
    
    smooth_I = cv.blur(I, (kernel_size_i, kernel_size_i), borderType=cv.BORDER_REPLICATE)
    
    return cv.merge((HSI_img[:,:,0], HSI_img[:,:,1], smooth_I))

@st.cache_data(show_spinner=True)
def sharpen_rgb(rgb_img, k = 1):
    float_rgb_img = rgb_img.astype(np.float32)

    kernel = np.array([[ 0,       -k,  0],
                       [-k,  1 + 4*k, -k],
                       [ 0,       -k,  0]])
    
    res = cv.filter2D(float_rgb_img, -1, kernel)
    return np.clip(res, 0, 255).astype(np.uint8) 
    
@st.cache_data(show_spinner=True)
def sharpen_hsi(HSI_img, k = 1):
    i = HSI_img[:, :, 2].astype(np.float32)
    
    kernel = np.array([[ 0,       -k,  0],
                       [-k,  1 + 4*k, -k],
                       [ 0,       -k,  0]])
    
    res = cv.filter2D(i, -1, kernel)
    sharp_i = np.clip(res, 0, 255).astype(np.uint8)
    return cv.merge((HSI_img[:,:,0], HSI_img[:,:,1], sharp_i))