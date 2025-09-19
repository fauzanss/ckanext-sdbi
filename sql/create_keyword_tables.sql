-- Create tables for dynamic keyword matching
-- This allows adding new provinces, cities, and ministries without code changes

-- Table for provinces and their aliases
CREATE TABLE IF NOT EXISTS provinsi_keywords (
    id SERIAL PRIMARY KEY,
    provinsi_name VARCHAR(100) NOT NULL,
    keyword VARCHAR(100) NOT NULL,
    is_alias BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(provinsi_name, keyword)
);

-- Table for kabupaten/kota and their aliases
CREATE TABLE IF NOT EXISTS kabupaten_kota_keywords (
    id SERIAL PRIMARY KEY,
    kabupaten_kota_name VARCHAR(100) NOT NULL,
    keyword VARCHAR(100) NOT NULL,
    is_alias BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(kabupaten_kota_name, keyword)
);

-- Table for ministries/institutions and their aliases
CREATE TABLE IF NOT EXISTS kementerian_keywords (
    id SERIAL PRIMARY KEY,
    kementerian_name VARCHAR(100) NOT NULL,
    keyword VARCHAR(100) NOT NULL,
    is_alias BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(kementerian_name, keyword)
);

-- Insert 38 provinsi data dengan 4 alias masing-masing
INSERT INTO provinsi_keywords (provinsi_name, keyword, is_alias) VALUES
-- BALI
('bali', 'bali', FALSE),
('bali', 'provinsi bali', TRUE),
('bali', 'pulau bali', TRUE),
('bali', 'daerah bali', TRUE),

-- BANGKA BELITUNG
('bangka belitung', 'bangka belitung', FALSE),
('bangka belitung', 'provinsi bangka belitung', TRUE),
('bangka belitung', 'babel', TRUE),
('bangka belitung', 'kepulauan bangka belitung', TRUE),

-- BANTEN
('banten', 'banten', FALSE),
('banten', 'provinsi banten', TRUE),
('banten', 'daerah banten', TRUE),
('banten', 'wilayah banten', TRUE),

-- BENGKULU
('bengkulu', 'bengkulu', FALSE),
('bengkulu', 'provinsi bengkulu', TRUE),
('bengkulu', 'daerah bengkulu', TRUE),
('bengkulu', 'wilayah bengkulu', TRUE),

-- DI YOGYAKARTA
('di yogyakarta', 'di yogyakarta', FALSE),
('di yogyakarta', 'provinsi di yogyakarta', TRUE),
('di yogyakarta', 'yogyakarta', TRUE),
('di yogyakarta', 'jogja', TRUE),

-- DKI JAKARTA
('dki jakarta', 'dki jakarta', FALSE),
('dki jakarta', 'provinsi dki jakarta', TRUE),
('dki jakarta', 'jakarta', TRUE),
('dki jakarta', 'jakarta raya', TRUE),

-- GORONTALO
('gorontalo', 'gorontalo', FALSE),
('gorontalo', 'provinsi gorontalo', TRUE),
('gorontalo', 'daerah gorontalo', TRUE),
('gorontalo', 'wilayah gorontalo', TRUE),

-- JAMBI
('jambi', 'jambi', FALSE),
('jambi', 'provinsi jambi', TRUE),
('jambi', 'daerah jambi', TRUE),
('jambi', 'wilayah jambi', TRUE),

-- JAWA BARAT
('jawa barat', 'jawa barat', FALSE),
('jawa barat', 'provinsi jawa barat', TRUE),
('jawa barat', 'jabar', TRUE),
('jawa barat', 'west java', TRUE),

-- JAWA TENGAH
('jawa tengah', 'jawa tengah', FALSE),
('jawa tengah', 'provinsi jawa tengah', TRUE),
('jawa tengah', 'jateng', TRUE),
('jawa tengah', 'central java', TRUE),

-- JAWA TIMUR
('jawa timur', 'jawa timur', FALSE),
('jawa timur', 'provinsi jawa timur', TRUE),
('jawa timur', 'jatim', TRUE),
('jawa timur', 'east java', TRUE),

