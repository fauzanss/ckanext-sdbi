-- =====================================================
-- INSERT DATASET BARU UNTUK MALUKU
-- =====================================================
-- Script ini akan menambahkan dataset baru untuk Maluku
-- untuk testing keyword matching system

-- Insert dataset Maluku
INSERT INTO package (
    id,
    name,
    title,
    notes,
    url,
    version,
    author,
    author_email,
    maintainer,
    maintainer_email,
    license_id,
    state,
    type,
    owner_org,
    private,
    metadata_created,
    metadata_modified
) VALUES (
    'maluku-bencana-2024-uuid',
    'data-bencana-maluku-2024',
    'Data Bencana Alam Provinsi Maluku Tahun 2024',
    'Dataset ini berisi data bencana alam yang terjadi di Provinsi Maluku selama tahun 2024. Data mencakup informasi tentang gempa bumi, tsunami, banjir, dan bencana alam lainnya yang terjadi di berbagai kabupaten dan kota di Maluku. Dataset ini dikumpulkan oleh Badan Penanggulangan Bencana Daerah (BPBD) Provinsi Maluku dan diupdate secara berkala.',
    '',
    '1.0',
    'BPBD Maluku',
    'bpbd@maluku.go.id',
    'BPBD Maluku',
    'bpbd@maluku.go.id',
    'cc-by',
    'active',
    'dataset',
    NULL,
    false,
    NOW(),
    NOW()
);

-- Insert dataset Ambon (Kota di Maluku)
INSERT INTO package (
    id,
    name,
    title,
    notes,
    url,
    version,
    author,
    author_email,
    maintainer,
    maintainer_email,
    license_id,
    state,
    type,
    owner_org,
    private,
    metadata_created,
    metadata_modified
) VALUES (
    'ambon-penduduk-2024-uuid',
    'data-penduduk-ambon-2024',
    'Data Kependudukan Kota Ambon Tahun 2024',
    'Dataset ini berisi data kependudukan Kota Ambon, Provinsi Maluku untuk tahun 2024. Data mencakup jumlah penduduk per kecamatan, distribusi usia, jenis kelamin, dan data demografi lainnya. Dataset ini dikumpulkan oleh Badan Pusat Statistik (BPS) Kota Ambon dan Dinas Kependudukan dan Catatan Sipil Kota Ambon.',
    '',
    '1.0',
    'BPS Kota Ambon',
    'bps@ambon.go.id',
    'BPS Kota Ambon',
    'bps@ambon.go.id',
    'cc-by',
    'active',
    'dataset',
    NULL,
    false,
    NOW(),
    NOW()
);

-- Insert dataset Ternate (Kota di Maluku Utara)
INSERT INTO package (
    id,
    name,
    title,
    notes,
    url,
    version,
    author,
    author_email,
    maintainer,
    maintainer_email,
    license_id,
    state,
    type,
    owner_org,
    private,
    metadata_created,
    metadata_modified
) VALUES (
    'ternate-ekonomi-2024-uuid',
    'data-ekonomi-ternate-2024',
    'Data Ekonomi Kota Ternate Tahun 2024',
    'Dataset ini berisi data ekonomi Kota Ternate, Provinsi Maluku Utara untuk tahun 2024. Data mencakup Produk Domestik Regional Bruto (PDRB), inflasi, tingkat pengangguran, dan indikator ekonomi lainnya. Dataset ini dikumpulkan oleh Badan Pusat Statistik (BPS) Kota Ternate dan Dinas Perindustrian dan Perdagangan Kota Ternate.',
    '',
    '1.0',
    'BPS Kota Ternate',
    'bps@ternate.go.id',
    'BPS Kota Ternate',
    'bps@ternate.go.id',
    'cc-by',
    'active',
    'dataset',
    NULL,
    false,
    NOW(),
    NOW()
);

