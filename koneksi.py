import mysql.connector

conn = mysql.connector.connect(
    host="127.0.0.1",
    port=8889,
    user="root",
    password="root",
    database="beasiswa_kip_rbs"
)

cursor = conn.cursor(dictionary=True)

print("Koneksi berhasil")
