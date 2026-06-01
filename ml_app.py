import streamlit as st
import pandas as pd

from koneksi import conn, cursor

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)


st.title(" Sistem Prediksi Beasiswa KIP-Kuliah")
st.subheader("Machine Learning (k-NN)")


query = "SELECT * FROM dataset_training"
df = pd.read_sql(query, conn)

X = df[
    [
        "mahasiswa_baru",
        "angkatan",
        "lulusan_tahun",
        "memiliki_prestasi",
        "ekonomi_kurang_mampu",
        "memiliki_kip",
        "memiliki_kks",
        "memiliki_kjp",
        "organisasi_anti_pancasila",
        "upload_kk",
        "upload_ktp",
        "upload_ijazah",
        "upload_surat_penghasilan",
        "upload_surat_kurang_mampu"
    ]
]

y = df["keputusan"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


model = KNeighborsClassifier(
    n_neighbors=3
)

model.fit(X_train, y_train)


y_pred = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    y_pred
)

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=["LOLOS", "TIDAK LOLOS"]
)

report = classification_report(
    y_test,
    y_pred,
    output_dict=True
)


st.header("Input Data Mahasiswa")

nama = st.text_input("Nama Mahasiswa")

mahasiswa_baru = st.selectbox(
    "Mahasiswa Baru",
    [1, 0],
    format_func=lambda x: "YA" if x == 1 else "TIDAK"
)

angkatan = st.number_input(
    "Angkatan",
    min_value=2020,
    max_value=2030,
    value=2025
)

lulusan_tahun = st.selectbox(
    "Tahun Lulusan",
    [2023, 2024, 2025]
)

prestasi = st.selectbox(
    "Memiliki Prestasi",
    [1, 0],
    format_func=lambda x: "YA" if x == 1 else "TIDAK"
)

ekonomi = st.selectbox(
    "Ekonomi Kurang Mampu",
    [1, 0],
    format_func=lambda x: "YA" if x == 1 else "TIDAK"
)

kip = st.selectbox(
    "Memiliki KIP",
    [1, 0],
    format_func=lambda x: "YA" if x == 1 else "TIDAK"
)

kks = st.selectbox(
    "Memiliki KKS",
    [1, 0],
    format_func=lambda x: "YA" if x == 1 else "TIDAK"
)

kjp = st.selectbox(
    "Memiliki KJP",
    [1, 0],
    format_func=lambda x: "YA" if x == 1 else "TIDAK"
)

organisasi = st.selectbox(
    "Terlibat Organisasi Anti Pancasila",
    [0, 1],
    format_func=lambda x: "TIDAK" if x == 0 else "YA"
)

st.subheader("Kelengkapan Dokumen")

kk = st.selectbox(
    "Upload KK",
    [1, 0],
    format_func=lambda x: "YA" if x == 1 else "TIDAK"
)

ktp = st.selectbox(
    "Upload KTP",
    [1, 0],
    format_func=lambda x: "YA" if x == 1 else "TIDAK"
)

ijazah = st.selectbox(
    "Upload Ijazah",
    [1, 0],
    format_func=lambda x: "YA" if x == 1 else "TIDAK"
)

surat_penghasilan = st.selectbox(
    "Upload Surat Penghasilan",
    [1, 0],
    format_func=lambda x: "YA" if x == 1 else "TIDAK"
)

surat_kurang_mampu = st.selectbox(
    "Upload Surat Kurang Mampu",
    [1, 0],
    format_func=lambda x: "YA" if x == 1 else "TIDAK"
)

if st.button("Prediksi Kelayakan"):

    data_baru = [[
        mahasiswa_baru,
        angkatan,
        lulusan_tahun,
        prestasi,
        ekonomi,
        kip,
        kks,
        kjp,
        organisasi,
        kk,
        ktp,
        ijazah,
        surat_penghasilan,
        surat_kurang_mampu
    ]]

    hasil = model.predict(data_baru)

    st.subheader("Hasil Prediksi")

    if hasil[0] == "LOLOS":

        st.success(
            f"✅ {nama} Diprediksi LOLOS Beasiswa KIP-Kuliah"
        )

    else:

        st.error(
            f"❌ {nama} Diprediksi TIDAK LOLOS"
        )

    sql = """
    INSERT INTO hasil_prediksi
    (
    mahasiswa_baru,
    angkatan,
    lulusan_tahun,
    memiliki_prestasi,
    ekonomi_kurang_mampu,
    memiliki_kip,
    memiliki_kks,
    memiliki_kjp,
    organisasi_anti_pancasila,
    upload_kk,
    upload_ktp,
    upload_ijazah,
    upload_surat_penghasilan,
    upload_surat_kurang_mampu,
    hasil_prediksi
    )
    VALUES
    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    val = (
        mahasiswa_baru,
        angkatan,
        lulusan_tahun,
        prestasi,
        ekonomi,
        kip,
        kks,
        kjp,
        organisasi,
        kk,
        ktp,
        ijazah,
        surat_penghasilan,
        surat_kurang_mampu,
        hasil[0]
    )

    cursor.execute(sql, val)
    conn.commit()


st.header("Evaluasi Model")

st.metric(
    "Accuracy",
    f"{accuracy * 100:.2f}%"
)

st.subheader("Confusion Matrix")

cm_df = pd.DataFrame(
    cm,
    columns=[
        "Prediksi LOLOS",
        "Prediksi TIDAK LOLOS"
    ],
    index=[
        "Data Asli LOLOS",
        "Data Asli TIDAK LOLOS"
    ]
)

st.table(cm_df)


st.subheader("Classification Report")

report_df = pd.DataFrame(report).transpose()

st.dataframe(report_df)


st.subheader("Dataset Training")

st.write(
    f"Jumlah Dataset Training : {len(df)}"
)

st.dataframe(df)


st.subheader("Riwayat Prediksi")

riwayat = pd.read_sql(
    "SELECT * FROM hasil_prediksi ORDER BY id DESC",
    conn
)

st.dataframe(riwayat)
