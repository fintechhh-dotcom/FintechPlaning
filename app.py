import streamlit as st
import google.generativeai as genai
import plotly.graph_objects as go
import requests
from streamlit_lottie import st_lottie

# Konfigurasi Halaman
st.set_page_config(page_title="Fintech AI", page_icon="💹", layout="wide")

# CSS Kustom
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .stButton>button {
        width: 100%; border-radius: 12px; height: 3.5em;
        background: linear-gradient(90deg, #00C9FF 0%, #92FE9D 100%);
        color: #1E1E1E; font-weight: 700; border: none; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.01); }
    
    .chat-bubble {
        padding: 1.5rem; border-radius: 15px; background-color: #f0f2f6;
        margin-bottom: 1rem; border-left: 5px solid #00C9FF;
    }
    </style>
    """, unsafe_allow_html=True)

# Fungsi Animasi
def load_lottieurl(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

lottie_loading = load_lottieurl("https://assets1.lottiefiles.com/private_files/lf30_fkw8v5ba.json")

# Inisialisasi Riwayat Chat di Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("# 🛡️ Fintech Access")
    user_api_key = st.text_input("Google API Key", type="password")
    
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

# --- MAIN UI ---
st.title("💹 Fintech AI Planner")
st.markdown("Analisis finansial cerdas berbasis **Gemini 2.5 Flash**.")

if not user_api_key:
    st.info("Silakan masukkan API Key di sidebar untuk memulai.")
else:
    genai.configure(api_key=user_api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')

    # Input Form
    with st.expander("📝 Form Input Data Baru", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            income = st.number_input("Pemasukan (Rp)", min_value=0, value=10000000)
            savings = st.number_input("Tabungan (Rp)", min_value=0, value=5000000)
        with c2:
            expenses = st.number_input("Pengeluaran (Rp)", min_value=0, value=7000000)
            risk = st.select_slider("Risiko", ["Rendah", "Moderat", "Tinggi"])
        with c3:
            goal = st.text_input("Tujuan", value="Investasi Rumah")
            target = st.number_input("Target Dana (Rp)", min_value=0, value=100000000)

    if st.button("PROSES ANALISIS BARU"):
        with st.spinner(""):
            surplus = max(0, income - expenses)
            prompt = f"Berikan analisis finansial profesional singkat untuk Income: {income}, Expense: {expenses}, Goal: {goal}, Target: {target}, Risiko: {risk}. Sertakan tabel alokasi anggaran."
            
            try:
                response = model.generate_content(prompt)
                # Simpan ke riwayat
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response.text,
                    "chart_data": [expenses, surplus],
                    "goal_name": goal
                })
                st.snow()
            except Exception as e:
                st.error("API Key tidak valid atau terjadi gangguan koneksi.")

    # --- DISPLAY RIWAYAT CHAT ---
    st.markdown("---")
    st.subheader("📜 Riwayat Analisis")
    
    for idx, msg in enumerate(reversed(st.session_state.messages)):
        with st.container():
            st.markdown(f"#### Analisis #{len(st.session_state.messages) - idx}: {msg['goal_name']}")
            res_col1, res_col2 = st.columns([1, 2])
            
            with res_col1:
                fig = go.Figure(data=[go.Pie(labels=['Pengeluaran', 'Sisa'], 
                                           values=msg['chart_data'], 
                                           hole=.6,
                                           marker_colors=['#FF4B4B', '#00C9FF'])])
                fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0), height=200)
                st.plotly_chart(fig, use_container_width=True, key=f"chart_{idx}")
            
            with res_col2:
                st.markdown(f'<div class="chat-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
            st.divider()
