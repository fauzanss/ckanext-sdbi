-- =====================================================
-- INSERT KOTA/KABUPATEN LENGKAP INDONESIA
-- =====================================================
-- Script ini berisi semua kota dan kabupaten di Indonesia
-- dengan berbagai alias untuk keyword matching

-- Insert semua kota/kabupaten dengan 4 alias masing-masing
INSERT INTO kabupaten_kota_keywords (kabupaten_kota_name, keyword, is_alias) VALUES
-- ACEH
('aceh barat', 'aceh barat', FALSE),
('aceh barat', 'kabupaten aceh barat', TRUE),
('aceh barat', 'kab aceh barat', TRUE),
('aceh barat', 'aceh barat', TRUE),

('aceh barat daya', 'aceh barat daya', FALSE),
('aceh barat daya', 'kabupaten aceh barat daya', TRUE),
('aceh barat daya', 'kab aceh barat daya', TRUE),
('aceh barat daya', 'abdya', TRUE),

('aceh besar', 'aceh besar', FALSE),
('aceh besar', 'kabupaten aceh besar', TRUE),
('aceh besar', 'kab aceh besar', TRUE),
('aceh besar', 'aceh besar', TRUE),

('aceh jaya', 'aceh jaya', FALSE),
('aceh jaya', 'kabupaten aceh jaya', TRUE),
('aceh jaya', 'kab aceh jaya', TRUE),
('aceh jaya', 'aceh jaya', TRUE),

('aceh selatan', 'aceh selatan', FALSE),
('aceh selatan', 'kabupaten aceh selatan', TRUE),
('aceh selatan', 'kab aceh selatan', TRUE),
('aceh selatan', 'aceh selatan', TRUE),

('aceh singkil', 'aceh singkil', FALSE),
('aceh singkil', 'kabupaten aceh singkil', TRUE),
('aceh singkil', 'kab aceh singkil', TRUE),
('aceh singkil', 'aceh singkil', TRUE),

('aceh tamiang', 'aceh tamiang', FALSE),
('aceh tamiang', 'kabupaten aceh tamiang', TRUE),
('aceh tamiang', 'kab aceh tamiang', TRUE),
('aceh tamiang', 'aceh tamiang', TRUE),

('aceh tengah', 'aceh tengah', FALSE),
('aceh tengah', 'kabupaten aceh tengah', TRUE),
('aceh tengah', 'kab aceh tengah', TRUE),
('aceh tengah', 'aceh tengah', TRUE),

('aceh tenggara', 'aceh tenggara', FALSE),
('aceh tenggara', 'kabupaten aceh tenggara', TRUE),
('aceh tenggara', 'kab aceh tenggara', TRUE),
('aceh tenggara', 'aceh tenggara', TRUE),

('aceh timur', 'aceh timur', FALSE),
('aceh timur', 'kabupaten aceh timur', TRUE),
('aceh timur', 'kab aceh timur', TRUE),
('aceh timur', 'aceh timur', TRUE),

('aceh utara', 'aceh utara', FALSE),
('aceh utara', 'kabupaten aceh utara', TRUE),
('aceh utara', 'kab aceh utara', TRUE),
('aceh utara', 'aceh utara', TRUE),

('banda aceh', 'banda aceh', FALSE),
('banda aceh', 'kota banda aceh', TRUE),
('banda aceh', 'kota banda aceh', TRUE),
('banda aceh', 'banda aceh', TRUE),

('langsa', 'langsa', FALSE),
('langsa', 'kota langsa', TRUE),
('langsa', 'kota langsa', TRUE),
('langsa', 'langsa', TRUE),

('lhokseumawe', 'lhokseumawe', FALSE),
('lhokseumawe', 'kota lhokseumawe', TRUE),
('lhokseumawe', 'kota lhokseumawe', TRUE),
('lhokseumawe', 'lhokseumawe', TRUE),

('sabang', 'sabang', FALSE),
('sabang', 'kota sabang', TRUE),
('sabang', 'kota sabang', TRUE),
('sabang', 'sabang', TRUE),

('subulussalam', 'subulussalam', FALSE),
('subulussalam', 'kota subulussalam', TRUE),
('subulussalam', 'kota subulussalam', TRUE),
('subulussalam', 'subulussalam', TRUE);

