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
# 🎨 CSS DARK THEME PREMIUM (REFINED)
# -------------------------------------------------------
DARK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

:root {
    --primary: #667eea;
    --primary-dark: #5a67d8;
    --secondary: #48bb78;
    --accent: #ed8936;
    --bg-main: #0f172a;
    --bg-card: #1e293b;
    --bg-sidebar: #1a202c;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --border: #334155;
    --shadow: rgba(0, 0, 0, 0.3);
}

html, body, .main, .stApp {
    background: var(--bg-main) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif;
    font-weight: 400;
}

/* Sidebar Styling */
section[data-testid="stSidebar"] {
    background: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border);
}

section[data-testid="stSidebar"] > div {
    background: transparent;
    padding: 2rem 1rem;
}

section[data-testid="stSidebar"] h2 {
    color: var(--primary);
    font-size: 1.4rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
    letter-spacing: -0.5px;
}

section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stRadio label {
    color: var(--text-primary) !important;
    font-weight: 500;
    font-size: 0.875rem;
    letter-spacing: 0.025em;
}

section[data-testid="stSidebar"] [data-baseweb="select"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px;
}

section[data-testid="stSidebar"] button {
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.65rem 1rem;
    font-weight: 600;
    transition: all 0.3s ease;
    width: 100%;
    font-size: 0.9rem;
}

section[data-testid="stSidebar"] button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
}

/* Main Header with Animation */
.main-header {
    background: linear-gradient(135deg, var(--bg-card) 0%, #2d3748 100%);
    padding: 2rem 2.5rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    border: 1px solid var(--border);
    box-shadow: 0 4px 24px var(--shadow);
    position: relative;
    overflow: hidden;
}

.main-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
    animation: shine 3s infinite;
}

@keyframes shine {
    0% { left: -100%; }
    100% { left: 100%; }
}

.main-header h1 {
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 2rem;
    font-weight: 700;
    margin: 0;
    letter-spacing: -1px;
}

.main-header p {
    color: var(--text-secondary);
    margin: 0.75rem 0 0 0;
    font-size: 0.95rem;
    font-weight: 400;
}

/* Card Styling */
.card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.75rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 12px var(--shadow);
    transition: all 0.3s ease;
}

.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.4);
    border-color: var(--primary);
}

.card h2, .card h3 {
    color: var(--text-primary);
    margin-bottom: 1rem;
    font-weight: 600;
    font-size: 1.25rem;
    letter-spacing: -0.5px;
}

/* Stat Box with Gradient */
.stat-box {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    text-align: center;
    box-shadow: 0 2px 12px var(--shadow);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.stat-box::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--primary), var(--secondary));
}

.stat-box:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
}

.stat-box .label {
    font-size: 0.85rem;
    color: var(--text-secondary);
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.5rem;
}

.stat-box .value {
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-top: 0.5rem;
}

/* Form Inputs */
.stTextInput input, .stNumberInput input, .stSelectbox select {
    background: var(--bg-main) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    padding: 0.65rem !important;
    font-size: 0.9rem !important;
    transition: all 0.2s ease !important;
}

.stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
    outline: none !important;
}

.stTextInput label, .stNumberInput label, .stSelectbox label {
    color: var(--text-primary) !important;
    font-weight: 500 !important;
    margin-bottom: 0.5rem !important;
    font-size: 0.9rem !important;
}

/* Buttons */
.stButton button, .stDownloadButton button {
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    transition: all 0.3s ease;
    font-size: 0.9rem;
}

.stButton button:hover, .stDownloadButton button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

.stDownloadButton button {
    background: linear-gradient(135deg, var(--secondary), #38a169);
}

/* DataFrames */
.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid var(--border);
}

.stDataFrame table {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
}

.stDataFrame th {
    background: linear-gradient(135deg, var(--primary), var(--primary-dark)) !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 1rem !important;
    text-transform: uppercase;
    font-size: 0.85rem;
    letter-spacing: 0.5px;
}

.stDataFrame td {
    border-color: var(--border) !important;
    padding: 0.85rem !important;
    font-size: 0.9rem;
}