-- KALIMANTAN BARAT
('kalimantan barat', 'kalimantan barat', FALSE),
('kalimantan barat', 'provinsi kalimantan barat', TRUE),
('kalimantan barat', 'kalbar', TRUE),
('kalimantan barat', 'west kalimantan', TRUE),

-- KALIMANTAN SELATAN
('kalimantan selatan', 'kalimantan selatan', FALSE),
('kalimantan selatan', 'provinsi kalimantan selatan', TRUE),
('kalimantan selatan', 'kalsel', TRUE),
('kalimantan selatan', 'south kalimantan', TRUE),

-- KALIMANTAN TENGAH
('kalimantan tengah', 'kalimantan tengah', FALSE),
('kalimantan tengah', 'provinsi kalimantan tengah', TRUE),
('kalimantan tengah', 'kalteng', TRUE),
('kalimantan tengah', 'central kalimantan', TRUE),

-- KALIMANTAN TIMUR
('kalimantan timur', 'kalimantan timur', FALSE),
('kalimantan timur', 'provinsi kalimantan timur', TRUE),
('kalimantan timur', 'kaltim', TRUE),
('kalimantan timur', 'east kalimantan', TRUE),

-- KALIMANTAN UTARA
('kalimantan utara', 'kalimantan utara', FALSE),
('kalimantan utara', 'provinsi kalimantan utara', TRUE),
('kalimantan utara', 'kaltara', TRUE),
('kalimantan utara', 'north kalimantan', TRUE),

-- KEPULAUAN RIAU
('kepulauan riau', 'kepulauan riau', FALSE),
('kepulauan riau', 'provinsi kepulauan riau', TRUE),
('kepulauan riau', 'kepri', TRUE),
('kepulauan riau', 'riau islands', TRUE),

-- LAMPUNG
('lampung', 'lampung', FALSE),
('lampung', 'provinsi lampung', TRUE),
('lampung', 'daerah lampung', TRUE),
('lampung', 'wilayah lampung', TRUE),

-- MALUKU
('maluku', 'maluku', FALSE),
('maluku', 'provinsi maluku', TRUE),
('maluku', 'daerah maluku', TRUE),
('maluku', 'wilayah maluku', TRUE),

-- MALUKU UTARA
('maluku utara', 'maluku utara', FALSE),
('maluku utara', 'provinsi maluku utara', TRUE),
('maluku utara', 'malut', TRUE),
('maluku utara', 'north maluku', TRUE),

-- NANGGROE ACEH DARUSSALAM (NAD)
('nanggroe aceh darussalam', 'nanggroe aceh darussalam', FALSE),
('nanggroe aceh darussalam', 'provinsi nanggroe aceh darussalam', TRUE),
('nanggroe aceh darussalam', 'aceh', TRUE),
('nanggroe aceh darussalam', 'nad', TRUE),

-- NUSA TENGGARA BARAT (NTB)
('nusa tenggara barat', 'nusa tenggara barat', FALSE),
('nusa tenggara barat', 'provinsi nusa tenggara barat', TRUE),
('nusa tenggara barat', 'ntb', TRUE),
('nusa tenggara barat', 'west nusa tenggara', TRUE),

-- NUSA TENGGARA TIMUR (NTT)
('nusa tenggara timur', 'nusa tenggara timur', FALSE),
('nusa tenggara timur', 'provinsi nusa tenggara timur', TRUE),
('nusa tenggara timur', 'ntt', TRUE),
('nusa tenggara timur', 'east nusa tenggara', TRUE),

-- PAPUA
('papua', 'papua', FALSE),
('papua', 'provinsi papua', TRUE),
('papua', 'daerah papua', TRUE),
('papua', 'wilayah papua', TRUE),

-- PAPUA BARAT
('papua barat', 'papua barat', FALSE),
('papua barat', 'provinsi papua barat', TRUE),
('papua barat', 'pabar', TRUE),
('papua barat', 'west papua', TRUE),

-- PAPUA BARAT DAYA
('papua barat daya', 'papua barat daya', FALSE),
('papua barat daya', 'provinsi papua barat daya', TRUE),
('papua barat daya', 'pabar daya', TRUE),
('papua barat daya', 'southwest papua', TRUE),

