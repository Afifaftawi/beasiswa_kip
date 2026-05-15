CREATE DATABASE beasiswa_kip;

USE beasiswa_kip;


CREATE TABLE rules (
    id_rule INT AUTO_INCREMENT PRIMARY KEY,
    nama_rule VARCHAR(50),
    kondisi TEXT,
    hasil VARCHAR(100)
);


CREATE TABLE conditions (
    id_condition INT AUTO_INCREMENT PRIMARY KEY,
    nama_condition VARCHAR(100),
    nilai VARCHAR(100)
);


CREATE TABLE pendaftaran (
    id_pendaftar INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100),

    mahasiswa_baru ENUM('YA','TIDAK'),
    angkatan INT,
    lulusan_tahun INT,

    memiliki_prestasi ENUM('YA','TIDAK'),
    ekonomi_kurang_mampu ENUM('YA','TIDAK'),

    memiliki_kip ENUM('YA','TIDAK'),
    memiliki_kks ENUM('YA','TIDAK'),
    memiliki_kjp ENUM('YA','TIDAK'),

    organisasi_anti_pancasila ENUM('YA','TIDAK'),

    upload_kk ENUM('YA','TIDAK'),
    upload_ktp ENUM('YA','TIDAK'),
    upload_ijazah ENUM('YA','TIDAK'),

    upload_surat_penghasilan ENUM('YA','TIDAK'),
    upload_surat_kurang_mampu ENUM('YA','TIDAK')
);


INSERT INTO rules (nama_rule, kondisi, hasil) VALUES
('RULE 1',
'mahasiswa_baru=YA AND angkatan=2025',
'status_mahasiswa=VALID'),

('RULE 2',
'lulusan_tahun=2023 OR lulusan_tahun=2024 OR lulusan_tahun=2025',
'status_lulusan=VALID'),

('RULE 3',
'memiliki_prestasi=YA AND ekonomi_kurang_mampu=YA',
'status_ekonomi_prestasi=VALID'),

('RULE 4',
'memiliki_kip=YA OR memiliki_kks=YA OR memiliki_kjp=YA',
'status_kartu_bantuan=VALID'),

('RULE 5',
'organisasi_anti_pancasila=TIDAK',
'status_integritas=VALID'),

('RULE 6',
'status_mahasiswa=VALID AND status_lulusan=VALID',
'lolos_tahap_1=YA'),

('RULE 7',
'status_ekonomi_prestasi=VALID AND status_kartu_bantuan=VALID',
'lolos_tahap_2=YA'),

('RULE 8',
'upload_kk=YA AND upload_ktp=YA AND upload_ijazah=YA',
'dokumen_utama=LENGKAP'),

('RULE 9',
'upload_surat_penghasilan=YA AND upload_surat_kurang_mampu=YA',
'dokumen_ekonomi=LENGKAP'),

('RULE 10',
'lolos_tahap_1=YA AND lolos_tahap_2=YA AND status_integritas=VALID AND dokumen_utama=LENGKAP AND dokumen_ekonomi=LENGKAP',
'keputusan=LOLOS');


INSERT INTO conditions (nama_condition, nilai) VALUES
('mahasiswa_baru', 'YA'),
('angkatan', '2025'),
('lulusan_tahun', '2025'),
('memiliki_prestasi', 'YA'),
('ekonomi_kurang_mampu', 'YA'),
('memiliki_kip', 'YA'),
('organisasi_anti_pancasila', 'TIDAK');


INSERT INTO pendaftaran (
    nama,
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
    upload_surat_kurang_mampu
) VALUES (
    'AFIF AFTAWI',
    'YA',
    2025,
    2025,
    'YA',
    'YA',
    'YA',
    'TIDAK',
    'TIDAK',
    'TIDAK',
    'YA',
    'YA',
    'YA',
    'YA',
    'YA'
);