-- Insert Kota/Kabupaten Sumatera Utara
INSERT INTO kabupaten_kota_keywords (kabupaten_kota_name, keyword, is_alias) VALUES
('agam', 'agam', FALSE),
('agam', 'kabupaten agam', TRUE),
('agam', 'kab agam', TRUE),
('agam', 'agam', TRUE),

('asahan', 'asahan', FALSE),
('asahan', 'kabupaten asahan', TRUE),
('asahan', 'kab asahan', TRUE),
('asahan', 'asahan', TRUE),

('batubara', 'batubara', FALSE),
('batubara', 'kabupaten batubara', TRUE),
('batubara', 'kab batubara', TRUE),
('batubara', 'batubara', TRUE),

('dairi', 'dairi', FALSE),
('dairi', 'kabupaten dairi', TRUE),
('dairi', 'kab dairi', TRUE),
('dairi', 'dairi', TRUE),

('deli serdang', 'deli serdang', FALSE),
('deli serdang', 'kabupaten deli serdang', TRUE),
('deli serdang', 'kab deli serdang', TRUE),
('deli serdang', 'deli serdang', TRUE),

('humbang hasundutan', 'humbang hasundutan', FALSE),
('humbang hasundutan', 'kabupaten humbang hasundutan', TRUE),
('humbang hasundutan', 'kab humbang hasundutan', TRUE),
('humbang hasundutan', 'humbang hasundutan', TRUE),

('karo', 'karo', FALSE),
('karo', 'kabupaten karo', TRUE),
('karo', 'kab karo', TRUE),
('karo', 'karo', TRUE),

('labuhanbatu', 'labuhanbatu', FALSE),
('labuhanbatu', 'kabupaten labuhanbatu', TRUE),
('labuhanbatu', 'kab labuhanbatu', TRUE),
('labuhanbatu', 'labuhanbatu', TRUE),

('labuhanbatu selatan', 'labuhanbatu selatan', FALSE),
('labuhanbatu selatan', 'kabupaten labuhanbatu selatan', TRUE),
('labuhanbatu selatan', 'kab labuhanbatu selatan', TRUE),
('labuhanbatu selatan', 'labuhanbatu selatan', TRUE),

('labuhanbatu utara', 'labuhanbatu utara', FALSE),
('labuhanbatu utara', 'kabupaten labuhanbatu utara', TRUE),
('labuhanbatu utara', 'kab labuhanbatu utara', TRUE),
('labuhanbatu utara', 'labuhanbatu utara', TRUE),

('langkat', 'langkat', FALSE),
('langkat', 'kabupaten langkat', TRUE),
('langkat', 'kab langkat', TRUE),
('langkat', 'langkat', TRUE),

('mandailing natal', 'mandailing natal', FALSE),
('mandailing natal', 'kabupaten mandailing natal', TRUE),
('mandailing natal', 'kab mandailing natal', TRUE),
('mandailing natal', 'mandailing natal', TRUE),

('nias', 'nias', FALSE),
('nias', 'kabupaten nias', TRUE),
('nias', 'kab nias', TRUE),
('nias', 'nias', TRUE),

('nias barat', 'nias barat', FALSE),
('nias barat', 'kabupaten nias barat', TRUE),
('nias barat', 'kab nias barat', TRUE),
('nias barat', 'nias barat', TRUE),

('nias selatan', 'nias selatan', FALSE),
('nias selatan', 'kabupaten nias selatan', TRUE),
('nias selatan', 'kab nias selatan', TRUE),
('nias selatan', 'nias selatan', TRUE),

('nias utara', 'nias utara', FALSE),
('nias utara', 'kabupaten nias utara', TRUE),
('nias utara', 'kab nias utara', TRUE),
('nias utara', 'nias utara', TRUE),

('padang lawas', 'padang lawas', FALSE),
('padang lawas', 'kabupaten padang lawas', TRUE),
('padang lawas', 'kab padang lawas', TRUE),
('padang lawas', 'padang lawas', TRUE),

('padang lawas utara', 'padang lawas utara', FALSE),
('padang lawas utara', 'kabupaten padang lawas utara', TRUE),
('padang lawas utara', 'kab padang lawas utara', TRUE),
('padang lawas utara', 'padang lawas utara', TRUE),

