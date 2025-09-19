-- =====================================================
-- INSERT KEMENTERIAN DAN LEMBAGA LENGKAP
-- =====================================================
-- Script ini berisi semua kementerian dan lembaga negara Indonesia
-- dengan berbagai alias untuk keyword matching

-- Insert Kementerian Koordinator
INSERT INTO kementerian_keywords (kementerian_name, keyword, is_alias) VALUES
-- Kementerian Koordinator Bidang Politik dan Keamanan
('kemenko polhukam', 'kemenko polhukam', FALSE),
('kemenko polhukam', 'kementerian koordinator bidang politik dan keamanan', TRUE),
('kemenko polhukam', 'kemenko politik keamanan', TRUE),
('kemenko polhukam', 'koordinator polhukam', TRUE),

-- Kementerian Koordinator Bidang Hukum, HAM, Imigrasi & Pemasyarakatan
('kemenko hukum ham', 'kemenko hukum ham', FALSE),
('kemenko hukum ham', 'kementerian koordinator bidang hukum ham imigrasi pemasyarakatan', TRUE),
('kemenko hukum ham', 'kemenko hukum dan ham', TRUE),
('kemenko hukum ham', 'koordinator hukum ham', TRUE),

-- Kementerian Koordinator Bidang Perekonomian
('kemenko perekonomian', 'kemenko perekonomian', FALSE),
('kemenko perekonomian', 'kementerian koordinator bidang perekonomian', TRUE),
('kemenko perekonomian', 'kemenko ekonomi', TRUE),
('kemenko perekonomian', 'koordinator perekonomian', TRUE),

-- Kementerian Koordinator Bidang Pembangunan Manusia dan Kebudayaan
('kemenko pmk', 'kemenko pmk', FALSE),
('kemenko pmk', 'kementerian koordinator bidang pembangunan manusia dan kebudayaan', TRUE),
('kemenko pmk', 'kemenko pembangunan manusia kebudayaan', TRUE),
('kemenko pmk', 'koordinator pmk', TRUE),

-- Kementerian Koordinator Bidang Infrastruktur dan Pembangunan Kewilayahan
('kemenko infrastruktur', 'kemenko infrastruktur', FALSE),
('kemenko infrastruktur', 'kementerian koordinator bidang infrastruktur dan pembangunan kewilayahan', TRUE),
('kemenko infrastruktur', 'kemenko infrakeswil', TRUE),
('kemenko infrastruktur', 'koordinator infrastruktur', TRUE),

-- Kementerian Koordinator Bidang Pemberdayaan Masyarakat
('kemenko pm', 'kemenko pm', FALSE),
('kemenko pm', 'kementerian koordinator bidang pemberdayaan masyarakat', TRUE),
('kemenko pm', 'kemenko pemberdayaan masyarakat', TRUE),
('kemenko pm', 'koordinator pemberdayaan masyarakat', TRUE),

-- Kementerian Koordinator Bidang Pangan
('kemenko pangan', 'kemenko pangan', FALSE),
('kemenko pangan', 'kementerian koordinator bidang pangan', TRUE),
('kemenko pangan', 'kemenko ketahanan pangan', TRUE),
('kemenko pangan', 'koordinator pangan', TRUE);

-- Insert Kementerian Teknis
INSERT INTO kementerian_keywords (kementerian_name, keyword, is_alias) VALUES
-- Kementerian Dalam Negeri
('kemendagri', 'kemendagri', FALSE),
('kemendagri', 'kementerian dalam negeri', TRUE),
('kemendagri', 'mendagri', TRUE),
('kemendagri', 'dalam negeri', TRUE),

-- Kementerian Luar Negeri
('kemlu', 'kemlu', FALSE),
('kemlu', 'kementerian luar negeri', TRUE),
('kemlu', 'menlu', TRUE),
('kemlu', 'luar negeri', TRUE),

