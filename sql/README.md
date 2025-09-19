# SQL Scripts untuk Keyword Management

Folder ini berisi script SQL untuk mengelola keywords provinsi, kabupaten/kota, dan kementerian/lembaga.

## 📁 File Structure

```
sql/
├── README.md                    # Dokumentasi ini
├── create_keyword_tables.sql    # Script untuk membuat tabel keywords
├── insert_keywords.sql          # Script untuk insert keywords baru
└── add_keyword_examples.sql     # Contoh-contoh insert keywords
```

## 🗄️ Database Tables

### 1. `provinsi_keywords`

Tabel untuk menyimpan keywords provinsi dan alias-nya.

**Structure:**

- `id` - Primary key
- `provinsi_name` - Nama provinsi (e.g., 'jawa barat')
- `keyword` - Keyword untuk matching (e.g., 'jabar', 'provinsi jawa barat')
- `is_alias` - Boolean, apakah ini alias atau nama utama
- `created_at` - Timestamp

### 2. `kabupaten_kota_keywords`

Tabel untuk menyimpan keywords kabupaten/kota dan alias-nya.

**Structure:**

- `id` - Primary key
- `kabupaten_kota_name` - Nama kabupaten/kota (e.g., 'bandung')
- `keyword` - Keyword untuk matching (e.g., 'kota bandung', 'kabupaten bandung')
- `is_alias` - Boolean, apakah ini alias atau nama utama
- `created_at` - Timestamp

### 3. `kementerian_keywords`

Tabel untuk menyimpan keywords kementerian/lembaga dan alias-nya.

**Structure:**

- `id` - Primary key
- `kementerian_name` - Nama kementerian (e.g., 'bnpb')
- `keyword` - Keyword untuk matching (e.g., 'badan nasional penanggulangan bencana')
- `is_alias` - Boolean, apakah ini alias atau nama utama
- `created_at` - Timestamp

## 🚀 Cara Menggunakan

### 1. Setup Awal (First Time)

```bash
# Jalankan script untuk membuat tabel
podman exec db psql -U ckan -d ckan -f /path/to/create_keyword_tables.sql
```

### 2. Tambah Keywords Baru

```bash
# Edit file insert_keywords.sql sesuai kebutuhan
nano insert_keywords.sql

# Jalankan script
podman exec db psql -U ckan -d ckan -f /path/to/insert_keywords.sql
```

### 3. Insert Manual

```sql
-- Tambah provinsi baru
INSERT INTO provinsi_keywords (provinsi_name, keyword, is_alias) VALUES
('provinsi baru', 'provinsi baru', FALSE),
('provinsi baru', 'alias1', TRUE);

-- Tambah kota baru
INSERT INTO kabupaten_kota_keywords (kabupaten_kota_name, keyword, is_alias) VALUES
('kota baru', 'kota baru', FALSE),
('kota baru', 'kota kota baru', TRUE);

-- Tambah kementerian baru
INSERT INTO kementerian_keywords (kementerian_name, keyword, is_alias) VALUES
('kementerian baru', 'kementerian baru', FALSE),
('kementerian baru', 'kemen baru', TRUE);
```

## 📊 Query untuk Testing

### Cek Statistik Terbaru

```sql
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
    (SELECT COUNT(*) FROM provinsi_matches) as provinsi_count,
    (SELECT COUNT(*) FROM kabupaten_kota_matches) as kabupaten_kota_count,
    (SELECT COUNT(*) FROM kementerian_matches) as kementerian_count;
```

### Cek Keywords yang Ada

```sql
-- Cek semua provinsi
SELECT provinsi_name, COUNT(*) as keyword_count
FROM provinsi_keywords
GROUP BY provinsi_name
ORDER BY provinsi_name;

-- Cek semua kabupaten/kota
SELECT kabupaten_kota_name, COUNT(*) as keyword_count
FROM kabupaten_kota_keywords
GROUP BY kabupaten_kota_name
ORDER BY kabupaten_kota_name;

-- Cek semua kementerian
SELECT kementerian_name, COUNT(*) as keyword_count
FROM kementerian_keywords
GROUP BY kementerian_name
ORDER BY kementerian_name;
```

## 🔧 Maintenance

### Hapus Keywords

```sql
-- Hapus provinsi tertentu
DELETE FROM provinsi_keywords WHERE provinsi_name = 'provinsi yang akan dihapus';

-- Hapus kota tertentu
DELETE FROM kabupaten_kota_keywords WHERE kabupaten_kota_name = 'kota yang akan dihapus';

-- Hapus kementerian tertentu
DELETE FROM kementerian_keywords WHERE kementerian_name = 'kementerian yang akan dihapus';
```

### Update Keywords

```sql
-- Update keyword provinsi
UPDATE provinsi_keywords
SET keyword = 'keyword baru'
WHERE provinsi_name = 'provinsi' AND keyword = 'keyword lama';

-- Update keyword kota
UPDATE kabupaten_kota_keywords
SET keyword = 'keyword baru'
WHERE kabupaten_kota_name = 'kota' AND keyword = 'keyword lama';

-- Update keyword kementerian
UPDATE kementerian_keywords
SET keyword = 'keyword baru'
WHERE kementerian_name = 'kementerian' AND keyword = 'keyword lama';
```

## 📈 Performance Tips

1. **Indexes**: Tabel sudah memiliki index pada kolom `keyword` untuk performa optimal
2. **Batch Insert**: Gunakan batch insert untuk menambah banyak keywords sekaligus
3. **Regular Cleanup**: Hapus keywords yang tidak digunakan untuk menjaga performa

## 🎯 Benefits

- **No Code Changes**: Tambah keywords tanpa perlu ganti code Python
- **Scalable**: Bisa handle ribuan keywords dengan performa baik
- **Flexible**: Satu entitas bisa punya banyak alias
- **Maintainable**: Admin bisa manage keywords tanpa developer
- **Fast**: Database-level matching dengan indexes
