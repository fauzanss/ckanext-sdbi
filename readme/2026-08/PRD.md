# PRD — Upgrade Portal Data BNPB

Dokumen persyaratan produk. Status ada di [`STATUS.md`](STATUS.md). Cara implementasi dan cutover ada di [`HOW-TO-IMPLEMENT.md`](HOW-TO-IMPLEMENT.md).

| Field | Nilai |
| --- | --- |
| Produk | Portal Data BNPB (`data.bnpb.go.id`) |
| Repositori | `ckanext-sdbi` (tema, rute, harvester), `ckan-compose` (image, env, Solr, worker) |
| Prefiks tiket | `SCOL-1234` sampai nomor tiket resmi ada |
| Target lokal | CKAN **2.10.11** |
| Produksi saat ini | CKAN **2.9.11** (masuk rentang CVE-2026-42031) |

---

## 1. Masalah

Portal harus tetap berfungsi sebagai katalog data terbuka kebencanaan nasional, sambil menutup insiden kebocoran kredensial, menambal CVE DataStore CKAN, dan menambah fitur yang tidak bisa dicakup harvest CKAN 2.9 (API JSON non-CKAN, peta BPBD, FAQ, kamar dashboard tanggap darurat).

## 2. Tujuan

1. Mematikan `datastore_search_sql` tanpa autentikasi (CVE-2026-42031) dan menjaganya tetap mati.
2. Memaksa login web memakai TOTP (2FA) lewat plugin security yang sudah ada.
3. Harvest dataset dari API JSON REST non-CKAN (contoh: Satu Data Jakarta).
4. Menayangkan peta BPBD dua layer (Provinsi + Kabupaten) dengan info SDM dan tautan Google Maps.
5. Menayangkan halaman FAQ / Bantuan untuk publik.
6. Menayangkan dashboard Tanggap Darurat dalam kamar per jenis bencana; kamar boleh kosong sampai URL iframe tersedia.

## 3. Di luar lingkup (sampai diminta secara eksplisit)

- Keycloak atau 2FA kustom di dalam `ckanext-sdbi`
- CKAN 2.11.5
- Mengaktifkan kembali SQL search publik / UI SQL Recline
- Aturan WAF di nginx
- Mengisi semua kamar Tanggap Darurat dengan dashboard produksi
- Commit GeoJSON Kabupaten/Kota penuh (`> 2 MB`) ke repositori
- Menyalin baris JSON harvest (`data[]`) ke DataStore / DataTables
- Memasang plugin DCAT produksi (`dcat`, harvester RDF/JSON, `structured_data`) di 2.10 sampai diminta

## 4. Pengguna

| Peran | Kebutuhan |
| --- | --- |
| Pengunjung publik | Katalog, peta, FAQ, kamar Tanggap Darurat (tanpa login) |
| Editor / admin organisasi | Terbit dataset; 2FA saat login web |
| Sysadmin | Sumber harvest, pembaruan data FAQ/peta, reset TOTP, panduan hosting iframe, admin Google Forms |

2FA web **tidak** melindungi token API. Setelah kebocoran kredensial, token tetap harus dicabut. Harvest CKAN tanpa saring juga bisa menelan dataset tidak pantas. Langkah: [`HOW-TO-IMPLEMENT.md`](HOW-TO-IMPLEMENT.md) *Cabut API key produksi* dan *Sumber harvest produksi*.

---

## 5. Persyaratan

### B0 — Penahanan SQL search

**Persyaratan:** `datastore_search_sql` tidak boleh menjadi aksi publik.

**Konfigurasi:** `CKAN__DATASTORE__SQLSEARCH__ENABLED=false` di `.ckan-env`. Recreate container (jangan hanya restart).

**Kriteria lulus:**

- `docker exec ckan env | grep SQLSEARCH` menampilkan `false`
- `help_show?name=datastore_search_sql` tidak dikenal / tidak ditemukan
- `datastore_search` (non-SQL) tetap jalan

### B1 — Upgrade inti CKAN

**Persyaratan:** Produksi harus keluar dari 2.9.11 ke jalur 2.10 yang sudah ditambal. Target lokal/staging: **2.10.11**.

**Kriteria lulus:**

- `ckan --version` menampilkan 2.10.11
- Situs, detail dataset, login, harvest, pratinjau spasial berfungsi
- Solr memakai `ckan/ckan-solr:2.10-solr9` dengan volume **baru** (data Solr 2.9 tidak dipakai ulang)

### B2 — Otorisasi SQL search default tolak

**Persyaratan:** Meski SQL search dinyalakan karena salah konfigurasi, pengguna anonim dan pengguna biasa tidak boleh menjalankannya. Hanya sysadmin.

**Kriteria lulus:**

- `sdbi` berada di urutan terakhir `CKAN__PLUGINS`
- `IAuthFunctions` berantai untuk `datastore_search_sql` di CKAN 2.10
- Uji unit di `ckanext/sdbi/tests/test_auth.py`

B2 tidak menggantikan B0 atau B1.

### Fase 0 — 2FA (TOTP)

**Persyaratan:** Setelah username + password, login web meminta kode TOTP 6 digit. Login pertama menampilkan QR code.

**Stack:** `ckanext-security` **4.1.1** (data-govt-nz), Redis DB **2**, `ckan security migrate`.

**Kriteria lulus:**

- Login di `/user/login` berlanjut ke TOTP
- Authenticator hilang: sysadmin menjalankan `ckan security reset-totp <username>`
- FAQ menjelaskan bahwa API key tidak dilindungi 2FA