-- Kementerian Pertahanan
('kemenhan', 'kemenhan', FALSE),
('kemenhan', 'kementerian pertahanan', TRUE),
('kemenhan', 'menhan', TRUE),
('kemenhan', 'pertahanan', TRUE),

-- Kementerian Keuangan
('kemenkeu', 'kemenkeu', FALSE),
('kemenkeu', 'kementerian keuangan', TRUE),
('kemenkeu', 'menkeu', TRUE),
('kemenkeu', 'keuangan', TRUE),

-- Kementerian Kesehatan
('kemenkes', 'kemenkes', FALSE),
('kemenkes', 'kementerian kesehatan', TRUE),
('kemenkes', 'menkes', TRUE),
('kemenkes', 'kesehatan', TRUE),

-- Kementerian Perdagangan
('kemendag', 'kemendag', FALSE),
('kemendag', 'kementerian perdagangan', TRUE),
('kemendag', 'mendag', TRUE),
('kemendag', 'perdagangan', TRUE),

-- Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi
('kemendikbudristek', 'kemendikbudristek', FALSE),
('kemendikbudristek', 'kementerian pendidikan kebudayaan riset dan teknologi', TRUE),
('kemendikbudristek', 'kemendikbud', TRUE),
('kemendikbudristek', 'mendikbud', TRUE),

-- Kementerian Agama
('kemenag', 'kemenag', FALSE),
('kemenag', 'kementerian agama', TRUE),
('kemenag', 'menag', TRUE),
('kemenag', 'agama', TRUE),

-- Kementerian Hukum dan HAM
('kemenkumham', 'kemenkumham', FALSE),
('kemenkumham', 'kementerian hukum dan ham', TRUE),
('kemenkumham', 'kementerian hukum dan hak asasi manusia', TRUE),
('kemenkumham', 'menkumham', TRUE),

-- Kementerian Energi dan Sumber Daya Mineral
('esdm', 'esdm', FALSE),
('esdm', 'kementerian energi dan sumber daya mineral', TRUE),
('esdm', 'kementerian esdm', TRUE),
('esdm', 'menesdm', TRUE),

-- Kementerian Perhubungan
('kemenhub', 'kemenhub', FALSE),
('kemenhub', 'kementerian perhubungan', TRUE),
('kemenhub', 'menhub', TRUE),
('kemenhub', 'perhubungan', TRUE),

-- Kementerian Lingkungan Hidup dan Kehutanan
('klhk', 'klhk', FALSE),
('klhk', 'kementerian lingkungan hidup dan kehutanan', TRUE),
('klhk', 'kementerian lhk', TRUE),
('klhk', 'menlhk', TRUE),

-- Kementerian Komunikasi dan Informatika
('kominfo', 'kominfo', FALSE),
('kominfo', 'kementerian komunikasi dan informatika', TRUE),
('kominfo', 'kementerian kominfo', TRUE),
('kominfo', 'menkominfo', TRUE),

-- Kementerian Koperasi dan Usaha Kecil Menengah
('kemenkop ukm', 'kemenkop ukm', FALSE),
('kemenkop ukm', 'kementerian koperasi dan usaha kecil menengah', TRUE),
('kemenkop ukm', 'kementerian koperasi ukm', TRUE),
('kemenkop ukm', 'menkop ukm', TRUE),

-- Kementerian BUMN
('kementerian bumn', 'kementerian bumn', FALSE),
('kementerian bumn', 'kementerian badan usaha milik negara', TRUE),
('kementerian bumn', 'menbumn', TRUE),
('kementerian bumn', 'bumn', TRUE),

-- Kementerian Desa, Pembangunan Daerah Tertinggal, dan Transmigrasi
('kemendesa pdtt', 'kemendesa pdtt', FALSE),
('kemendesa pdtt', 'kementerian desa pembangunan daerah tertinggal dan transmigrasi', TRUE),
('kemendesa pdtt', 'kementerian desa pdtt', TRUE),
('kemendesa pdtt', 'mendes pdtt', TRUE),

