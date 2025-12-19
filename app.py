import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import plotly.express as px
from datetime import datetime

# -------------------------------------------------------
# ⚙️ KONFIGURASI AWAL
# -------------------------------------------------------
st.set_page_config(
    page_title="Rekap Pelanggaran & Prestasi Siswa",
    layout="wide",
    initial_sidebar_state="expanded"
)
# -------------------------------------------------------
# 🚫 HILANGKAN HEADER HITAM STREAMLIT
# -------------------------------------------------------
st.markdown("""
<style>
/* Hilangkan header hitam Streamlit */
header[data-testid="stHeader"] {
    display: none;
}

/* Hilangkan footer bawaan Streamlit */
footer {
    display: none;
}

/* Biar konten naik ke atas */
.block-container {
    padding-top: 1rem;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# 🎨 CSS MODERN & CLEAN
# -------------------------------------------------------
MODERN_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg-primary: #f8f9fa;
    --bg-secondary: #ffffff;
    --bg-tertiary: #f1f3f5;
    --primary: #2563eb;
    --primary-dark: #1e40af;
    --primary-light: #dbeafe;
    --text-primary: #1f2937;
    --text-secondary: #6b7280;
    --text-light: #9ca3af;
    --border: #e5e7eb;
    --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

* {
    font-family: 'Inter', sans-serif;
}

html, body, .stApp {
    background: var(--bg-primary);
    color: var(--text-primary);
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: var(--bg-secondary);
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] .stMarkdown {
    color: var(--text-primary) !important;
}

/* ===== TABS ===== */
.stTabs {
    background: var(--bg-secondary);
    border-radius: 12px;
    padding: 0.5rem;
    margin-bottom: 1.5rem;
    box-shadow: var(--shadow);
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
    background: transparent;
}

.stTabs [data-baseweb="tab"] {
    height: 50px;
    background: transparent;
    border-radius: 8px;
    color: var(--text-secondary) !important;
    font-weight: 500;
    padding: 0 1.5rem;
    border: none;
    transition: all 0.2s;
}

.stTabs [data-baseweb="tab"]:hover {
    background: var(--bg-tertiary);
    color: var(--text-primary) !important;
}

.stTabs [aria-selected="true"] {
    background: var(--primary) !important;
    color: white !important;
    font-weight: 600;
}

/* ===== HEADER ===== */
.main-header {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
    border-radius: 16px;
    padding: 2.5rem;
    margin-bottom: 2rem;
    box-shadow: var(--shadow-lg);
    position: relative;
    overflow: hidden;
}

.main-header::before {
    content: "";
    position: absolute;
    top: -50%;
    right: -10%;
    width: 300px;
    height: 300px;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 50%;
}

.main-header h1 {
    color: white !important;
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    letter-spacing: -0.5px;
}

.main-header p {
    color: rgba(255, 255, 255, 0.9) !important;
    font-size: 1rem;
    margin: 0;
}

/* ===== CARDS ===== */
.card {
    background: var(--bg-secondary);
    border-radius: 12px;
    padding: 1.8rem;
    margin-bottom: 1.5rem;
    box-shadow: var(--shadow);
    border: 1px solid var(--border);
}

/* ===== STAT BOX ===== */
.stat-box {
    background: var(--bg-secondary);
    border-radius: 12px;
    padding: 1.8rem;
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
    transition: transform 0.2s, box-shadow 0.2s;
}

.stat-box:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}

.stat-box .label {
    color: var(--text-secondary);
    font-size: 0.875rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.5rem;
}

.stat-box .value {
    color: var(--text-primary);
    font-size: 2.5rem;
    font-weight: 700;
    line-height: 1;
}

/* ===== FORMS & INPUTS ===== */
.stTextInput > div > div > input,
.stSelectbox > div > div > div,
.stNumberInput > div > div > input {
    background: var(--bg-secondary) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 8px !important;
    color: #000000 !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 0.75rem !important;
    transition: border-color 0.2s !important;
    font-weight: 600 !important;
    -webkit-text-fill-color: #000000 !important;
}

.stTextInput > div > div > input:focus,
.stSelectbox > div > div > div:focus-within,
.stNumberInput > div > div > input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1) !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}

/* Force text color untuk input text biasa */
.stTextInput input {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
}

/* Selectbox dropdown */
.stSelectbox > div > div > div[data-baseweb="select"] > div {
    background: var(--bg-secondary) !important;
    color: var(--text-primary) !important;
}

/* Selectbox arrow */
.stSelectbox svg {
    fill: var(--text-primary) !important;
}

/* Labels */
.stTextInput label,
.stSelectbox label,
.stNumberInput label,
.stRadio label {
    color: var(--text-primary) !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    margin-bottom: 0.5rem !important;
}

/* ===== RADIO BUTTONS ===== */
.stRadio {
    padding: 0.5rem 0;
}

.stRadio > label {
    color: var(--text-primary) !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    margin-bottom: 0.75rem !important;
}

.stRadio > div {
    background: var(--bg-secondary);
    padding: 1rem;
    border-radius: 10px;
    border: 1.5px solid var(--border);
}

.stRadio > div > label {
    display: flex;
    align-items: center;
    padding: 0.75rem 1rem;
    margin: 0 0.5rem 0 0;
    background: var(--bg-tertiary);
    border-radius: 8px;
    border: 2px solid transparent;
    transition: all 0.2s;
    cursor: pointer;
}

.stRadio > div > label:hover {
    background: var(--primary-light);
    border-color: var(--primary);
}

.stRadio > div > label > div:first-child {
    margin-right: 0.75rem;
}

.stRadio > div > label > div:last-child {
    color: var(--text-primary) !important;
    font-weight: 500 !important;
    font-size: 1rem !important;
}

.stRadio input[type="radio"]:checked + div {
    background: var(--primary) !important;
    color: white !important;
}

.stRadio input[type="radio"]:checked ~ label {
    background: var(--primary-light);
    border-color: var(--primary);
}

.stRadio input[type="radio"]:checked ~ label > div:last-child {
    color: var(--primary) !important;
    font-weight: 600 !important;
}

/* ===== BUTTONS ===== */
.stButton > button {
    background: var(--primary) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.2s !important;
    box-shadow: var(--shadow) !important;
}

.stButton > button:hover {
    background: var(--primary-dark) !important;
    transform: translateY(-1px);
    box-shadow: var(--shadow-lg) !important;
}

.stDownloadButton > button {
    background: var(--text-primary) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

/* ===== DATAFRAME ===== */
.stDataFrame {
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    overflow: hidden !important;
}

.stDataFrame [data-testid="stDataFrameResizable"] {
    border-radius: 8px !important;
}

/* ===== METRICS ===== */
.stMetric {
    background: var(--bg-secondary);
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid var(--border);
}

.stMetric label {
    color: var(--text-secondary) !important;
    font-size: 0.875rem !important;
}

.stMetric [data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    font-size: 1.5rem !important;
    font-weight: 700 !important;
}

/* ===== DIVIDER ===== */
hr {
    border: none;
    border-top: 1px solid var(--border);
    margin: 2rem 0;
}

/* ===== CAPTION ===== */
.stCaption {
    color: var(--text-light) !important;
    font-size: 0.85rem !important;
}

/* ===== INFO/WARNING/SUCCESS ===== */
.stAlert {
    border-radius: 8px !important;
    border: 1px solid var(--border) !important;
}

/* ===== EXPANDER ===== */
.streamlit-expanderHeader {
    background: var(--bg-tertiary) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-weight: 500 !important;
}

/* ===== SUBHEADER ===== */
h2, h3 {
    color: var(--text-primary) !important;
    font-weight: 600 !important;
}

/* ===== PODIUM ===== */
.podium-item {
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: transform 0.2s;
}

.podium-item:hover {
    transform: scale(1.02);
}

.podium-gold {
    background: linear-gradient(135deg, #dbeafe 0%, #93c5fd 100%);
    border-color: #2563eb;
}

.podium-silver {
    background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
    border-color: #9ca3af;
}

.podium-bronze {
    background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
    border-color: #f59e0b;
}

.podium-item h3 {
    margin: 0 0 0.5rem 0;
    color: var(--text-primary) !important;
    font-size: 1.25rem;
}

.podium-item p {
    margin: 0;
    color: var(--text-secondary) !important;
}

/* ===== FIX PLACEHOLDER TEXT ===== */
input::placeholder,
textarea::placeholder {
    color: #9ca3af !important;
    opacity: 1 !important;
    font-weight: 400 !important;
    -webkit-text-fill-color: #9ca3af !important;
}

/* Text yang diketik user - HITAM PEKAT */
.stTextInput input[type="text"],
.stTextInput input[type="search"],
.stNumberInput input[type="number"],
.stSelectbox input,
textarea {
    color: #000000 !important;
    font-weight: 600 !important;
    -webkit-text-fill-color: #000000 !important;
}

/* ===== FIX DISABLED INPUTS ===== */
input:disabled,
textarea:disabled {
    background: var(--bg-tertiary) !important;
    color: #6b7280 !important;
    cursor: not-allowed !important;
    font-weight: 400 !important;
    -webkit-text-fill-color: #6b7280 !important;
}

/* ===== PLOTLY CHARTS ===== */
.js-plotly-plot {
    border-radius: 8px;
    overflow: hidden;
}

/* =====================================
   HILANGKAN GARIS MERAH TAB (st.tabs)
===================================== */

/* Hilangkan underline default */
.stTabs [data-baseweb="tab"] {
    outline: none !important;
    box-shadow: none !important;
    border-bottom: none !important;
}

/* Saat aktif */
.stTabs [aria-selected="true"] {
    outline: none !important;
    box-shadow: none !important;
    border-bottom: none !important;
}

/* Fokus keyboard (yang bikin garis merah) */
.stTabs [data-baseweb="tab"]:focus,
.stTabs [data-baseweb="tab"]:focus-visible,
.stTabs [data-baseweb="tab"]:active {
    outline: none !important;
    box-shadow: none !important;
    border-bottom: none !important;
}

/* Pseudo-element bawaan BaseWeb */
.stTabs [data-baseweb="tab"]::after {
    display: none !important;
}

/* =====================================
   FIX TOTAL GARIS MERAH st.tabs (FINAL)
===================================== */

/* Hilangkan garis di container tab */
.stTabs [data-baseweb="tab-list"] {
    border-bottom: none !important;
    box-shadow: none !important;
}

/* Hilangkan indikator aktif bawaan BaseWeb */
.stTabs [data-baseweb="tab-highlight"] {
    display: none !important;
}

/* Extra safety: semua pseudo underline */
.stTabs *::before,
.stTabs *::after {
    box-shadow: none !important;
    border: none !important;
}


</style>
"""

st.markdown(MODERN_CSS, unsafe_allow_html=True)

# -------------------------------------------------------
# 📊 GOOGLE SHEETS SETUP
# -------------------------------------------------------
def get_gspread_client():
    """Inisialisasi client gspread"""
    SCOPE = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    creds_dict = st.secrets["GOOGLE_CREDENTIALS"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPE)
    client = gspread.authorize(creds)
    
    return client

@st.cache_data(ttl=300)
def load_data():
    """Load data dari Google Sheets dengan retry mechanism"""
    import time
    
    SPREADSHEET_ID = "1U-RPsmFwSwtdRkMdUlxsndpq15JtZHDulnkf-0v5gCc"
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            client = get_gspread_client()
            spreadsheet = client.open_by_key(SPREADSHEET_ID)
            
            ws_siswa = spreadsheet.worksheet("data_siswa")
            ws_rekap = spreadsheet.worksheet("rekap_pelanggaran")
            ws_pelanggaran = spreadsheet.worksheet("pelanggaran")
            ws_prestasi = spreadsheet.worksheet("prestasi")

            # Load semua data
            all_siswa = ws_siswa.get_all_values()
            all_rekap = ws_rekap.get_all_values()
            all_pelanggaran = ws_pelanggaran.get_all_values()
            all_prestasi = ws_prestasi.get_all_values()

            # Data siswa
            if len(all_siswa) <= 1:
                df_siswa = pd.DataFrame(columns=["Nama", "Kelas", "NIS"])
            else:
                df_siswa = pd.DataFrame(all_siswa[1:], columns=all_siswa[0])
                df_siswa.columns = df_siswa.columns.str.strip()

            # Data rekap pelanggaran
            if len(all_rekap) <= 1:
                df_rekap = pd.DataFrame(columns=[
                    "Tanggal", "Nama Siswa", "Kelas", "Jenis", "Deskripsi",
                    "Poin", "Poin Kumulatif"
                ])
            else:
                df_rekap = pd.DataFrame(all_rekap[1:], columns=all_rekap[0])
                df_rekap.columns = df_rekap.columns.str.strip()
                for col in ["Poin", "Poin Kumulatif"]:
                    if col in df_rekap.columns:
                        df_rekap[col] = pd.to_numeric(df_rekap[col], errors='coerce').fillna(0)

            # Database pelanggaran
            if len(all_pelanggaran) <= 1:
                df_db_pelanggaran = pd.DataFrame(columns=["Nama Pelanggaran", "Poin", "Kategori"])
            else:
                df_db_pelanggaran = pd.DataFrame(all_pelanggaran[1:], columns=all_pelanggaran[0])
                df_db_pelanggaran.columns = df_db_pelanggaran.columns.str.strip()
                
                col_mapping = {}
                for col in df_db_pelanggaran.columns:
                    col_lower = col.lower()
                    if 'nama' in col_lower and 'pelanggaran' in col_lower:
                        col_mapping[col] = 'Nama Pelanggaran'
                    elif 'poin' in col_lower:
                        col_mapping[col] = 'Poin'
                    elif 'kategori' in col_lower:
                        col_mapping[col] = 'Kategori'
                if col_mapping:
                    df_db_pelanggaran.rename(columns=col_mapping, inplace=True)
                
                if "Poin" in df_db_pelanggaran.columns:
                    df_db_pelanggaran["Poin"] = pd.to_numeric(df_db_pelanggaran["Poin"], errors='coerce').fillna(0)

            # Database prestasi
            if len(all_prestasi) <= 1:
                df_db_prestasi = pd.DataFrame(columns=["Nama Prestasi", "Poin", "Kategori"])
            else:
                df_db_prestasi = pd.DataFrame(all_prestasi[1:], columns=all_prestasi[0])
                df_db_prestasi.columns = df_db_prestasi.columns.str.strip()
                
                col_mapping = {}
                for col in df_db_prestasi.columns:
                    col_lower = col.lower()
                    if 'nama' in col_lower and 'prestasi' in col_lower:
                        col_mapping[col] = 'Nama Prestasi'
                    elif 'poin' in col_lower:
                        col_mapping[col] = 'Poin'
                    elif 'kategori' in col_lower:
                        col_mapping[col] = 'Kategori'
                if col_mapping:
                    df_db_prestasi.rename(columns=col_mapping, inplace=True)
                
                if "Poin" in df_db_prestasi.columns:
                    df_db_prestasi["Poin"] = pd.to_numeric(df_db_prestasi["Poin"], errors='coerce').fillna(0)

            return df_siswa, df_rekap, df_db_pelanggaran, df_db_prestasi
            
        except Exception as e:
            if attempt < max_retries - 1:
                st.warning(f"Koneksi gagal (percobaan {attempt + 1}/{max_retries}), mencoba lagi...")
                time.sleep(2)
            else:
                st.error(f"Gagal memuat data: {e}")
                st.info("""**Solusi:**
                1. Pastikan Anda sudah membuat 4 sheets
                2. Cek koneksi internet
                3. Refresh halaman
                """)
                st.stop()

df_siswa, df_rekap, df_db_pelanggaran, df_db_prestasi = load_data()

# 🧭 TOP NAVIGATION (TABS)
page = st.tabs([
    "Beranda",
    "Tambah Data",
    "Lihat Data",
    "Kelola Siswa",
    "Ranking",
    "Pelanggaran",
    "Prestasi"
])

# -------------------------------------------------------
# 🏠 HALAMAN BERANDA
# -------------------------------------------------------
with page[0]:
    st.markdown(f"""
    <div class='main-header'>
        <h1>Sistem Pelanggaran & Prestasi Siswa</h1>
        <p>Kelola pelanggaran dan prestasi siswa SMA Al-Falah Darmo • Update terakhir: {datetime.now().strftime('%d %B %Y, %H:%M')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class='stat-box'>
            <div class='label'>Total Siswa</div>
            <div class='value'>{len(df_siswa)}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        pelanggaran_count = len(df_rekap[df_rekap.get('Jenis', '') == 'Pelanggaran']) if not df_rekap.empty else 0
        st.markdown(f"""
        <div class='stat-box'>
            <div class='label'>Pelanggaran</div>
            <div class='value'>{pelanggaran_count}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        prestasi_count = len(df_rekap[df_rekap.get('Jenis', '') == 'Prestasi']) if not df_rekap.empty else 0
        st.markdown(f"""
        <div class='stat-box'>
            <div class='label'>Prestasi</div>
            <div class='value'>{prestasi_count}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        if not df_rekap.empty and 'Poin Kumulatif' in df_rekap.columns:
            df_temp = df_rekap.copy()
            df_temp['Poin Kumulatif'] = pd.to_numeric(df_temp['Poin Kumulatif'], errors='coerce').fillna(0)
            latest_poin = df_temp.groupby('Nama Siswa')['Poin Kumulatif'].last()
            avg_poin = latest_poin.mean() if len(latest_poin) > 0 else 0
        else:
            avg_poin = 0
            
        st.markdown(f"""
        <div class='stat-box'>
            <div class='label'>Rata-rata Poin</div>
            <div class='value'>{avg_poin:.1f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    if not df_rekap.empty and 'Kelas' in df_rekap.columns:
        st.subheader("📊 Distribusi Poin per Kelas")
        df_temp = df_rekap.copy()
        df_temp['Poin'] = pd.to_numeric(df_temp['Poin'], errors='coerce').fillna(0)
        df_grouped = df_temp.groupby('Kelas')['Poin'].sum().reset_index()
        df_grouped.columns = ['Kelas', 'Total Poin']
        fig = px.bar(
            df_grouped, x='Kelas', y='Total Poin',
            color='Total Poin',
            color_continuous_scale='Blues'
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🕐 Aktivitas Terbaru")
        if not df_rekap.empty:
            recent = df_rekap[['Tanggal', 'Nama Siswa', 'Jenis', 'Deskripsi', 'Poin']].tail(5)
            st.dataframe(recent, use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada aktivitas")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("👥 Total Poin Per Siswa")
        if not df_rekap.empty:
            df_temp = df_rekap.copy()
            df_temp['Poin Kumulatif'] = pd.to_numeric(df_temp['Poin Kumulatif'], errors='coerce').fillna(0)
            summary = df_temp.groupby('Nama Siswa').agg({
                'Poin Kumulatif': 'last',
                'Kelas': 'last'
            }).reset_index()
            summary.columns = ['Nama Siswa', 'Total Poin', 'Kelas']
            summary = summary.sort_values('Total Poin', ascending=False).head(5)
            st.dataframe(summary, use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada data siswa")
        st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------
# ➕ HALAMAN TAMBAH DATA
# -------------------------------------------------------
with page[1]:
    st.markdown("""
    <div class='main-header'>
        <h1>➕ Tambah Data Baru</h1>
        <p>Input pelanggaran atau prestasi siswa</p>
    </div>
    """, unsafe_allow_html=True)

    if df_siswa.empty:
        st.warning("⚠️ Daftar siswa kosong. Silakan tambahkan siswa terlebih dahulu di tab 'Kelola Siswa'.")
    else:
        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.markdown("""
        <div style='margin-bottom: 1.5rem;'>
            <label style='color: #1f2937; font-weight: 600; font-size: 1rem; display: block; margin-bottom: 0.75rem;'>
                📝 Pilih Jenis Data
            </label>
        </div>
        """, unsafe_allow_html=True)

        jenis = st.radio(
            "jenis_label",
            ["Pelanggaran", "Prestasi"],
            horizontal=True,
            label_visibility="collapsed"
        )

        with st.form("form_tambah"):
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("""
                <label style='color: #1f2937; font-weight: 600; font-size: 0.95rem; display: block; margin-bottom: 0.5rem;'>
                    Nama Siswa
                </label>
                """, unsafe_allow_html=True)
                
                nama = st.selectbox(
                    "Nama Siswa",
                    options=df_siswa["Nama"].tolist(),
                    index=None,
                    placeholder="Ketik nama siswa...",
                    label_visibility="collapsed"
                )

                kelas = ""
                if nama:
                    kelas = df_siswa.loc[df_siswa["Nama"] == nama, "Kelas"].values[0]

                st.markdown("""
                <label style='color: #1f2937; font-weight: 600; font-size: 0.95rem; display: block; margin-bottom: 0.5rem; margin-top: 1rem;'>
                    🏫 Kelas
                </label>
                """, unsafe_allow_html=True)
                
                st.text_input("Kelas", value=kelas, disabled=True, label_visibility="collapsed")

            with col2:
                selected = None
                poin_otomatis = 0

                if jenis == "Pelanggaran" and not df_db_pelanggaran.empty:
                    st.markdown("""
                    <label style='color: #1f2937; font-weight: 600; font-size: 0.95rem; display: block; margin-bottom: 0.5rem;'>
                        Pilih Pelanggaran
                    </label>
                    """, unsafe_allow_html=True)
                    
                    selected = st.selectbox(
                        "Pilih Pelanggaran",
                        options=df_db_pelanggaran["Nama Pelanggaran"].tolist(),
                        index=None,
                        placeholder="Ketik jenis pelanggaran...",
                        key="select_pelanggaran",
                        label_visibility="collapsed"
                    )

                    if selected:
                        poin_otomatis = int(
                            df_db_pelanggaran.loc[
                                df_db_pelanggaran["Nama Pelanggaran"] == selected,
                                "Poin"
                            ].values[0]
                        )

                elif jenis == "Prestasi" and not df_db_prestasi.empty:
                    st.markdown("""
                    <label style='color: #1f2937; font-weight: 600; font-size: 0.95rem; display: block; margin-bottom: 0.5rem;'>
                        ⭐ Pilih Prestasi
                    </label>
                    """, unsafe_allow_html=True)
                    
                    selected = st.selectbox(
                        "Pilih Prestasi",
                        options=df_db_prestasi["Nama Prestasi"].tolist(),
                        index=None,
                        placeholder="Ketik jenis prestasi...",
                        key="select_prestasi",
                        label_visibility="collapsed"
                    )

                    if selected:
                        poin_otomatis = int(
                            df_db_prestasi.loc[
                                df_db_prestasi["Nama Prestasi"] == selected,
                                "Poin"
                            ].values[0]
                        )

                st.markdown("""
                <label style='color: #1f2937; font-weight: 600; font-size: 0.95rem; display: block; margin-bottom: 0.5rem; margin-top: 1rem;'>
                    🎯 Poin (otomatis)
                </label>
                """, unsafe_allow_html=True)
                
                st.number_input(
                    "Poin (otomatis)",
                    value=poin_otomatis,
                    disabled=True,
                    label_visibility="collapsed"
                )
            
            st.markdown("<br>", unsafe_allow_html=True)

            submit = st.form_submit_button("💾 Simpan Data", use_container_width=True)

            if submit:
                if not nama:
                    st.error("❌ Pilih nama siswa terlebih dahulu!")
                elif not selected:
                    st.error(f"❌ Pilih {jenis.lower()} terlebih dahulu!")
                else:
                    poin_input = -poin_otomatis if jenis == "Pelanggaran" else poin_otomatis

                    client = get_gspread_client()
                    spreadsheet = client.open_by_key("1U-RPsmFwSwtdRkMdUlxsndpq15JtZHDulnkf-0v5gCc")
                    ws_rekap = spreadsheet.worksheet("rekap_pelanggaran")

                    records = ws_rekap.get_all_values()

                    poin_sebelum = 0
                    if len(records) > 1:
                        df_temp = pd.DataFrame(records[1:], columns=records[0])
                        df_temp["Poin Kumulatif"] = pd.to_numeric(
                            df_temp["Poin Kumulatif"], errors="coerce"
                        ).fillna(0)

                        siswa_data = df_temp[df_temp["Nama Siswa"] == nama]
                        if not siswa_data.empty:
                            poin_sebelum = int(siswa_data.iloc[-1]["Poin Kumulatif"])

                    poin_baru = poin_sebelum + poin_input

                    ws_rekap.append_row([
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        nama,
                        kelas,
                        jenis,
                        selected,
                        poin_input,
                        poin_baru
                    ])

                    st.success("✅ Data berhasil disimpan!")
                    st.cache_data.clear()
                    st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------
# 📋 HALAMAN LIHAT DATA
# -------------------------------------------------------
with page[2]:
    st.markdown("""
    <div class='main-header'>
        <h1>📋 Data Rekap</h1>
        <p>Lihat, filter, dan export data</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📝 Riwayat Transaksi", "📊 Total Poin Per Siswa"])
    
    with tab1:
        if df_rekap.empty:
            st.info("📭 Belum ada data transaksi")
        else:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                search = st.text_input("🔍 Cari nama atau deskripsi", "")
            
            with col2:
                kelas_filter = st.selectbox("Kelas", ["Semua"] + sorted(df_rekap['Kelas'].unique().tolist()))
            
            with col3:
                jenis_filter = st.selectbox("Jenis", ["Semua", "Pelanggaran", "Prestasi"])
            
            df_filtered = df_rekap.copy()
            
            if search:
                df_filtered = df_filtered[
                    df_filtered['Nama Siswa'].str.contains(search, case=False, na=False) |
                    df_filtered['Deskripsi'].str.contains(search, case=False, na=False)
                ]
            
            if kelas_filter != "Semua":
                df_filtered = df_filtered[df_filtered['Kelas'] == kelas_filter]
            
            if jenis_filter != "Semua":
                df_filtered = df_filtered[df_filtered['Jenis'] == jenis_filter]
            
            st.dataframe(df_filtered, use_container_width=True, hide_index=True)
            
            csv = df_filtered.to_csv(index=False)
            st.download_button(
                "📥 Export CSV",
                csv,
                f"rekap_transaksi_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv",
                use_container_width=True
            )
            
            st.caption(f"Menampilkan {len(df_filtered)} dari {len(df_rekap)} transaksi")
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        if df_rekap.empty:
            st.info("📭 Belum ada data siswa")
        else:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            
            df_temp = df_rekap.copy()
            df_temp['Poin Kumulatif'] = pd.to_numeric(df_temp['Poin Kumulatif'], errors='coerce').fillna(0)
            summary = df_temp.groupby(['Nama Siswa', 'Kelas']).agg({
                'Poin Kumulatif': 'last'
            }).reset_index()
            summary.columns = ['Nama Siswa', 'Kelas', 'Total Poin']
            summary = summary.sort_values('Total Poin', ascending=False)
            
            search_siswa = st.text_input("🔍 Cari nama siswa", "", key="search_summary")
            if search_siswa:
                summary = summary[summary['Nama Siswa'].str.contains(search_siswa, case=False, na=False)]
            
            st.dataframe(summary, use_container_width=True, hide_index=True)
            
            csv_summary = summary.to_csv(index=False)
            st.download_button(
                "📥 Export Summary CSV",
                csv_summary,
                f"summary_poin_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv",
                use_container_width=True
            )
            
            st.caption(f"Menampilkan {len(summary)} siswa")
            st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------
# 👥 HALAMAN KELOLA SISWA
# -------------------------------------------------------
with page[3]:
    st.markdown("""
    <div class='main-header'>
        <h1>👥 Kelola Siswa</h1>
        <p>Manajemen data siswa</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📋 Daftar Siswa")
        
        search = st.text_input("🔍 Cari siswa", "")
        df_filtered = df_siswa.copy()
        
        if search:
            df_filtered = df_filtered[df_filtered['Nama'].str.contains(search, case=False, na=False)]
        
        st.dataframe(df_filtered, use_container_width=True, hide_index=True)
        
        if not df_siswa.empty:
            per_kelas = df_siswa['Kelas'].value_counts().to_dict()
            st.caption(f"📊 Distribusi: {per_kelas}")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("➕ Tambah Siswa Baru")
        
        with st.form("form_siswa"):
            new_nama = st.text_input("Nama Lengkap")
            new_kelas = st.text_input("Kelas (contoh: X-1, XI-2)")
            new_nis = st.text_input("NIS")
            
            submit = st.form_submit_button("💾 Simpan", use_container_width=True)
            
            if submit and all([new_nama.strip(), new_kelas.strip(), new_nis.strip()]):
                try:
                    client = get_gspread_client()
                    spreadsheet = client.open_by_key("1U-RPsmFwSwtdRkMdUlxsndpq15JtZHDulnkf-0v5gCc")
                    ws_siswa_write = spreadsheet.worksheet("data_siswa")
                    
                    ws_siswa_write.append_row([new_nama, new_kelas, new_nis])
                    st.success(f"✅ {new_nama} berhasil ditambahkan!")
                    st.cache_data.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Gagal: {e}")
            elif submit:
                st.warning("⚠️ Lengkapi semua field!")
        
        st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------
# 🏆 HALAMAN RANKING
# -------------------------------------------------------
with page[4]:
    st.markdown("""
    <div class='main-header'>
        <h1>🏆 Ranking Siswa</h1>
        <p>Leaderboard berdasarkan total poin</p>
    </div>
    """, unsafe_allow_html=True)
    
    if df_rekap.empty:
        st.warning("📭 Belum ada data untuk ranking")
    else:
        df_temp = df_rekap.copy()
        df_temp['Poin Kumulatif'] = pd.to_numeric(df_temp['Poin Kumulatif'], errors='coerce').fillna(0)
        
        ranking = df_temp.groupby('Nama Siswa').agg({
            'Poin Kumulatif': 'last',
            'Kelas': 'last'
        }).reset_index()
        ranking.columns = ['Nama Siswa', 'Total Poin', 'Kelas']
        ranking = ranking.sort_values('Total Poin', ascending=False).reset_index(drop=True)
        
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("🥇 Top 3 Performer")
        
        podium_classes = ["podium-gold", "podium-silver", "podium-bronze"]
        medals = ["🥇", "🥈", "🥉"]
        
        for idx, row in ranking.head(3).iterrows():
            st.markdown(f"""
            <div class='podium-item {podium_classes[idx]}'>
                <h3>{medals[idx]} {row['Nama Siswa']}</h3>
                <p>Total Poin: <strong>{row['Total Poin']:.0f}</strong> | Kelas: {row['Kelas']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📊 Ranking Lengkap")
        st.dataframe(ranking, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        fig = px.bar(
            ranking.head(10), x='Nama Siswa', y='Total Poin',
            color='Total Poin',
            color_continuous_scale='Blues',
            title="Top 10 Siswa"
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=500,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("👑 Siswa Terbaik", ranking.iloc[0]['Nama Siswa'])
        with col2:
            st.metric("📈 Poin Tertinggi", f"{ranking.iloc[0]['Total Poin']:.0f}")

# -------------------------------------------------------
# ⚠️ HALAMAN DATABASE PELANGGARAN
# -------------------------------------------------------
with page[5]:
    st.markdown("""
    <div class='main-header'>
        <h1>⚠️ Database Pelanggaran</h1>
        <p>Kelola daftar pelanggaran dan poinnya</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📋 Daftar Pelanggaran")
        
        if df_db_pelanggaran.empty:
            st.info("📭 Database pelanggaran kosong")
        else:
            search = st.text_input("🔍 Cari pelanggaran", "", key="search_pelang")
            df_filtered = df_db_pelanggaran.copy()
            
            if search:
                df_filtered = df_filtered[df_filtered['Nama Pelanggaran'].str.contains(search, case=False, na=False)]
            
            st.dataframe(df_filtered, use_container_width=True, hide_index=True)
            st.caption(f"Total: {len(df_db_pelanggaran)} jenis pelanggaran")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("➕ Tambah Pelanggaran")
        
        with st.form("form_pelanggaran"):
            nama_pelang = st.text_input("Nama Pelanggaran")
            poin_pelang = st.number_input("Poin (positif)", min_value=1, value=10)
            kategori_pelang = st.selectbox("Kategori", [
                "Ringan", "Sedang", "Berat", "Sangat Berat"
            ])
            
            st.info("ℹ️ Poin akan disimpan sebagai nilai positif, tapi dikurangi saat input ke siswa")
            
            submit = st.form_submit_button("💾 Simpan", use_container_width=True)
            
            if submit and nama_pelang.strip():
                try:
                    client = get_gspread_client()
                    spreadsheet = client.open_by_key("1U-RPsmFwSwtdRkMdUlxsndpq15JtZHDulnkf-0v5gCc")
                    ws_pelang_write = spreadsheet.worksheet("pelanggaran")
                    
                    ws_pelang_write.append_row([nama_pelang, int(poin_pelang), kategori_pelang])
                    st.success(f"✅ Pelanggaran '{nama_pelang}' berhasil ditambahkan!")
                    st.cache_data.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Gagal: {e}")
            elif submit:
                st.warning("⚠️ Isi nama pelanggaran!")
        
        st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------
# ⭐ HALAMAN DATABASE PRESTASI
# -------------------------------------------------------
with page[6]:
    st.markdown("""
    <div class='main-header'>
        <h1>⭐ Database Prestasi</h1>
        <p>Kelola daftar prestasi dan poinnya</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("📋 Daftar Prestasi")
        
        if df_db_prestasi.empty:
            st.info("📭 Database prestasi kosong")
        else:
            search = st.text_input("🔍 Cari prestasi", "", key="search_pres")
            df_filtered = df_db_prestasi.copy()
            
            if search:
                df_filtered = df_filtered[df_filtered['Nama Prestasi'].str.contains(search, case=False, na=False)]
            
            st.dataframe(df_filtered, use_container_width=True, hide_index=True)
            st.caption(f"Total: {len(df_db_prestasi)} jenis prestasi")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("➕ Tambah Prestasi")
        
        with st.form("form_prestasi"):
            nama_pres = st.text_input("Nama Prestasi")
            poin_pres = st.number_input("Poin (positif)", min_value=1, value=20)
            kategori_pres = st.selectbox("Kategori", [
                "Akademik", "Non-Akademik", "Olahraga", "Seni", "Kepemimpinan", "Lainnya"
            ])
            
            st.info("ℹ️ Poin akan ditambahkan ke total siswa saat input")
            
            submit = st.form_submit_button("💾 Simpan", use_container_width=True)
            
            if submit and nama_pres.strip():
                try:
                    client = get_gspread_client()
                    spreadsheet = client.open_by_key("1U-RPsmFwSwtdRkMdUlxsndpq15JtZHDulnkf-0v5gCc")
                    ws_pres_write = spreadsheet.worksheet("prestasi")
                    
                    ws_pres_write.append_row([nama_pres, int(poin_pres), kategori_pres])
                    st.success(f"✅ Prestasi '{nama_pres}' berhasil ditambahkan!")
                    st.cache_data.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Gagal: {e}")
            elif submit:
                st.warning("⚠️ Isi nama prestasi!")
        
        st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------
# FOOTER
# -------------------------------------------------------
st.divider()
st.markdown(
    f"<div style='text-align: center; color: #9ca3af; padding: 1rem; font-size: 0.9rem;'>"
    f"📊 Dashboard Siswa v4.0 • Dibuat dengan ❤️ untuk SMA Al-Falah Darmo<br>"
    f"Update terakhir: {datetime.now().strftime('%d %B %Y, %H:%M:%S')}"
    f"</div>",
    unsafe_allow_html=True
)