-- Insert tracking data untuk simulasi views
INSERT INTO tracking_raw (url, tracking_type, user_key, access_timestamp) VALUES
('/dataset/data-bencana-maluku-2024', 'page', 'test_user_1', NOW() - INTERVAL '1 day'),
('/dataset/data-bencana-maluku-2024', 'page', 'test_user_2', NOW() - INTERVAL '2 days'),
('/dataset/data-bencana-maluku-2024', 'page', 'test_user_3', NOW() - INTERVAL '3 days'),
('/dataset/data-bencana-maluku-2024', 'page', 'test_user_4', NOW() - INTERVAL '4 days'),
('/dataset/data-bencana-maluku-2024', 'page', 'test_user_5', NOW() - INTERVAL '5 days'),
('/dataset/data-bencana-maluku-2024', 'page', 'test_user_6', NOW() - INTERVAL '6 days'),
('/dataset/data-bencana-maluku-2024', 'page', 'test_user_7', NOW() - INTERVAL '7 days'),
('/dataset/data-bencana-maluku-2024', 'page', 'test_user_8', NOW() - INTERVAL '8 days'),
('/dataset/data-bencana-maluku-2024', 'page', 'test_user_9', NOW() - INTERVAL '9 days'),
('/dataset/data-bencana-maluku-2024', 'page', 'test_user_10', NOW() - INTERVAL '10 days'),
('/dataset/data-penduduk-ambon-2024', 'page', 'test_user_1', NOW() - INTERVAL '1 day'),
('/dataset/data-penduduk-ambon-2024', 'page', 'test_user_2', NOW() - INTERVAL '2 days'),
('/dataset/data-penduduk-ambon-2024', 'page', 'test_user_3', NOW() - INTERVAL '3 days'),
('/dataset/data-penduduk-ambon-2024', 'page', 'test_user_4', NOW() - INTERVAL '4 days'),
('/dataset/data-penduduk-ambon-2024', 'page', 'test_user_5', NOW() - INTERVAL '5 days'),
('/dataset/data-ekonomi-ternate-2024', 'page', 'test_user_1', NOW() - INTERVAL '1 day'),
('/dataset/data-ekonomi-ternate-2024', 'page', 'test_user_2', NOW() - INTERVAL '2 days'),
('/dataset/data-ekonomi-ternate-2024', 'page', 'test_user_3', NOW() - INTERVAL '3 days');

-- Verifikasi dataset yang baru ditambahkan
SELECT 'Dataset Maluku yang baru ditambahkan:' as info;
SELECT name, title, notes 
FROM package 
WHERE name IN ('data-bencana-maluku-2024', 'data-penduduk-ambon-2024', 'data-ekonomi-ternate-2024')
ORDER BY name;

-- Test keyword matching untuk Maluku
SELECT 'Test keyword matching untuk Maluku:' as info;
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
    'Statistik Setelah Insert Maluku:' as info,
    (SELECT COUNT(*) FROM provinsi_matches) as provinsi_count,
    (SELECT COUNT(*) FROM kabupaten_kota_matches) as kabupaten_kota_count,
    (SELECT COUNT(*) FROM kementerian_matches) as kementerian_count;

-- Cek provinsi yang terdeteksi
SELECT 'Provinsi yang terdeteksi:' as info;
SELECT DISTINCT pk.provinsi_name
FROM package p
JOIN provinsi_keywords pk ON LOWER(CONCAT(p.title, ' ', COALESCE(p.notes, ''))) LIKE '%' || pk.keyword || '%'
WHERE p.state = 'active' AND p.private = false
ORDER BY pk.provinsi_name;

-- Cek kabupaten/kota yang terdeteksi
SELECT 'Kabupaten/Kota yang terdeteksi:' as info;
SELECT DISTINCT kkk.kabupaten_kota_name
FROM package p
JOIN kabupaten_kota_keywords kkk ON LOWER(CONCAT(p.title, ' ', COALESCE(p.notes, ''))) LIKE '%' || kkk.keyword || '%'
WHERE p.state = 'active' AND p.private = false
ORDER BY kkk.kabupaten_kota_name;