-- Kementerian Pemuda dan Olahraga
('kemenpora', 'kemenpora', FALSE),
('kemenpora', 'kementerian pemuda dan olahraga', TRUE),
('kemenpora', 'kementerian pemuda olahraga', TRUE),
('kemenpora', 'menpora', TRUE),

-- Kementerian Pekerjaan Umum dan Perumahan Rakyat
('pupr', 'pupr', FALSE),
('pupr', 'kementerian pekerjaan umum dan perumahan rakyat', TRUE),
('pupr', 'kementerian pupr', TRUE),
('pupr', 'menpupr', TRUE),

-- Kementerian Pertanian
('kementan', 'kementan', FALSE),
('kementan', 'kementerian pertanian', TRUE),
('kementan', 'mentan', TRUE),
('kementan', 'pertanian', TRUE),

-- Kementerian Kelautan dan Perikanan
('kkp', 'kkp', FALSE),
('kkp', 'kementerian kelautan dan perikanan', TRUE),
('kkp', 'kementerian kkp', TRUE),
('kkp', 'menkkp', TRUE),

-- Kementerian Perindustrian
('kemenperin', 'kemenperin', FALSE),
('kemenperin', 'kementerian perindustrian', TRUE),
('kemenperin', 'menperin', TRUE),
('kemenperin', 'perindustrian', TRUE),

-- Kementerian Tenaga Kerja
('kemnaker', 'kemnaker', FALSE),
('kemnaker', 'kementerian tenaga kerja', TRUE),
('kemnaker', 'kementerian ketenagakerjaan', TRUE),
('kemnaker', 'menaker', TRUE),

-- Kementerian Sosial
('kemensos', 'kemensos', FALSE),
('kemensos', 'kementerian sosial', TRUE),
('kemensos', 'mensos', TRUE),
('kemensos', 'sosial', TRUE),

-- Kementerian PANRB
('kemenpan rb', 'kemenpan rb', FALSE),
('kemenpan rb', 'kementerian pendayagunaan aparatur negara dan reformasi birokrasi', TRUE),
('kemenpan rb', 'kementerian panrb', TRUE),
('kemenpan rb', 'menpan rb', TRUE),

-- Kementerian Investasi/BKPM
('kementerian investasi', 'kementerian investasi', FALSE),
('kementerian investasi', 'kementerian investasi bkpm', TRUE),
('kementerian investasi', 'bkpm', TRUE),
('kementerian investasi', 'meninvestasi', TRUE),

-- Kementerian ATR/BPN
('kementerian atr bpn', 'kementerian atr bpn', FALSE),
('kementerian atr bpn', 'kementerian agraria dan tata ruang badan pertanahan nasional', TRUE),
('kementerian atr bpn', 'kementerian atr', TRUE),
('kementerian atr bpn', 'menatr', TRUE),

-- Kementerian Perencanaan Pembangunan Nasional/Bappenas
('bappenas', 'bappenas', FALSE),
('bappenas', 'kementerian perencanaan pembangunan nasional', TRUE),
('bappenas', 'kementerian ppn bappenas', TRUE),
('bappenas', 'menppn', TRUE);

-- Insert Lembaga Negara
INSERT INTO kementerian_keywords (kementerian_name, keyword, is_alias) VALUES
-- Majelis Permusyawaratan Rakyat
('mpr', 'mpr', FALSE),
('mpr', 'majelis permusyawaratan rakyat', TRUE),
('mpr', 'majelis rakyat', TRUE),
('mpr', 'permusyawaratan rakyat', TRUE),

-- Dewan Perwakilan Rakyat
('dpr', 'dpr', FALSE),
('dpr', 'dewan perwakilan rakyat', TRUE),
('dpr', 'dewan rakyat', TRUE),
('dpr', 'perwakilan rakyat', TRUE),

-- Dewan Perwakilan Daerah
('dpd', 'dpd', FALSE),
('dpd', 'dewan perwakilan daerah', TRUE),
('dpd', 'dewan daerah', TRUE),
('dpd', 'perwakilan daerah', TRUE),

