import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import requests
from streamlit_lottie import st_lottie
import json

# ==========================================
# 1. KONFIGURASI HALAMAN & CSS KUSTOM
# ==========================================
st.set_page_config(
    page_title="FinTech - AI Finance Advisor",
    page_icon="💎",
    layout="wide", # Menggunakan layout lebar agar lebih lega
    initial_sidebar_state="expanded"
)

# CSS Kustom untuk Tampilan Modern
st.markdown("""
    <style>
    /* Mengubah font utama */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }

    /* Kustomisasi Sidebar */
    .css-1d391kg {
        background-color: #1a1c24;
        color: #ffffff;
    }
    
    /* Kustomisasi Kartu/Container */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        color: #00d1b2;
    }

    /* Kustomisasi Tombol Utama */
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        height: 3em;
        background: linear-gradient(45deg, #FF4B4B, #FF8F6B);
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        border: none;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4);
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(255, 75, 75, 0.6);
        background: linear-gradient(45deg, #FF8F6B, #FF4B4B);
    }

    /* Kustomisasi Input */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        border-radius: 10px;
    }

    /* Header Styling */
    .main-header {
        font-weight: 700;
        color: #1a1c24;
        font-size: 3rem;
        margin-bottom: 0px;
    }
    .sub-header {
        color: #6a6e7c;
        font-weight: 400;
        font-size: 1.2rem;
        margin-top: 0px;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. FUNGSI HELPER (ANIMASI & CHART)
# ==========================================

# Fungsi untuk memuat Lottie Animation dari URL
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Fungsi untuk membuat Donut Chart yang Menarik
def create_budget_chart(labels, values, colors):
    fig = go.Figure(data=[go.Pie(
        labels=labels, 
        values=values, 
        hole=.5, # Membuatnya jadi donut chart
        marker_colors=colors,
        textinfo='label+percent',
        hoverinfo='label+value+percent',
        textfont_size=14,
        textposition='outside'
    )])
    
    fig.update_layout(
        showlegend=False,
        margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor='rgba(0,0,0,0)', # Background transparan
        plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig

# Memuat Animasi Lottie (Ganti URL jika ingin animasi lain)
# Animasi Finansial
lottie_finance = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_ml0jwf4j.json")
# Animasi Loading
lottie_loading = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_m6m04dt4.json")

# ==========================================
# 3. SIDEBAR: LOGIN & API KEY
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/diamond.png", width=60) # Logo fiktif
    st.markdown("<h1 style='color: white; font-size: 2rem;'>FinTech AI</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.subheader("🔐 Akses Model")
    user_api_key = st.text_input("Google API Key:", type="password", help="Dapatkan di Google AI Studio")
    # Link ke Google AI Studio
    st.markdown("""
        <a href="https://aistudio.google.com/app/apikey" target="_blank">
            <button style="width:100%; border-radius:10px; border:1px solid #00C9FF; background:transparent; color:#00C9FF; padding:10px; cursor:pointer;">
                🔑 Dapatkan API Key di Google AI Studio
            </button>
        </a>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🗑️ Hapus Riwayat Chat"):
        st.session_state.messages = []
        st.rerun()
    
    # Tampilkan animasi di sidebar
    if lottie_finance:
        st_lottie(lottie_finance, height=200, key="finance_anim")

# ==========================================
# 4. KONTEN UTAMA
# ==========================================

# Header Kustom
st.markdown('<p class="main-header">Hi there! 👋</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Siap merencanakan masa depan finansial yang gemilang?</p>', unsafe_allow_html=True)

if not user_api_key:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.warning("⚠️ **Akses Terkunci:** Silakan masukkan Google API Key Anda di sidebar sebelah kiri untuk membuka fitur analisis AI.")
        st.markdown("""
        **Cara Mendapatkan API Key:**
        1. Kunjungi [Google AI Studio](https://aistudio.google.com/).
        2. Login dengan akun Google Anda.
        3. Klik "Get API Key".
        4. Salin dan tempel di sidebar.
        """)
    with col2:
        # Tambahkan visual placeholder atau animasi
        pass
else:
    # KONFIGURASI GEMINI
    try:
        genai.configure(api_key=user_api_key)
        # Menggunakan Gemini 2.5 Flash
        model = genai.GenerativeModel('gemini-2.5-flash')
    except Exception as e:
        st.error(f"Gagal mengonfigurasi Gemini: {e}")
        st.stop()

    # FORM INPUT DATA
    st.markdown("### 📝 Data Keuangan Anda")
    with st.container():
        # Desain layout input yang rapi
        box_col1, box_col2, box_col3 = st.columns([1, 1, 1])
        
        with box_col1:
            st.markdown("#### 💰 Pendapatan")
            income = st.number_input("Pemasukan Bulanan (Rp)", min_value=0, step=100000, value=10000000)
            savings = st.number_input("Tabungan Saat Ini (Rp)", min_value=0, step=100000, value=5000000)

        with box_col2:
            st.markdown("#### 💸 Pengeluaran")
            expenses = st.number_input("Estimasi Pengeluaran (Rp)", min_value=0, step=100000, value=7000000)
            risk_tolerance = st.select_slider(
                "Toleransi Risiko Investasi",
                options=["Sangat Rendah", "Rendah", "Moderat", "Tinggi", "Sangat Tinggi"],
                value="Moderat"
            )

        with box_col3:
            st.markdown("#### 🎯 Tujuan")
            goal = st.text_input("Tujuan Utama (Contoh: Dana Pensiun, Beli Mobil)", value="Dana Pendidikan Anak")
            goal_amount = st.number_input("Target Dana Tujuan (Rp)", min_value=0, step=1000000, value=200000000)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # TOMBOL ANALISIS
    analyze_btn = st.button("Hasilkan Rencana Finansial ✨")

    # LOGIKA ANALISIS
    if analyze_btn:
        st.divider()
        
        # VALIDASI DASAR
        if income == 0:
            st.error("Mohon masukkan pendapatan bulanan Anda.")
        elif expenses > income:
            st.warning("Peringatan: Pengeluaran Anda lebih besar dari pendapatan. AI akan fokus pada strategi pengurangan utang.")
        
        # PROSES ANALISIS DENGAN ANIMASI
        with st.spinner(""):
            # Tampilkan animasi loading yang smooth
            loading_col1, loading_col2, loading_col3 = st.columns([1,2,1])
            with loading_col2:
                if lottie_loading:
                    st_lottie(lottie_loading, height=200, key="loading_anim")
                st.markdown("<p style='text-align: center; color: #6a6e7c;'>Gemini 2.5 Flash sedang meracik strategi terbaik...</p>", unsafe_allow_html=True)
            
            # Perhitungan Dasar untuk Chart
            surplus = income - expenses
            if surplus < 0: surplus = 0
            
            # Membuat Chart Alokasi Saat Ini
            labels_chart = ['Pengeluaran', 'Sisa (Surplus)']
            values_chart = [expenses, surplus]
            colors_chart = ['#FF4B4B', '#00d1b2'] # Merah untuk pengeluaran, Toska untuk sisa
            
            fig = create_budget_chart(labels_chart, values_chart, colors_chart)

            # PROMPT UNTUK GEMINI 2.5 FLASH
            # Prompt dibuat lebih spesifik agar outputnya terstruktur
            prompt = f"""
            Anda adalah perencana keuangan profesional senior yang bijaksana dan solutif.
            Analisis data berikut dengan cepat menggunakan kemampuan penalaran Anda:
            - Pendapatan: Rp{income}
            - Pengeluaran saat ini: Rp{expenses}
            - Tabungan saat ini: Rp{savings}
            - Tujuan Finansial: {goal}
            - Target Dana Tujuan: Rp{goal_amount}
            - Toleransi Risiko: {risk_tolerance}

            Sajikan rencana dalam format Markdown yang sangat rapi, menggunakan emoji, dan dibagi menjadi bagian-bagian berikut:

            ### 1️⃣ Evaluasi Kesehatan Keuangan
            (Berikan analisis singkat tentang rasio pengeluaran vs pendapatan. Apakah sehat?)

            ### 2️⃣ Rekomendasi Alokasi Anggaran (Metode 50/30/20 Modifikasi)
            (Sarankan alokasi Kebutuhan Pokok, Keinginan, dan Tabungan/Investasi dalam Rupiah dan Persentase).

            ### 3️⃣ Strategi Pencapaian Tujuan ({goal})
            (Hitung estimasi waktu mencapai target dana dengan sisa pendapatan saat ini. Berikan rekomendasi instrumen investasi yang cocok untuk toleransi risiko {risk_tolerance}).

            ### 4️⃣ Tips Spesifik 'Actionable'
            (Berikan 3 tips konkret untuk menghemat pengeluaran atau meningkatkan pendapatan sesuai profit pengguna).
            """

            try:
                # Memanggil Gemini 2.5 Flash
                response = model.generate_content(prompt)
                
                # MENAMPILKAN HASIL
                st.markdown("## 📊 Hasil Analisis ZeniFi AI")
                
                res_col1, res_col2 = st.columns([1, 2])
                
                with res_col1:
                    st.markdown("#### Alokasi Dana Saat Ini")
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Tampilkan metrik ringkas
                    st.metric(label="Sisa Dana (Surplus)", value=f"Rp{surplus:,}", delta=f"{ (surplus/income)*100:.1f}% dari Income" if income > 0 else "0%")

                with res_col2:
                    st.markdown(response.text)
                    
                st.balloons() # Animasi perayaan sukses

            except Exception as e:
                st.error(f"Terjadi kesalahan saat menghubungi Gemini AI: {e}")
