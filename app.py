import streamlit as st
from mitosheet.streamlit.v1 import spreadsheet
import pandas as pd
import plotly.express as px

st.set_page_config(
    layout="wide",
    initial_sidebar_state="auto",
    page_title='Analisa Tren UMKM Jawa Barat 2016-2023',
    page_icon=':face_with_monocle:',
)
st.title("Analisa Tren UMKM Jawa Barat 2016-2023")

@st.cache_data(ttl=86400)
def load_data():
    data = pd.read_csv('https://raw.githubusercontent.com/alfianbayu11/tren-umkm-analisis/main/diskuk-od_17372_proyeksi_jml_ush_mikro_kecil_menengah_umkm__kabupatenk_data.csv')
    return data

# Load data
data = load_data()

# Use Mito spreadsheet for initial exploration
new_dfs, code = spreadsheet(data)
st.write(f"Explore the data in detail using Mito:", new_dfs)

# User selection for visualization
if "Kabupaten/Kota" not in data.columns:
    # Ganti nama kolom "kode_kabupaten_kota" menjadi "Kabupaten/Kota"
    data = data.rename(columns={"nama_kabupaten_kota": "Kabupaten/Kota"})

# Cek apakah kolom "Tahun" ada
if "Tahun" not in data.columns:
    # Tambahkan kolom "Tahun"
    data["Tahun"] = data["tahun"]

# Get selected cities/districts
kabupaten_selected = st.multiselect("Pilih Kabupaten/Kota:", data["Kabupaten/Kota"].unique())

# Get selected years
tahun_awal = st.slider("Tahun Awal:", min_value=2016, max_value=2023, value=2016, key="tahun_awal")
tahun_akhir = st.slider("Tahun Akhir:", min_value=tahun_awal, max_value=2023, value=2023, key="tahun_akhir")

# Filter data based on user selection
filtered_data = data[
    (data["Kabupaten/Kota"].isin(kabupaten_selected)) &
    (data["Tahun"] >= tahun_awal) &
    (data["Tahun"] <= tahun_akhir)
]

# Create visualization using Plotly
fig = px.line(
    filtered_data, x="Tahun", y="proyeksi_jumlah_umkm", color="Kabupaten/Kota"
)
st.plotly_chart(fig)

# fig2 =px.bar(
#     filtered_data, x="Tahun", y="proyeksi_jumlah_umkm", color="Kabupaten/Kota"
# )
# st.plotly_chart(fig2)

# Add explanation
for kabupaten in kabupaten_selected:
    jumlah_proyeksi_seluruh = filtered_data[filtered_data["Kabupaten/Kota"] == kabupaten]["proyeksi_jumlah_umkm"].sum()
    jumlah_proyeksi = filtered_data[filtered_data["Kabupaten/Kota"] == kabupaten]["proyeksi_jumlah_umkm"].max()
    tahun_proyeksi_tertinggi = filtered_data[filtered_data["Kabupaten/Kota"] == kabupaten]["Tahun"].max()
    jumlah_proyeksi_terendah = filtered_data[filtered_data["Kabupaten/Kota"] == kabupaten]["proyeksi_jumlah_umkm"].min()
    tahun_proyeksi_terendah = filtered_data[filtered_data["Kabupaten/Kota"] == kabupaten]["Tahun"].min()
    st.write(f"Kabupaten/Kota: {kabupaten}")
    st.write(f"Jumlah proyeksi UMKM dari {kabupaten} pada tahun {tahun_awal}-{tahun_akhir} adalah **{jumlah_proyeksi_seluruh}** unit.")
    st.write(f"Jumlah proyeksi terendah: {jumlah_proyeksi_terendah} unit pada tahun {tahun_proyeksi_terendah}")
    st.write(f"Jumlah proyeksi tertinggi: {jumlah_proyeksi} unit pada tahun {tahun_proyeksi_tertinggi}")