# Laporan status — Upgrade Portal Data BNPB

Laporan kondisi terhadap [`PRD.md`](PRD.md). Cara implementasi dan cutover: [`HOW-TO-IMPLEMENT.md`](HOW-TO-IMPLEMENT.md).

| Field | Nilai |
| --- | --- |
| Tanggal laporan | 9 September 2026 |
| Branch | `ckanext-sdbi` dan `ckan-compose`: `upgrade-ckan-security-etc` |
| URL lokal | http://localhost:8080 |
| Produksi | https://data.bnpb.go.id (masih CKAN 2.9.11) |

Commit harvest: sdbi `20687d5`, compose `37c41b2`. Settings FAQ/kamar: sdbi `239cc06`, compose `de479a7`. Navbar Tanggap Darurat: sdbi `74a71d5`. Sebaran layar penuh: sdbi `117caeb`.

---

## 1. Lingkungan

| Lingkungan | CKAN | Image / Solr |
| --- | --- | --- |
| Produksi | **2.9.11** | `ghcr.io/keitaroinc/ckan:2.9.11-focal` (rentang CVE `< 2.10.10`) |
| Compose lokal | **2.10.11** | `ckan/ckan-base:2.10.11-py3.10` + `ckan/ckan-solr:2.10-solr9` |

---

## 2. Status persyaratan

| ID | Persyaratan | Lokal | Produksi | Bukti / celah |
| --- | --- | --- | --- | --- |
| B0 | `CKAN__DATASTORE__SQLSEARCH__ENABLED=false` | **Selesai** | **Selesai** | Flag env. Tetap false setelah 2.10. |
| B2 | Auth SQL default tolak (`sdbi` terakhir) | **Selesai** | Belum di-deploy | `ckanext/sdbi/auth.py`; IAuthFunctions berantai di 2.10 |
| B1 | CKAN 2.10.11 | **Selesai** | **Belum dimulai** | Lokal `ckan --version` 2.10.11 |
| Fase 0 | 2FA TOTP | **Selesai** | Perlu rebuild image + `security migrate` | security 4.1.1, Redis DB 2, QR di login pertama |
| Fase 1 | Harvester JSON REST | **Selesai** | Perlu image produksi + worker yang sama | Tipe **JSON REST**; sumber `jakarta1` sudah import `sdbi-kerusakan-pada-…` |
| Fase 2 | `/sebaran-bpbd` | **Selesai** | Belum di-deploy | Peta layar penuh MapLibre; unduh/unggah CSV |
| Fase 3 | `/bantuan` | **Selesai** | Belum di-deploy | Chip + cari; JSON `sdbi_settings.faq` (tanpa YAML) |
| Fase 4 | Kamar `/tanggap-darurat` | **Selesai** | Perlu cutover 2.10 | Dropdown **navbar**; JSON `tanggap_rooms`; `/kelola` sysadmin; iframe HTTPS |

---

## 3. Verifikasi lokal (9 Sep 2026)

| Pemeriksaan | Hasil |
| --- | --- |
| Beranda, `/dataset`, detail dataset | 200 |
| `status_show` | 2.10.11; plugin termasuk `activity`, `sdbi_json_harvester`; `sdbi` terakhir |
| `/sebaran-bpbd` | 200, peta layar penuh, sakelar layer, unduh CSV |
| `/bantuan` | 200; chip kategori; cari; tipe 16px |
| `/bantuan/kelola` | 403 anonim; sysadmin menyimpan JSON `faq` |
| `/tanggap-darurat` | 200, kamar dari dropdown navbar (bukan kontrol di halaman) |
| `/tanggap-darurat/kelola` | 403 anonim; iframe harus HTTPS |
| `/tanggap-darurat?jenis=banjir` | Teks kamar kosong |
| `/tanggap-darurat/panduan` | 403 untuk anonim |
| `/gempantt2026` | 200 lewat URL; tidak di navbar |
| `/harvest` | Tipe JSON REST; form tidak auto-pilih JSON REST |
| JSON REST live (Jakarta) | Gather/fetch/import **berhasil** dari Docker setelah worker memuat plugin; paket di org `pvmbg` |
| `datastore_search_sql` | Tidak terdaftar / tertahan |
| Healthcheck | `ckan` healthy (`wget`); worker harvest tanpa probe HTTP |

Plugin produksi 2.9 yang **belum** di lokal: `dcat*`, `structured_data`, `resourceauthorizer` (sengaja).

---

## 4. Risiko dan sisa pekerjaan

| Item | Dampak | Catatan |
| --- | --- | --- |
| Produksi masih 2.9.11 | CVE sampai cutover B1 | B0 adalah kunci produksi saat ini |
| Image produksi belum di-bake 2.10 | Worker/web bisa beda plugin | Lokal sudah: `image: ckan-compose-ckan` + `CKAN__PLUGINS` di start worker |
| Harvest MANUAL tanpa Reharvest | Sumber ada, `job_count=0`, tidak ada dataset | Harus Reharvest atau `ckan harvester job` |
| Harvest hanya metadata + tautan JSON | Tabel `data[]` tidak di DataStore | Sesuai Fase 1; salin ke DataStore belum diminta |
| Slug contoh di config | Paket kosong `sdbi-another-jakarta-slug` | Hapus dari Config; hapus dataset dummy |
| GeoJSON Kabupaten kosong | Layer kabupaten tanpa poligon | Tambah ADM2 yang disederhanakan nanti |
| Kamar Tanggap kosong | Sesuai desain | Isi iframe di `/tanggap-darurat/kelola` |
| API key produksi masih yang lama | Token lolos 2FA | Cabut semua key 2.9 sekarang; putar DataPusher; cabut JWT lagi setelah 2.10 |
| Harvest katalog kota tanpa saring | Dataset tidak pantas / data pribadi di portal | ≈372 paket harvested; jeda sumber Integrasi Kota Malang; hapus BPJS/penduduk dll. |
| Fase 0–4 belum di produksi | Celah fitur | Kirim bersama image 2.10 |
| DCAT produksi tidak di 2.10 | RDF/JSON-LD katalog | Bukan pengganti `sdbi_json_harvester` |

---

## 5. Langkah berikutnya (produksi)

1. Cabut semua API key pengguna produksi 2.9; putar token DataPusher (lihat [`HOW-TO-IMPLEMENT.md`](HOW-TO-IMPLEMENT.md))
2. Jeda harvest katalog penuh; hapus paket non-bencana harvested (lihat HOW-TO *Sumber harvest produksi*)
3. Rebuild staging ke 2.10.11 memakai [`HOW-TO-IMPLEMENT.md`](HOW-TO-IMPLEMENT.md)
4. Ulangi pemeriksaan lokal di staging (termasuk `harvesters_info` di **gather**)
5. Jendela maintenance produksi: `db upgrade`, Solr 9, `security migrate`, reindex
6. Recreate web **dan** worker harvest dari image yang sama; cabut JWT 2.10
7. Jangan mengaktifkan kembali SQL search

Urutan: B0 (selesai) → B2 di tree (selesai) → B1 staging/produksi → Fase 0/1 di image web+worker → Fase 2–4 ikut image yang sama.