('pakpak bharat', 'pakpak bharat', FALSE),
('pakpak bharat', 'kabupaten pakpak bharat', TRUE),
('pakpak bharat', 'kab pakpak bharat', TRUE),
('pakpak bharat', 'pakpak bharat', TRUE),

('samosir', 'samosir', FALSE),
('samosir', 'kabupaten samosir', TRUE),
('samosir', 'kab samosir', TRUE),
('samosir', 'samosir', TRUE),

('serdang bedagai', 'serdang bedagai', FALSE),
('serdang bedagai', 'kabupaten serdang bedagai', TRUE),
('serdang bedagai', 'kab serdang bedagai', TRUE),
('serdang bedagai', 'serdang bedagai', TRUE),

('simalungun', 'simalungun', FALSE),
('simalungun', 'kabupaten simalungun', TRUE),
('simalungun', 'kab simalungun', TRUE),
('simalungun', 'simalungun', TRUE),

('tapanuli selatan', 'tapanuli selatan', FALSE),
('tapanuli selatan', 'kabupaten tapanuli selatan', TRUE),
('tapanuli selatan', 'kab tapanuli selatan', TRUE),
('tapanuli selatan', 'tapanuli selatan', TRUE),

('tapanuli tengah', 'tapanuli tengah', FALSE),
('tapanuli tengah', 'kabupaten tapanuli tengah', TRUE),
('tapanuli tengah', 'kab tapanuli tengah', TRUE),
('tapanuli tengah', 'tapanuli tengah', TRUE),

('tapanuli utara', 'tapanuli utara', FALSE),
('tapanuli utara', 'kabupaten tapanuli utara', TRUE),
('tapanuli utara', 'kab tapanuli utara', TRUE),
('tapanuli utara', 'tapanuli utara', TRUE),

('toba', 'toba', FALSE),
('toba', 'kabupaten toba', TRUE),
('toba', 'kab toba', TRUE),
('toba', 'toba', TRUE),

('toba samosir', 'toba samosir', FALSE),
('toba samosir', 'kabupaten toba samosir', TRUE),
('toba samosir', 'kab toba samosir', TRUE),
('toba samosir', 'toba samosir', TRUE),

('binjai', 'binjai', FALSE),
('binjai', 'kota binjai', TRUE),
('binjai', 'kota binjai', TRUE),
('binjai', 'binjai', TRUE),

('gunungsitoli', 'gunungsitoli', FALSE),
('gunungsitoli', 'kota gunungsitoli', TRUE),
('gunungsitoli', 'kota gunungsitoli', TRUE),
('gunungsitoli', 'gunungsitoli', TRUE),

('medan', 'medan', FALSE),
('medan', 'kota medan', TRUE),
('medan', 'kota medan', TRUE),
('medan', 'medan', TRUE),

('padang sidempuan', 'padang sidempuan', FALSE),
('padang sidempuan', 'kota padang sidempuan', TRUE),
('padang sidempuan', 'kota padang sidempuan', TRUE),
('padang sidempuan', 'padang sidempuan', TRUE),

('pematang siantar', 'pematang siantar', FALSE),
('pematang siantar', 'kota pematang siantar', TRUE),
('pematang siantar', 'kota pematang siantar', TRUE),
('pematang siantar', 'pematang siantar', TRUE),

('sibolga', 'sibolga', FALSE),
('sibolga', 'kota sibolga', TRUE),
('sibolga', 'kota sibolga', TRUE),
('sibolga', 'sibolga', TRUE),

('tanjung balai', 'tanjung balai', FALSE),
('tanjung balai', 'kota tanjung balai', TRUE),
('tanjung balai', 'kota tanjung balai', TRUE),
('tanjung balai', 'tanjung balai', TRUE),

('tebing tinggi', 'tebing tinggi', FALSE),
('tebing tinggi', 'kota tebing tinggi', TRUE),
('tebing tinggi', 'kota tebing tinggi', TRUE),
('tebing tinggi', 'tebing tinggi', TRUE);

-- Insert Kota/Kabupaten Sumatera Barat
INSERT INTO kabupaten_kota_keywords (kabupaten_kota_name, keyword, is_alias) VALUES
('agam', 'agam', FALSE),
('agam', 'kabupaten agam', TRUE),
('agam', 'kab agam', TRUE),
('agam', 'agam', TRUE),