/* Metrics */
.stMetric {
    background: var(--bg-card);
    padding: 1.25rem;
    border-radius: 12px;
    border: 1px solid var(--border);
}

.stMetric label {
    color: var(--text-secondary) !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

.stMetric [data-testid="stMetricValue"] {
    color: var(--primary) !important;
    font-size: 1.75rem !important;
    font-weight: 700 !important;
}

/* Alerts */
.stAlert {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}

/* Divider */
hr {
    border-color: var(--border) !important;
    margin: 2rem 0 !important;
    opacity: 0.5;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: transparent;
}

.stTabs [data-baseweb="tab"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 8px;
    color: var(--text-secondary);
    padding: 0.75rem 1.5rem;
    font-weight: 500;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
    color: white;
    border-color: var(--primary);
}

/* Expander */
.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-weight: 500 !important;
}

/* Caption */
.caption {
    color: var(--text-secondary);
    font-size: 0.85rem;
    margin-top: 0.5rem;
    font-style: italic;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: var(--bg-main);
}

::-webkit-scrollbar-thumb {
    background: var(--border);
    border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--primary);
}

/* Podium Styles */
.podium-item {
    background: var(--bg-card);
    border: 2px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 0.5rem 0;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.podium-item:hover {
    transform: translateX(8px);
    border-color: var(--primary);
}

.podium-item::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 4px;
}

