import streamlit as st
from koneksi import conn, cursor

st.title("Sistem Rule Based Beasiswa KIP-KULIAH")

st.subheader("Input Data Mahasiswa")

nama = st.text_input("Nama Mahasiswa")

mahasiswa_baru = st.selectbox(
    "Mahasiswa Baru",
    ["YA", "TIDAK"]
)

angkatan = st.number_input(
    "Angkatan",
    min_value=2020,
    max_value=2030,
    step=1
)

lulusan_tahun = st.selectbox(
    "Tahun Lulusan",
    [2023, 2024, 2025]
)

memiliki_prestasi = st.selectbox(
    "Memiliki Prestasi",
    ["YA", "TIDAK"]
)

ekonomi_kurang_mampu = st.selectbox(
    "Ekonomi Kurang Mampu",
    ["YA", "TIDAK"]
)

memiliki_kip = st.selectbox(
    "Memiliki KIP",
    ["YA", "TIDAK"]
)

memiliki_kks = st.selectbox(
    "Memiliki KKS",
    ["YA", "TIDAK"]
)

memiliki_kjp = st.selectbox(
    "Memiliki KJP",
    ["YA", "TIDAK"]
)

organisasi_anti_pancasila = st.selectbox(
    "Terlibat Organisasi Anti Pancasila",
    ["YA", "TIDAK"]
)

st.subheader("Kelengkapan Dokumen")

upload_kk = st.selectbox(
    "Upload KK",
    ["YA", "TIDAK"]
)

upload_ktp = st.selectbox(
    "Upload KTP",
    ["YA", "TIDAK"]
)

upload_ijazah = st.selectbox(
    "Upload Ijazah",
    ["YA", "TIDAK"]
)

upload_surat_penghasilan = st.selectbox(
    "Upload Surat Penghasilan",
    ["YA", "TIDAK"]
)

upload_surat_kurang_mampu = st.selectbox(
    "Upload Surat Kurang Mampu",
    ["YA", "TIDAK"]
)

# BUTTON
if st.button("Proses Seleksi"):

    fakta = {}
    reasoning = []

    if mahasiswa_baru == "YA" and angkatan == 2025:
        fakta["status_mahasiswa"] = "VALID"
        reasoning.append("RULE 1 aktif → status_mahasiswa = VALID")

    if lulusan_tahun in [2023, 2024, 2025]:
        fakta["status_lulusan"] = "VALID"
        reasoning.append("RULE 2 aktif → status_lulusan = VALID")

    if memiliki_prestasi == "YA" and ekonomi_kurang_mampu == "YA":
        fakta["status_ekonomi_prestasi"] = "VALID"
        reasoning.append("RULE 3 aktif → status_ekonomi_prestasi = VALID")

    if (
        memiliki_kip == "YA"
        or memiliki_kks == "YA"
        or memiliki_kjp == "YA"
    ):
        fakta["status_kartu_bantuan"] = "VALID"
        reasoning.append("RULE 4 aktif → status_kartu_bantuan = VALID")

    if organisasi_anti_pancasila == "TIDAK":
        fakta["status_integritas"] = "VALID"
        reasoning.append("RULE 5 aktif → status_integritas = VALID")

    if (
        fakta.get("status_mahasiswa") == "VALID"
        and fakta.get("status_lulusan") == "VALID"
    ):
        fakta["lolos_tahap_1"] = "YA"
        reasoning.append("RULE 6 aktif → lolos_tahap_1 = YA")

    if (
        fakta.get("status_ekonomi_prestasi") == "VALID"
        and fakta.get("status_kartu_bantuan") == "VALID"
    ):
        fakta["lolos_tahap_2"] = "YA"
        reasoning.append("RULE 7 aktif → lolos_tahap_2 = YA")

    if (
        upload_kk == "YA"
        and upload_ktp == "YA"
        and upload_ijazah == "YA"
    ):
        fakta["dokumen_utama"] = "LENGKAP"
        reasoning.append("RULE 8 aktif → dokumen_utama = LENGKAP")

    if (
        upload_surat_penghasilan == "YA"
        and upload_surat_kurang_mampu == "YA"
    ):
        fakta["dokumen_ekonomi"] = "LENGKAP"
        reasoning.append("RULE 9 aktif → dokumen_ekonomi = LENGKAP")

    if (
        fakta.get("lolos_tahap_1") == "YA"
        and fakta.get("lolos_tahap_2") == "YA"
        and fakta.get("status_integritas") == "VALID"
        and fakta.get("dokumen_utama") == "LENGKAP"
        and fakta.get("dokumen_ekonomi") == "LENGKAP"
    ):

        keputusan = "LOLOS"
        reasoning.append("RULE 10 aktif → keputusan = LOLOS")

    else:
        keputusan = "TIDAK LOLOS"

    st.subheader("Hasil Keputusan")

    if keputusan == "LOLOS":
        st.success("Mahasiswa DINYATAKAN LOLOS Beasiswa KIP-KULIAH")
    else:
        st.error("Mahasiswa DINYATAKAN TIDAK LOLOS")

    # REASONING
    st.subheader("Reasoning Process")

    for r in reasoning:
        st.write(r)
