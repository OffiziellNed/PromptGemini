import streamlit as st
import json
import os

# --- PENANGANAN AMAN UNTUK ONLINE & LOKAL ---
# Mencoba import pyperclip. Jika di web online tidak ada, web tidak akan error.
try:
    import pyperclip
    HAS_PYPERCLIP = True
except ImportError:
    HAS_PYPERCLIP = False

# Konfigurasi Halaman
st.set_page_config(page_title="PROMPT GEMINI - RED GAMES", layout="wide")

# --- INISIALISASI FOLDER & DATA ---
if not os.path.exists("images"):
    os.makedirs("images")

DATA_FILE = "data_prompt_full.json"

# Data Default
DEFAULT_DATA = [] # Akan otomatis terisi jika data_prompt_full.json sudah ada

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump(DEFAULT_DATA, f, indent=4)
        return DEFAULT_DATA
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

daftar_prompt = load_data()

# --- INJEKSI CSS ---
st.markdown("""
<style>
.stTabs [data-baseweb="tab-list"] {
    justify-content: flex-end;
}
</style>
""", unsafe_allow_html=True)

# Judul Portal
st.title("PROMPT GEMINI - RED GAMES")
st.divider()

# --- ADMIN PANEL (DI SIDEBAR) ---
st.sidebar.header("⚙️ Admin Panel")
admin_password = st.sidebar.text_input("Masukkan Kode Akses:", type="password")

if admin_password == "Ger1594NxtOy!":
    st.sidebar.success("Akses Diberikan!")
    
    tab_upload, tab_delete = st.sidebar.tabs(["⬆️ Upload Baru", "🗑️ Hapus Data"])
    
    # BAGIAN UPLOAD & COPY DATA BACKUP
    with tab_upload:
        with st.form("form_upload", clear_on_submit=True):
            new_judul = st.text_input("Judul Style Baru")
            new_deskripsi = st.text_area("Deskripsi Prompt")
            uploaded_files = st.file_uploader("Upload Foto (Maks 3)", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)
            
            submit_upload = st.form_submit_button("Simpan Data")
            
            if submit_upload:
                if not new_judul or not new_deskripsi or not uploaded_files:
                    st.error("Semua kolom harus diisi dan gambar harus diupload!")
                elif len(uploaded_files) > 3:
                    st.error("Maksimal hanya 3 foto yang diperbolehkan!")
                else:
                    saved_image_paths = []
                    for file in uploaded_files:
                        file_path = os.path.join("images", file.name)
                        with open(file_path, "wb") as f:
                            f.write(file.getbuffer())
                        saved_image_paths.append(file_path)
                    
                    data_baru = {
                        "gambar": saved_image_paths,
                        "judul_gambar": new_judul,
                        "prompt": new_deskripsi
                    }
                    daftar_prompt.append(data_baru)
                    save_data(daftar_prompt)
                    st.success("Data berhasil ditambahkan ke sistem!")
                    st.rerun()
        
        # FITUR: COPY DATA TERUPDATE (DI BELAKANG LAYAR)
        st.divider()
        st.subheader("📦 Backup Script Terupdate")
        
        python_data_str = f"daftar_prompt = {json.dumps(daftar_prompt, indent=4)}"
        
        if st.button("📋 Copy Data Script Baru", use_container_width=True):
            if HAS_PYPERCLIP:
                pyperclip.copy(python_data_str)
                st.success("✅ Script terupdate berhasil di-copy ke clipboard!")
            else:
                st.error("Gagal copy! Fitur otomatis ini butuh berjalan di laptop lokal.")
                    
    # BAGIAN DELETE
    with tab_delete:
        pilihan_hapus = st.selectbox("Pilih Judul yang ingin dihapus:", [item["judul_gambar"] for item in daftar_prompt])
        if st.button("Hapus Data"):
            daftar_prompt = [item for item in daftar_prompt if item["judul_gambar"] != pilihan_hapus]
            save_data(daftar_prompt)
            st.success(f"{pilihan_hapus} berhasil dihapus!")
            st.rerun()
elif admin_password != "":
    st.sidebar.error("Kode Akses Salah!")

# --- TAMPILAN UTAMA (FLOW BARIS) ---
jumlah_kolom = 4 
cols = st.columns(jumlah_kolom)

for index, item in enumerate(daftar_prompt):
    col = cols[index % jumlah_kolom]
    
    with col:
        # 1. Judul
        st.subheader(f"{index + 1}. {item['judul_gambar']}")
        
        # 2. Gambar (Tabs)
        if len(item["gambar"]) > 1:
            nama_tabs = [f"Slide {i+1}" for i in range(len(item["gambar"]))]
        else:
            nama_tabs = ["View Image"] 
            
        tabs = st.tabs(nama_tabs)
        
        for i, tab in enumerate(tabs):
            with tab:
                try:
                    st.image(item["gambar"][i], use_container_width=True)
                except:
                    st.error("Gambar tidak ditemukan!")
        
        # 3. Board deskripsi yang rapi dan scrollable (Versi Lama)
        with st.container(height=350):
            st.markdown(item["prompt"])
            
        # 4. Tombol Copy
        if st.button("📋 Copy", key=f"copy_btn_main_{index}", use_container_width=True):
            if HAS_PYPERCLIP:
                pyperclip.copy(item["prompt"])
                st.success("✅ Deskripsi sudah tercopy oleh sistem!")
            else:
                st.info("Blok teks secara manual untuk di-copy jika sedang mengakses secara online.")