.podium-gold::before { background: #FFD700; }
.podium-silver::before { background: #C0C0C0; }
.podium-bronze::before { background: #CD7F32; }

.podium-item h3 {
    margin: 0;
    color: var(--text-primary);
    font-size: 1.25rem;
    font-weight: 600;
}

.podium-item p {
    margin: 0.5rem 0 0 0;
    color: var(--text-secondary);
    font-size: 0.95rem;
}

/* Radio Buttons */
.stRadio > div {
    flex-direction: row !important;
    gap: 1rem;
}

.stRadio label {
    color: var(--text-primary) !important;
}
</style>
"""

st.markdown(DARK_CSS, unsafe_allow_html=True)

# -------------------------------------------------------
# 🔐 GOOGLE SHEETS SETUP
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
                
                # Normalisasi nama kolom
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
                
                # Normalisasi nama kolom
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

            return df_siswa, df_rekap, df_db_pelanggaran, df_db_prestasi, ws_siswa, ws_rekap, ws_pelanggaran, ws_prestasi
            
        except Exception as e:
            if attempt < max_retries - 1:
                st.warning(f"Koneksi gagal (percobaan {attempt + 1}/{max_retries}), mencoba lagi...")
                time.sleep(2)
            else:
                st.error(f"Gagal memuat data: {e}")
                st.info("""**Solusi:**
                1. Pastikan Anda sudah membuat 4 sheets:
                   - `data_siswa` (kolom: Nama, Kelas, NIS)
                   - `rekap_pelanggaran` (kolom: Tanggal, Nama Siswa, Kelas, Jenis, Deskripsi, Poin, Poin Kumulatif)
                   - `pelanggaran` (kolom: Nama Pelanggaran, Poin, Kategori)
                   - `prestasi` (kolom: Nama Prestasi, Poin, Kategori)
                2. Cek koneksi internet
                3. Refresh halaman
                """)
                st.stop()

df_siswa, df_rekap, df_db_pelanggaran, df_db_prestasi, ws_siswa, ws_rekap, ws_pelanggaran, ws_prestasi = load_data()

# -------------------------------------------------------
# 🧭 SIDEBAR NAVIGATION
# -------------------------------------------------------
with st.sidebar:
    st.markdown("<h2>Dashboard Siswa</h2>", unsafe_allow_html=True)
    
    page = st.selectbox(
        "Pilih Menu",
        ["Beranda", "Tambah Data", "Lihat Data", "Kelola Siswa", 
         "Ranking", "Database Pelanggaran", "Database Prestasi"]
    )
    
    st.divider()
    
    if st.button("Refresh Data"):
        st.cache_data.clear()
        st.rerun()
    
    with st.expander("Informasi"):
        st.write("**Versi:** 3.2 Enhanced")
        st.write("**Data:** Real-time Google Sheets")
        st.write("**Update:** Auto-refresh 5 menit")

# -------------------------------------------------------
# 🏠 HALAMAN BERANDA
# -------------------------------------------------------
if page == "Beranda":
    st.markdown(f"""
    <div class='main-header'>
        <h1>Selamat Datang di Dashboard</h1>
        <p>Kelola pelanggaran dan prestasi siswa secara real-time • Update terakhir: {datetime.now().strftime('%d %B %Y, %H:%M')}</p>
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
        st.subheader("Distribusi Poin per Kelas")
        df_temp = df_rekap.copy()
        df_temp['Poin'] = pd.to_numeric(df_temp['Poin'], errors='coerce').fillna(0)
        df_grouped = df_temp.groupby('Kelas')['Poin'].sum().reset_index()
        df_grouped.columns = ['Kelas', 'Total Poin']
        fig = px.bar(
            df_grouped, x='Kelas', y='Total Poin',
            color='Total Poin',
            color_continuous_scale='Viridis',
            template='plotly_dark'
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#f1f5f9',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Aktivitas Terbaru (5 Terakhir)")
    if not df_rekap.empty:
        recent = df_rekap[['Tanggal', 'Nama Siswa', 'Jenis', 'Deskripsi', 'Poin']].tail(5)
        st.dataframe(recent, use_container_width=True, hide_index=True)
    else:
        st.info("Belum ada aktivitas")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Total Poin Per Siswa (Kumulatif Terkini)")
    if not df_rekap.empty:
        df_temp = df_rekap.copy()
        df_temp['Poin Kumulatif'] = pd.to_numeric(df_temp['Poin Kumulatif'], errors='coerce').fillna(0)
        summary = df_temp.groupby('Nama Siswa').agg({
            'Poin Kumulatif': 'last',
            'Kelas': 'last'
        }).reset_index()
        summary.columns = ['Nama Siswa', 'Total Poin', 'Kelas']
        summary = summary.sort_values('Total Poin', ascending=False)
        st.dataframe(summary, use_container_width=True, hide_index=True)
    else:
        st.info("Belum ada data siswa")
    st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------
# ➕ HALAMAN TAMBAH DATA
# -------------------------------------------------------
elif page == "Tambah Data":
    st.markdown("""
    <div class='main-header'>
        <h1>Tambah Data Baru</h1>
        <p>Input pelanggaran atau prestasi siswa dengan database terintegrasi</p>
    </div>
    """, unsafe_allow_html=True)
    
    if df_siswa.empty:
        st.warning("Daftar siswa kosong. Tambahkan siswa terlebih dahulu.")
    else:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        
        with st.form("form_tambah"):
            col1, col2 = st.columns(2)
            
            with col1:
                nama = st.selectbox("Nama Siswa", df_siswa["Nama"].tolist())
                if not df_siswa.empty and nama:
                    kelas_data = df_siswa[df_siswa["Nama"] == nama]["Kelas"]
                    kelas = kelas_data.values[0] if len(kelas_data) > 0 else ""
                else:
                    kelas = ""
                st.text_input("Kelas", value=kelas, disabled=True)
                
                jenis = st.radio("Jenis", ["Pelanggaran", "Prestasi"], horizontal=True)
            
            with col2:
                selected = ""
                poin_otomatis = 0
                
                if jenis == "Pelanggaran":
                    if not df_db_pelanggaran.empty and "Nama Pelanggaran" in df_db_pelanggaran.columns:
                        pelanggaran_list = df_db_pelanggaran["Nama Pelanggaran"].tolist()
                        if len(pelanggaran_list) > 0:
                            selected = st.selectbox(
                                "Pilih Pelanggaran", 
                                pelanggaran_list,
                                help="Ketik untuk mencari",
                                key="select_pelanggaran_input"
                            )
                            poin_row = df_db_pelanggaran[df_db_pelanggaran["Nama Pelanggaran"] == selected]
                            if len(poin_row) > 0:
                                poin_otomatis = float(poin_row["Poin"].values[0])
                            st.number_input("Poin (otomatis)", value=int(poin_otomatis), disabled=True, key="poin_pelang")
                        else:
                            st.warning("Database pelanggaran kosong")
                    else:
                        st.warning("Database pelanggaran kosong atau format salah")
                        st.info("Pastikan sheet 'pelanggaran' memiliki kolom: Nama Pelanggaran, Poin, Kategori")
                
                elif jenis == "Prestasi":
                    if not df_db_prestasi.empty and "Nama Prestasi" in df_db_prestasi.columns:
                        prestasi_list = df_db_prestasi["Nama Prestasi"].tolist()
                        if len(prestasi_list) > 0:
                            selected = st.selectbox(
                                "Pilih Prestasi", 
                                prestasi_list,
                                help="Ketik untuk mencari",
                                key="select_prestasi_input"
                            )
                            poin_row = df_db_prestasi[df_db_prestasi["Nama Prestasi"] == selected]
                            if len(poin_row) > 0:
                                poin_otomatis = float(poin_row["Poin"].values[0])
                            st.number_input("Poin (otomatis)", value=int(poin_otomatis), disabled=True, key="poin_pres")
                        else:
                            st.warning("Database prestasi kosong")
                    else:
                        st.warning("Database prestasi kosong atau format salah")
                        st.info("Pastikan sheet 'prestasi' memiliki kolom: Nama Prestasi, Poin, Kategori")
            
            # Hitung poin kumulatif
            if not df_rekap.empty and nama:
                df_siswa_rekap = df_rekap[df_rekap['Nama Siswa'] == nama]
                if len(df_siswa_rekap) > 0:
                    poin_kumulatif_sebelum = pd.to_numeric(df_siswa_rekap['Poin Kumulatif'].iloc[-1], errors='coerce')
                else:
                    poin_kumulatif_sebelum = 0
            else:
                poin_kumulatif_sebelum = 0
            
            # Poin baru: negatif untuk pelanggaran, positif untuk prestasi
            poin_input = -poin_otomatis if jenis == "Pelanggaran" else poin_otomatis
            poin_kumulatif_baru = poin_kumulatif_sebelum + poin_input
            
            st.info(f"**Poin Sebelum:** {poin_kumulatif_sebelum:+.0f} → **Poin Input:** {poin_input:+.0f} → **Total Poin Setelah:** {poin_kumulatif_baru:+.0f}")
            
            submit = st.form_submit_button("Simpan Data", use_container_width=True)
            
            if submit and selected and poin_otomatis > 0:
                try:
                    client = get_gspread_client()
                    spreadsheet = client.open_by_key("1U-RPsmFwSwtdRkMdUlxsndpq15JtZHDulnkf-0v5gCc")
                    ws_rekap_write = spreadsheet.worksheet("rekap_pelanggaran")
                    
                    tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    ws_rekap_write.append_row([
                        tanggal, 
                        nama, 
                        kelas, 
                        jenis,
                        selected,
                        float(poin_input),
                        float(poin_kumulatif_baru)
                    ])
                    st.success(f"Data berhasil disimpan untuk {nama}! Total poin sekarang: {poin_kumulatif_baru:+.0f}")
                    st.balloons()
                    st.cache_data.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"Gagal menyimpan: {e}")
            elif submit:
                st.warning("Pilih pelanggaran/prestasi terlebih dahulu!")
        
        st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------
# 📋 HALAMAN LIHAT DATA
# -------------------------------------------------------
elif page == "Lihat Data":
    st.markdown("""
    <div class='main-header'>
        <h1>Data Rekap</h1>
        <p>Lihat, filter, dan export data</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Riwayat Transaksi", "Total Poin Per Siswa"])
    
    with tab1:
        st.markdown("### Semua Riwayat Transaksi")
        if df_rekap.empty:
            st.info("Belum ada data")
        else:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                search = st.text_input("Cari nama atau deskripsi", "")
            
            with col2:
                kelas_filter = st.selectbox("Filter Kelas", ["Semua"] + sorted(df_rekap['Kelas'].unique().tolist()))
            
            with col3:
                jenis_filter = st.selectbox("Filter Jenis", ["Semua", "Pelanggaran", "Prestasi"])
            
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
                "Export CSV",
                csv,
                f"rekap_transaksi_{datetime.now().strftime('%Y%m%d')}.csv",
                "text/csv",
                use_container_width=True
            )
            
            st.caption(f"Menampilkan {len(df_filtered)} dari {len(df_rekap)} transaksi")
            st.markdown("</div>", unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### Total Poin Akumulatif Per Siswa")
        if df_rekap.empty:
            st.info("Belum ada data")
        else:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            
            df_temp = df_rekap.copy()
            df_temp['Poin Kumulatif'] = pd.to_numeric(df_temp['Poin Kumulatif'], errors='coerce').fillna(0)
            summary = df_temp.groupby(['Nama Siswa', 'Kelas']).agg({
                'Poin Kumulatif': 'last'
            }).reset_index()
            summary.columns = ['Nama Siswa', 'Kelas', 'Total Poin']
            summary = summary.sort_values('Total Poin', ascending=False)
            
            search_siswa = st.text_input("Cari nama siswa", "", key="search_summary")
            if search_siswa:
                summary = summary[summary['Nama Siswa'].str.contains(search_siswa, case=False, na=False)]
            
            st.dataframe(summary, use_container_width=True, hide_index=True)
            
            csv_summary = summary.to_csv(index=False)
            st.download_button(
                "Export Summary CSV",
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
elif page == "Kelola Siswa":
    st.markdown("""
    <div class='main-header'>
        <h1>Kelola Siswa</h1>
        <p>Manajemen data siswa</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Daftar Siswa")
        
        search = st.text_input("Cari siswa", "")
        df_filtered = df_siswa.copy()
        
        if search:
            df_filtered = df_filtered[df_filtered['Nama'].str.contains(search, case=False, na=False)]
        
        st.dataframe(df_filtered, use_container_width=True, hide_index=True)
        
        if not df_siswa.empty:
            per_kelas = df_siswa['Kelas'].value_counts().to_dict()
            st.caption(f"Distribusi: {per_kelas}")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Tambah Siswa")
        
        with st.form("form_siswa"):
            new_nama = st.text_input("Nama Lengkap")
            new_kelas = st.text_input("Kelas")
            new_nis = st.text_input("NIS")
            
            submit = st.form_submit_button("Simpan", use_container_width=True)
            
            if submit and all([new_nama.strip(), new_kelas.strip(), new_nis.strip()]):
                try:
                    client = get_gspread_client()
                    spreadsheet = client.open_by_key("1U-RPsmFwSwtdRkMdUlxsndpq15JtZHDulnkf-0v5gCc")
                    ws_siswa_write = spreadsheet.worksheet("data_siswa")
                    
                    ws_siswa_write.append_row([new_nama, new_kelas, new_nis])
                    st.success(f"{new_nama} berhasil ditambahkan!")
                    st.cache_data.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"Gagal: {e}")
            elif submit:
                st.warning("Lengkapi semua field!")
        
        st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------
# 🏆 HALAMAN RANKING
# -------------------------------------------------------
elif page == "Ranking":
    st.markdown("""
    <div class='main-header'>
        <h1>Ranking Siswa</h1>
        <p>Leaderboard berdasarkan total poin</p>
    </div>
    """, unsafe_allow_html=True)
    
    if df_rekap.empty:
        st.warning("Belum ada data untuk ranking")
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
        st.subheader("Top 3 Performer")
        
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
        st.subheader("Ranking Lengkap")
        st.dataframe(ranking, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        fig = px.bar(
            ranking.head(10), x='Nama Siswa', y='Total Poin',
            color='Total Poin',
            color_continuous_scale='RdYlGn',
            template='plotly_dark',
            title="Top 10 Siswa"
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#f1f5f9',
            height=500,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Siswa Terbaik", ranking.iloc[0]['Nama Siswa'])
        with col2:
            st.metric("Poin Tertinggi", f"{ranking.iloc[0]['Total Poin']:.0f}")

# -------------------------------------------------------
# 🗂️ HALAMAN DATABASE PELANGGARAN
# -------------------------------------------------------
elif page == "Database Pelanggaran":
    st.markdown("""
    <div class='main-header'>
        <h1>Database Pelanggaran</h1>
        <p>Kelola daftar pelanggaran dan poinnya</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Daftar Pelanggaran")
        
        if df_db_pelanggaran.empty:
            st.info("Database pelanggaran kosong")
        else:
            search = st.text_input("Cari pelanggaran", "", key="search_pelang")
            df_filtered = df_db_pelanggaran.copy()
            
            if search:
                df_filtered = df_filtered[df_filtered['Nama Pelanggaran'].str.contains(search, case=False, na=False)]
            
            st.dataframe(df_filtered, use_container_width=True, hide_index=True)
            st.caption(f"Total: {len(df_db_pelanggaran)} jenis pelanggaran")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Tambah Pelanggaran")
        
        with st.form("form_pelanggaran"):
            nama_pelang = st.text_input("Nama Pelanggaran")
            poin_pelang = st.number_input("Poin (positif)", min_value=1, value=10)
            kategori_pelang = st.selectbox("Kategori", [
                "Ringan", "Sedang", "Berat", "Sangat Berat"
            ])
            
            st.info("Poin akan disimpan sebagai nilai positif, tapi dikurangi saat input ke siswa")
            
            submit = st.form_submit_button("Simpan", use_container_width=True)
            
            if submit and nama_pelang.strip():
                try:
                    client = get_gspread_client()
                    spreadsheet = client.open_by_key("1U-RPsmFwSwtdRkMdUlxsndpq15JtZHDulnkf-0v5gCc")
                    ws_pelang_write = spreadsheet.worksheet("pelanggaran")
                    
                    ws_pelang_write.append_row([nama_pelang, int(poin_pelang), kategori_pelang])
                    st.success(f"Pelanggaran '{nama_pelang}' berhasil ditambahkan!")
                    st.cache_data.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"Gagal: {e}")
            elif submit:
                st.warning("Isi nama pelanggaran!")
        
        st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------
# ⭐ HALAMAN DATABASE PRESTASI
# -------------------------------------------------------
elif page == "Database Prestasi":
    st.markdown("""
    <div class='main-header'>
        <h1>Database Prestasi</h1>
        <p>Kelola daftar prestasi dan poinnya</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Daftar Prestasi")
        
        if df_db_prestasi.empty:
            st.info("Database prestasi kosong")
        else:
            search = st.text_input("Cari prestasi", "", key="search_pres")
            df_filtered = df_db_prestasi.copy()
            
            if search:
                df_filtered = df_filtered[df_filtered['Nama Prestasi'].str.contains(search, case=False, na=False)]
            
            st.dataframe(df_filtered, use_container_width=True, hide_index=True)
            st.caption(f"Total: {len(df_db_prestasi)} jenis prestasi")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.subheader("Tambah Prestasi")
        
        with st.form("form_prestasi"):
            nama_pres = st.text_input("Nama Prestasi")
            poin_pres = st.number_input("Poin (positif)", min_value=1, value=20)
            kategori_pres = st.selectbox("Kategori", [
                "Akademik", "Non-Akademik", "Olahraga", "Seni", "Kepemimpinan", "Lainnya"
            ])
            
            st.info("Poin akan ditambahkan ke total siswa saat input")
            
            submit = st.form_submit_button("Simpan", use_container_width=True)
            
            if submit and nama_pres.strip():
                try:
                    client = get_gspread_client()
                    spreadsheet = client.open_by_key("1U-RPsmFwSwtdRkMdUlxsndpq15JtZHDulnkf-0v5gCc")
                    ws_pres_write = spreadsheet.worksheet("prestasi")
                    
                    ws_pres_write.append_row([nama_pres, int(poin_pres), kategori_pres])
                    st.success(f"Prestasi '{nama_pres}' berhasil ditambahkan!")
                    st.cache_data.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"Gagal: {e}")
            elif submit:
                st.warning("Isi nama prestasi!")
        
        st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------------------------------
# FOOTER
# -------------------------------------------------------
st.divider()
st.markdown(
    f"<div style='text-align: center; color: var(--text-secondary); padding: 1rem;'>"
    f"Dashboard Siswa v3.2 Enhanced | "
    f"Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    f"</div>",
    unsafe_allow_html=True
)
