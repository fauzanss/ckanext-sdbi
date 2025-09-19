-- =====================================================
-- SCRIPT UNTUK INSERT KEYWORDS BARU
-- =====================================================
-- Script ini memungkinkan menambah provinsi, kabupaten/kota, dan kementerian baru
-- tanpa perlu mengubah code Python

-- =====================================================
-- 1. INSERT PROVINSI BARU
-- =====================================================

-- Contoh: Tambah Provinsi Papua Tengah
INSERT INTO provinsi_keywords (provinsi_name, keyword, is_alias) VALUES
('papua tengah', 'papua tengah', FALSE),
('papua tengah', 'papteng', TRUE),
('papua tengah', 'provinsi papua tengah', TRUE);

-- Contoh: Tambah Provinsi Papua Pegunungan
INSERT INTO provinsi_keywords (provinsi_name, keyword, is_alias) VALUES
('papua pegunungan', 'papua pegunungan', FALSE),
('papua pegunungan', 'papgun', TRUE),
('papua pegunungan', 'provinsi papua pegunungan', TRUE);

-- Contoh: Tambah Provinsi Papua Selatan
INSERT INTO provinsi_keywords (provinsi_name, keyword, is_alias) VALUES
('papua selatan', 'papua selatan', FALSE),
('papua selatan', 'papsel', TRUE),
('papua selatan', 'provinsi papua selatan', TRUE);

-- Contoh: Tambah Provinsi Papua Barat Daya
INSERT INTO provinsi_keywords (provinsi_name, keyword, is_alias) VALUES
('papua barat daya', 'papua barat daya', FALSE),
('papua barat daya', 'pabar daya', TRUE),
('papua barat daya', 'provinsi papua barat daya', TRUE);

-- =====================================================
-- 2. INSERT KABUPATEN/KOTA BARU
-- =====================================================

-- Contoh: Tambah Kota Cirebon
INSERT INTO kabupaten_kota_keywords (kabupaten_kota_name, keyword, is_alias) VALUES
('cirebon', 'cirebon', FALSE),
('cirebon', 'kota cirebon', TRUE),
('cirebon', 'kabupaten cirebon', TRUE);

-- Contoh: Tambah Kota Tasikmalaya
INSERT INTO kabupaten_kota_keywords (kabupaten_kota_name, keyword, is_alias) VALUES
('tasikmalaya', 'tasikmalaya', FALSE),
('tasikmalaya', 'kota tasikmalaya', TRUE),
('tasikmalaya', 'kabupaten tasikmalaya', TRUE);

-- Contoh: Tambah Kota Cimahi
INSERT INTO kabupaten_kota_keywords (kabupaten_kota_name, keyword, is_alias) VALUES
('cimahi', 'cimahi', FALSE),
('cimahi', 'kota cimahi', TRUE);

-- Contoh: Tambah Kota Banjar
INSERT INTO kabupaten_kota_keywords (kabupaten_kota_name, keyword, is_alias) VALUES
('banjar', 'banjar', FALSE),
('banjar', 'kota banjar', TRUE);

-- Contoh: Tambah Kota Sukabumi
INSERT INTO kabupaten_kota_keywords (kabupaten_kota_name, keyword, is_alias) VALUES
('sukabumi', 'sukabumi', FALSE),
('sukabumi', 'kota sukabumi', TRUE),
('sukabumi', 'kabupaten sukabumi', TRUE);

-- =====================================================
-- 3. INSERT KEMENTERIAN/LEMBAGA BARU
-- =====================================================

-- Contoh: Tambah Kementerian Investasi
INSERT INTO kementerian_keywords (kementerian_name, keyword, is_alias) VALUES
('kemeninvest', 'kemeninvest', FALSE),
('kemeninvest', 'kementerian investasi', TRUE),
('kemeninvest', 'kementerian investasi dan bumn', TRUE);

-- Contoh: Tambah Kementerian ATR/BPN
INSERT INTO kementerian_keywords (kementerian_name, keyword, is_alias) VALUES
('kemenatr', 'kemenatr', FALSE),
('kemenatr', 'kementerian agraria', TRUE),
('kemenatr', 'kementerian agraria dan tata ruang', TRUE),
('kemenatr', 'atr bpn', TRUE);

-- Contoh: Tambah Kementerian PUPR
INSERT INTO kementerian_keywords (kementerian_name, keyword, is_alias) VALUES
('kemenpupr', 'kemenpupr', FALSE),
('kemenpupr', 'kementerian pekerjaan umum', TRUE),
('kemenpupr', 'kementerian pekerjaan umum dan perumahan rakyat', TRUE);