-- PAPUA PEGUNUNGAN
('papua pegunungan', 'papua pegunungan', FALSE),
('papua pegunungan', 'provinsi papua pegunungan', TRUE),
('papua pegunungan', 'papgun', TRUE),
('papua pegunungan', 'highland papua', TRUE),

-- PAPUA SELATAN
('papua selatan', 'papua selatan', FALSE),
('papua selatan', 'provinsi papua selatan', TRUE),
('papua selatan', 'papsel', TRUE),
('papua selatan', 'south papua', TRUE),

-- PAPUA TENGAH
('papua tengah', 'papua tengah', FALSE),
('papua tengah', 'provinsi papua tengah', TRUE),
('papua tengah', 'papteng', TRUE),
('papua tengah', 'central papua', TRUE),

-- RIAU
('riau', 'riau', FALSE),
('riau', 'provinsi riau', TRUE),
('riau', 'daerah riau', TRUE),
('riau', 'wilayah riau', TRUE),

-- SULAWESI BARAT
('sulawesi barat', 'sulawesi barat', FALSE),
('sulawesi barat', 'provinsi sulawesi barat', TRUE),
('sulawesi barat', 'sulbar', TRUE),
('sulawesi barat', 'west sulawesi', TRUE),

-- SULAWESI SELATAN
('sulawesi selatan', 'sulawesi selatan', FALSE),
('sulawesi selatan', 'provinsi sulawesi selatan', TRUE),
('sulawesi selatan', 'sulsel', TRUE),
('sulawesi selatan', 'south sulawesi', TRUE),

-- SULAWESI TENGAH
('sulawesi tengah', 'sulawesi tengah', FALSE),
('sulawesi tengah', 'provinsi sulawesi tengah', TRUE),
('sulawesi tengah', 'sulteng', TRUE),
('sulawesi tengah', 'central sulawesi', TRUE),

-- SULAWESI TENGGARA
('sulawesi tenggara', 'sulawesi tenggara', FALSE),
('sulawesi tenggara', 'provinsi sulawesi tenggara', TRUE),
('sulawesi tenggara', 'sultra', TRUE),
('sulawesi tenggara', 'southeast sulawesi', TRUE),

-- SULAWESI UTARA
('sulawesi utara', 'sulawesi utara', FALSE),
('sulawesi utara', 'provinsi sulawesi utara', TRUE),
('sulawesi utara', 'sulut', TRUE),
('sulawesi utara', 'north sulawesi', TRUE),

-- SUMATERA BARAT
('sumatera barat', 'sumatera barat', FALSE),
('sumatera barat', 'provinsi sumatera barat', TRUE),
('sumatera barat', 'sumbar', TRUE),
('sumatera barat', 'west sumatra', TRUE),

-- SUMATERA SELATAN
('sumatera selatan', 'sumatera selatan', FALSE),
('sumatera selatan', 'provinsi sumatera selatan', TRUE),
('sumatera selatan', 'sumsel', TRUE),
('sumatera selatan', 'south sumatra', TRUE),

-- SUMATERA UTARA
('sumatera utara', 'sumatera utara', FALSE),
('sumatera utara', 'provinsi sumatera utara', TRUE),
('sumatera utara', 'sumut', TRUE),
('sumatera utara', 'north sumatra', TRUE);

-- Insert sample kabupaten/kota data
INSERT INTO kabupaten_kota_keywords (kabupaten_kota_name, keyword, is_alias) VALUES
-- Major cities
('bandung', 'bandung', FALSE),
('bandung', 'kota bandung', TRUE),
('bandung', 'kabupaten bandung', TRUE),

('surabaya', 'surabaya', FALSE),
('surabaya', 'kota surabaya', TRUE),

('bogor', 'bogor', FALSE),
('bogor', 'kota bogor', TRUE),
('bogor', 'kabupaten bogor', TRUE),

('medan', 'medan', FALSE),
('medan', 'kota medan', TRUE),

('badung', 'badung', FALSE),
('badung', 'kabupaten badung', TRUE),

('semarang', 'semarang', FALSE),
('semarang', 'kota semarang', TRUE),