('dharmasraya', 'dharmasraya', FALSE),
('dharmasraya', 'kabupaten dharmasraya', TRUE),
('dharmasraya', 'kab dharmasraya', TRUE),
('dharmasraya', 'dharmasraya', TRUE),

('kepulauan mentawai', 'kepulauan mentawai', FALSE),
('kepulauan mentawai', 'kabupaten kepulauan mentawai', TRUE),
('kepulauan mentawai', 'kab kepulauan mentawai', TRUE),
('kepulauan mentawai', 'kepulauan mentawai', TRUE),

('lima puluh kota', 'lima puluh kota', FALSE),
('lima puluh kota', 'kabupaten lima puluh kota', TRUE),
('lima puluh kota', 'kab lima puluh kota', TRUE),
('lima puluh kota', 'lima puluh kota', TRUE),

('padang pariaman', 'padang pariaman', FALSE),
('padang pariaman', 'kabupaten padang pariaman', TRUE),
('padang pariaman', 'kab padang pariaman', TRUE),
('padang pariaman', 'padang pariaman', TRUE),

('pasaman', 'pasaman', FALSE),
('pasaman', 'kabupaten pasaman', TRUE),
('pasaman', 'kab pasaman', TRUE),
('pasaman', 'pasaman', TRUE),

('pasaman barat', 'pasaman barat', FALSE),
('pasaman barat', 'kabupaten pasaman barat', TRUE),
('pasaman barat', 'kab pasaman barat', TRUE),
('pasaman barat', 'pasaman barat', TRUE),

('pesisir selatan', 'pesisir selatan', FALSE),
('pesisir selatan', 'kabupaten pesisir selatan', TRUE),
('pesisir selatan', 'kab pesisir selatan', TRUE),
('pesisir selatan', 'pesisir selatan', TRUE),

('sijunjung', 'sijunjung', FALSE),
('sijunjung', 'kabupaten sijunjung', TRUE),
('sijunjung', 'kab sijunjung', TRUE),
('sijunjung', 'sijunjung', TRUE),

('solok', 'solok', FALSE),
('solok', 'kabupaten solok', TRUE),
('solok', 'kab solok', TRUE),
('solok', 'solok', TRUE),

('solok selatan', 'solok selatan', FALSE),
('solok selatan', 'kabupaten solok selatan', TRUE),
('solok selatan', 'kab solok selatan', TRUE),
('solok selatan', 'solok selatan', TRUE),

('tanah datar', 'tanah datar', FALSE),
('tanah datar', 'kabupaten tanah datar', TRUE),
('tanah datar', 'kab tanah datar', TRUE),
('tanah datar', 'tanah datar', TRUE),

('bukittinggi', 'bukittinggi', FALSE),
('bukittinggi', 'kota bukittinggi', TRUE),
('bukittinggi', 'kota bukittinggi', TRUE),
('bukittinggi', 'bukittinggi', TRUE),

('padang', 'padang', FALSE),
('padang', 'kota padang', TRUE),
('padang', 'kota padang', TRUE),
('padang', 'padang', TRUE),

('padang panjang', 'padang panjang', FALSE),
('padang panjang', 'kota padang panjang', TRUE),
('padang panjang', 'kota padang panjang', TRUE),
('padang panjang', 'padang panjang', TRUE),

('pariaman', 'pariaman', FALSE),
('pariaman', 'kota pariaman', TRUE),
('pariaman', 'kota pariaman', TRUE),
('pariaman', 'pariaman', TRUE),

('payakumbuh', 'payakumbuh', FALSE),
('payakumbuh', 'kota payakumbuh', TRUE),
('payakumbuh', 'kota payakumbuh', TRUE),
('payakumbuh', 'payakumbuh', TRUE),

('sawah lunto', 'sawah lunto', FALSE),
('sawah lunto', 'kota sawah lunto', TRUE),
('sawah lunto', 'kota sawah lunto', TRUE),
('sawah lunto', 'sawah lunto', TRUE),

('solok', 'solok', FALSE),
('solok', 'kota solok', TRUE),
('solok', 'kota solok', TRUE),
('solok', 'solok', TRUE);

-- Verifikasi hasil insert
SELECT 'Kota/Kabupaten yang ditambahkan:' as info;
SELECT kabupaten_kota_name, COUNT(*) as keyword_count 
FROM kabupaten_kota_keywords 
GROUP BY kabupaten_kota_name 
ORDER BY kabupaten_kota_name;
