-- Examples of how to add new keywords without changing code
-- Just run these SQL commands to add new provinces, cities, or ministries

-- Add new province with aliases
INSERT INTO provinsi_keywords (provinsi_name, keyword, is_alias) VALUES
('papua tengah', 'papua tengah', FALSE),
('papua tengah', 'papteng', TRUE),
('papua tengah', 'provinsi papua tengah', TRUE);

-- Add new city with aliases  
INSERT INTO kabupaten_kota_keywords (kabupaten_kota_name, keyword, is_alias) VALUES
('cirebon', 'cirebon', FALSE),
('cirebon', 'kota cirebon', TRUE),
('cirebon', 'kabupaten cirebon', TRUE);

-- Add new ministry with aliases
INSERT INTO kementerian_keywords (kementerian_name, keyword, is_alias) VALUES
('kemenkumham', 'kementerian hukum dan hak asasi manusia', TRUE),
('kemenkumham', 'kemenkumham', FALSE);

-- You can also add multiple aliases at once
INSERT INTO provinsi_keywords (provinsi_name, keyword, is_alias) VALUES
('kalimantan utara', 'kalimantan utara', FALSE),
('kalimantan utara', 'kaltara', TRUE),
('kalimantan utara', 'provinsi kalimantan utara', TRUE),
('kalimantan utara', 'kaltim utara', TRUE);

-- Check what was added
SELECT 'New provinces added:' as info;
SELECT provinsi_name, keyword, is_alias FROM provinsi_keywords WHERE provinsi_name IN ('papua tengah', 'kalimantan utara');

SELECT 'New cities added:' as info;
SELECT kabupaten_kota_name, keyword, is_alias FROM kabupaten_kota_keywords WHERE kabupaten_kota_name = 'cirebon';

SELECT 'New ministries added:' as info;
SELECT kementerian_name, keyword, is_alias FROM kementerian_keywords WHERE kementerian_name = 'kemenkumham';