-- Contoh: Tambah Kementerian ESDM
INSERT INTO kementerian_keywords (kementerian_name, keyword, is_alias) VALUES
('kemenesdm', 'kemenesdm', FALSE),
('kemenesdm', 'kementerian energi', TRUE),
('kemenesdm', 'kementerian energi dan sumber daya mineral', TRUE);

-- =====================================================
-- 4. INSERT MULTIPLE KEYWORDS SEKALIGUS
-- =====================================================

-- Contoh: Tambah beberapa provinsi sekaligus
INSERT INTO provinsi_keywords (provinsi_name, keyword, is_alias) VALUES
('kalimantan utara', 'kalimantan utara', FALSE),
('kalimantan utara', 'kaltara', TRUE),
('kalimantan utara', 'provinsi kalimantan utara', TRUE),
('kepulauan riau', 'kepulauan riau', FALSE),
('kepulauan riau', 'kepri', TRUE),
('kepulauan riau', 'provinsi kepulauan riau', TRUE),
('kepulauan bangka belitung', 'kepulauan bangka belitung', FALSE),
('kepulauan bangka belitung', 'babel', TRUE),
('kepulauan bangka belitung', 'provinsi kepulauan bangka belitung', TRUE);

-- Contoh: Tambah beberapa kota sekaligus
INSERT INTO kabupaten_kota_keywords (kabupaten_kota_name, keyword, is_alias) VALUES
('purwokerto', 'purwokerto', FALSE),
('purwokerto', 'kota purwokerto', TRUE),
('purwokerto', 'kabupaten banyumas', TRUE),
('magelang', 'magelang', FALSE),
('magelang', 'kota magelang', TRUE),
('magelang', 'kabupaten magelang', TRUE),
('salatiga', 'salatiga', FALSE),
('salatiga', 'kota salatiga', TRUE);

-- =====================================================
-- 5. VERIFIKASI HASIL INSERT
-- =====================================================

-- Cek provinsi yang baru ditambahkan
SELECT 'Provinsi baru yang ditambahkan:' as info;
SELECT provinsi_name, keyword, is_alias 
FROM provinsi_keywords 
WHERE provinsi_name IN ('papua tengah', 'papua pegunungan', 'papua selatan', 'papua barat daya', 'kalimantan utara', 'kepulauan riau', 'kepulauan bangka belitung')
ORDER BY provinsi_name, is_alias;

-- Cek kabupaten/kota yang baru ditambahkan
SELECT 'Kabupaten/Kota baru yang ditambahkan:' as info;
SELECT kabupaten_kota_name, keyword, is_alias 
FROM kabupaten_kota_keywords 
WHERE kabupaten_kota_name IN ('cirebon', 'tasikmalaya', 'cimahi', 'banjar', 'sukabumi', 'purwokerto', 'magelang', 'salatiga')
ORDER BY kabupaten_kota_name, is_alias;

-- Cek kementerian yang baru ditambahkan
SELECT 'Kementerian baru yang ditambahkan:' as info;
SELECT kementerian_name, keyword, is_alias 
FROM kementerian_keywords 
WHERE kementerian_name IN ('kemeninvest', 'kemenatr', 'kemenpupr', 'kemenesdm')
ORDER BY kementerian_name, is_alias;

-- =====================================================
-- 6. TEST STATISTIK BARU
-- =====================================================

-- Test query untuk melihat statistik terbaru
WITH dataset_text AS (
    SELECT 
        name,
        title,
        notes,
        LOWER(CONCAT(title, ' ', COALESCE(notes, ''))) as full_text
    FROM package 
    WHERE state = 'active' AND private = false
),
provinsi_matches AS (
    SELECT DISTINCT pk.provinsi_name
    FROM dataset_text dt
    JOIN provinsi_keywords pk ON dt.full_text LIKE '%' || pk.keyword || '%'
),
kabupaten_kota_matches AS (
    SELECT DISTINCT kkk.kabupaten_kota_name
    FROM dataset_text dt
    JOIN kabupaten_kota_keywords kkk ON dt.full_text LIKE '%' || kkk.keyword || '%'
),
kementerian_matches AS (
    SELECT DISTINCT kk.kementerian_name
    FROM dataset_text dt
    JOIN kementerian_keywords kk ON dt.full_text LIKE '%' || kk.keyword || '%'
)
SELECT 
    'Statistik Terbaru:' as info,
    (SELECT COUNT(*) FROM provinsi_matches) as provinsi_count,
    (SELECT COUNT(*) FROM kabupaten_kota_matches) as kabupaten_kota_count,
    (SELECT COUNT(*) FROM kementerian_matches) as kementerian_count;