### Fase 1 — Harvester JSON REST (non-CKAN)

**Persyaratan:** Admin dapat harvest metadata dari API JSON REST yang **bukan** CKAN Action API. `ckan_harvester` dan harvester DCAT produksi tidak cukup untuk `ws.jakarta.go.id/gateway/...`.

**Plugin:** `sdbi_json_harvester` (tipe Harvest: **JSON REST**). Form sama dengan CKAN dan CSW.

**Mode URL (satu dataset):** Field URL = endpoint JSON detail. Configuration opsional (`title`, `source_portal`, `default_tags` sebagai `[{"name": "…"}]`, `default_extras`). Nama dataset diambil dari query `url=` / `name=` pada URL.

**Mode banyak dataset:** `datasets[]` berisi `{name, title}` plus `detail_url_template` yang mengandung `{name}`. `list_url` untuk katalog JSON yang mengembalikan daftar dataset. `datasets[].owner_org` opsional; jika kosong, memakai organisasi sumber harvest.

Frequency **MANUAL** memerlukan Reharvest (atau `ckan harvester job`). Harvest membuat paket katalog dengan resource JSON ke API asal; **tidak** menyalin `data[]` ke DataStore.

**Kriteria lulus:**

- Tipe muncul di `/harvest` dan `ckan harvester harvesters_info` (web **dan** worker gather)
- Gather → fetch → import membuat dataset CKAN `sdbi-*` dengan tag `harvested` dan resource JSON
- Worker harvest memakai image yang sama dengan web dan memuat `CKAN__PLUGINS` (termasuk `sdbi_json_harvester`)

### Fase 2 — Peta sebaran BPBD

**Persyaratan:** Peta publik layar penuh di `/sebaran-bpbd` (header/footer CKAN disembunyikan).

- Peta MapLibre; sakelar layer administrasi (Provinsi / Kabupaten) dan titik BPBD
- Popup SDM dan tautan Google Maps
- Publik: **Unduh data** CSV (`GET /sebaran-bpbd/data.csv`)
- Sysadmin: unggah CSV (mengganti semua titik) lewat dialog di peta: `kode_wilayah,tingkat,nama_instansi,alamat,lat,lng,telepon,email,jumlah_sdm,catatan_sdm`

**Kriteria lulus:**

- Halaman terbuka; sakelar layer berfungsi; titik di atas isian batas
- Unduh CSV memakai kolom yang sama dengan impor
- GeoJSON Kabupaten boleh kosong di rilis pertama; Provinsi + titik sampel cukup

### Fase 3 — FAQ / Bantuan

**Persyaratan:** Halaman bantuan publik di `/bantuan`, perannya mirip `/bantuan` Satu Data Jakarta (FAQ bisa dicari, bukan artikel CKAN Pages).

**Konten:** JSON di tabel `sdbi_settings` (key `faq`). Sysadmin mengubah lewat `/bantuan/kelola` tanpa rebuild image.

**Kriteria lulus:**

- Kategori dan tanya-jawab tampil; chip kategori dan pencarian menyaring
- Tidak perlu login
- Sysadmin dapat menyimpan JSON FAQ ke database

### Fase 4 — Kamar Tanggap Darurat

**Persyaratan:** `/tanggap-darurat` adalah kumpulan **kamar** per jenis bencana, bukan satu iframe yang dikunci.

Kamar: Gempa Bumi, Gunung Api, Banjir, Tanah Longsor, Kekeringan, Cuaca Ekstrem, Tsunami, Karhutla, Lainnya.

Kamar kosong tetap kosong sampai URL iframe HTTPS tersedia. Sysadmin mengisi URL di `/tanggap-darurat/kelola` (JSON `sdbi_settings.tanggap_rooms`). Catatan hosting: `/tanggap-darurat/panduan` (403 untuk non-sysadmin).

**Tetap dipertahankan** (sudah ada di portal ini):

- `/gempantt2026` — dashboard GIS khusus (URL saja; tidak di navbar)
- `/data/<link>` — halaman embed dari `sdbi_embed_pages`

**Kriteria lulus:**

- Dropdown **navbar** Tanggap Darurat mengganti kamar (bukan dropdown di dalam halaman)
- Kamar kosong menampilkan pesan kamar sudah disiapkan
- Panduan dan **Kelola Dashboard** hanya untuk sysadmin
- URL GIS/embed yang ada tetap jalan

---

## 6. Dependensi dan batasan

- Image resmi 2.10 memakai `CKAN_INI=/srv/app/ckan.ini` (`production.ini` symlink).
- Jangan mengaktifkan `resourceauthorizer` di 2.10 (Pylons).
- Aktifkan `activity` (alur aktivitas dataset).
- `CKAN__DATAPUSHER__API_TOKEN` wajib di 2.10.
- Redis security tidak boleh memakai Redis DB 1 milik CKAN.
- `CKAN__WEBASSETS__PATH=/var/lib/ckan/webassets`.
- Urutan plugin: plugin harvest, lalu `sdbi_json_harvester`, **`sdbi` terakhir**.

## 7. Sukses cutover produksi

Staging (lalu produksi) menyamai lokal:

1. CKAN 2.10.11, SQLSEARCH tetap false, aksi SQL tidak dikenal
2. Login 2FA jalan; reset TOTP terdokumentasi
3. `/sebaran-bpbd`, `/bantuan`, `/tanggap-darurat`, tipe JSON REST di `/harvest` semua jalan (worker gather memuat harvester yang sama)
4. Pencarian katalog setelah `search-index rebuild`