('makassar', 'makassar', FALSE),
('makassar', 'kota makassar', TRUE),

('palembang', 'palembang', FALSE),
('palembang', 'kota palembang', TRUE),

('tangerang', 'tangerang', FALSE),
('tangerang', 'kota tangerang', TRUE),
('tangerang', 'kabupaten tangerang', TRUE),

('bekasi', 'bekasi', FALSE),
('bekasi', 'kota bekasi', TRUE),
('bekasi', 'kabupaten bekasi', TRUE),

('depok', 'depok', FALSE),
('depok', 'kota depok', TRUE),

('malang', 'malang', FALSE),
('malang', 'kota malang', TRUE),
('malang', 'kabupaten malang', TRUE),

('solo', 'solo', FALSE),
('solo', 'surakarta', TRUE),
('solo', 'kota solo', TRUE),
('solo', 'kota surakarta', TRUE),

('pekanbaru', 'pekanbaru', FALSE),
('pekanbaru', 'kota pekanbaru', TRUE),

('padang', 'padang', FALSE),
('padang', 'kota padang', TRUE),

('bandar lampung', 'bandar lampung', FALSE),
('bandar lampung', 'kota bandar lampung', TRUE),

('denpasar', 'denpasar', FALSE),
('denpasar', 'kota denpasar', TRUE),

('samarinda', 'samarinda', FALSE),
('samarinda', 'kota samarinda', TRUE),

('balikpapan', 'balikpapan', FALSE),
('balikpapan', 'kota balikpapan', TRUE),

('pontianak', 'pontianak', FALSE),
('pontianak', 'kota pontianak', TRUE),

('manado', 'manado', FALSE),
('manado', 'kota manado', TRUE),

('mataram', 'mataram', FALSE),
('mataram', 'kota mataram', TRUE),

('kupang', 'kupang', FALSE),
('kupang', 'kota kupang', TRUE),

('jayapura', 'jayapura', FALSE),
('jayapura', 'kota jayapura', TRUE),

('merauke', 'merauke', FALSE),
('merauke', 'kabupaten merauke', TRUE),

('sorong', 'sorong', FALSE),
('sorong', 'kota sorong', TRUE),

('ambon', 'ambon', FALSE),
('ambon', 'kota ambon', TRUE),

('ternate', 'ternate', FALSE),
('ternate', 'kota ternate', TRUE),

('kendari', 'kendari', FALSE),
('kendari', 'kota kendari', TRUE),

('palu', 'palu', FALSE),
('palu', 'kota palu', TRUE),

('gorontalo', 'gorontalo', FALSE),
('gorontalo', 'kota gorontalo', TRUE),

('banjarmasin', 'banjarmasin', FALSE),
('banjarmasin', 'kota banjarmasin', TRUE),

('palangkaraya', 'palangkaraya', FALSE),
('palangkaraya', 'kota palangkaraya', TRUE),

('tarakan', 'tarakan', FALSE),
('tarakan', 'kota tarakan', TRUE),

('bontang', 'bontang', FALSE),
('bontang', 'kota bontang', TRUE),

('singkawang', 'singkawang', FALSE),
('singkawang', 'kota singkawang', TRUE),

('batam', 'batam', FALSE),
('batam', 'kota batam', TRUE),

('tanjung pinang', 'tanjung pinang', FALSE),
('tanjung pinang', 'kota tanjung pinang', TRUE),

('pangkal pinang', 'pangkal pinang', FALSE),
('pangkal pinang', 'kota pangkal pinang', TRUE),

('banda aceh', 'banda aceh', FALSE),
('banda aceh', 'kota banda aceh', TRUE);

-- Kementerian dan Lembaga data akan diinsert menggunakan file terpisah
-- Jalankan: insert_kementerian_lembaga.sql untuk data lengkap

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_provinsi_keywords_keyword ON provinsi_keywords(keyword);
CREATE INDEX IF NOT EXISTS idx_kabupaten_kota_keywords_keyword ON kabupaten_kota_keywords(keyword);
CREATE INDEX IF NOT EXISTS idx_kementerian_keywords_keyword ON kementerian_keywords(keyword);