-- Mahkamah Agung
('ma', 'ma', FALSE),
('ma', 'mahkamah agung', TRUE),
('ma', 'mahkamah agung ri', TRUE),
('ma', 'agung', TRUE),

-- Mahkamah Konstitusi
('mk', 'mk', FALSE),
('mk', 'mahkamah konstitusi', TRUE),
('mk', 'mahkamah konstitusi ri', TRUE),
('mk', 'konstitusi', TRUE),

-- Badan Pemeriksa Keuangan
('bpk', 'bpk', FALSE),
('bpk', 'badan pemeriksa keuangan', TRUE),
('bpk', 'bpk ri', TRUE),
('bpk', 'pemeriksa keuangan', TRUE),

-- Komisi Yudisial
('ky', 'ky', FALSE),
('ky', 'komisi yudisial', TRUE),
('ky', 'komisi yudisial ri', TRUE),
('ky', 'yudisial', TRUE),

-- Badan Intelijen Negara
('bin', 'bin', FALSE),
('bin', 'badan intelijen negara', TRUE),
('bin', 'badan intelijen', TRUE),
('bin', 'intelijen negara', TRUE),

-- Badan Siber dan Sandi Negara
('bssn', 'bssn', FALSE),
('bssn', 'badan siber dan sandi negara', TRUE),
('bssn', 'badan siber sandi negara', TRUE),
('bssn', 'badan siber', TRUE),

-- Badan Meteorologi, Klimatologi, dan Geofisika
('bmkg', 'bmkg', FALSE),
('bmkg', 'badan meteorologi klimatologi dan geofisika', TRUE),
('bmkg', 'badan meteorologi', TRUE),
('bmkg', 'meteorologi', TRUE),

-- Badan Nasional Penanggulangan Bencana
('bnpb', 'bnpb', FALSE),
('bnpb', 'badan nasional penanggulangan bencana', TRUE),
('bnpb', 'badan penanggulangan bencana', TRUE),
('bnpb', 'penanggulangan bencana', TRUE),

-- Komisi Pemberantasan Korupsi
('kpk', 'kpk', FALSE),
('kpk', 'komisi pemberantasan korupsi', TRUE),
('kpk', 'pemberantasan korupsi', TRUE),
('kpk', 'anti korupsi', TRUE),

-- Arsip Nasional Republik Indonesia
('anri', 'anri', FALSE),
('anri', 'arsip nasional republik indonesia', TRUE),
('anri', 'arsip nasional', TRUE),
('anri', 'arsip negara', TRUE),

-- Badan Informasi Geospasial
('big', 'big', FALSE),
('big', 'badan informasi geospasial', TRUE),
('big', 'badan geospasial', TRUE),
('big', 'informasi geospasial', TRUE),

-- Badan Kepegawaian Negara
('bkn', 'bkn', FALSE),
('bkn', 'badan kepegawaian negara', TRUE),
('bkn', 'badan kepegawaian', TRUE),
('bkn', 'kepegawaian negara', TRUE),

-- Badan Nasional Sertifikasi Profesi
('bnsp', 'bnsp', FALSE),
('bnsp', 'badan nasional sertifikasi profesi', TRUE),
('bnsp', 'badan sertifikasi profesi', TRUE),
('bnsp', 'sertifikasi profesi', TRUE),

-- Badan Kependudukan dan Keluarga Berencana Nasional
('bkkbn', 'bkkbn', FALSE),
('bkkbn', 'badan kependudukan dan keluarga berencana nasional', TRUE),
('bkkbn', 'badan keluarga berencana', TRUE),
('bkkbn', 'keluarga berencana', TRUE);

-- Verifikasi hasil insert
SELECT 'Kementerian dan Lembaga yang ditambahkan:' as info;
SELECT kementerian_name, COUNT(*) as keyword_count 
FROM kementerian_keywords 
GROUP BY kementerian_name 
ORDER BY kementerian_name;
