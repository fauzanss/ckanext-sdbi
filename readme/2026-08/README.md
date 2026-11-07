# Portal Data BNPB — dokumentasi implementasi

Dokumen upgrade ada di folder ini (`readme/2026-08/`). Prefiks tiket: `SCOL-1234` sampai nomor resmi ada. Tree kerja: `ckanext-sdbi` + `ckan-compose`.

| Dokumen | Isi |
| --- | --- |
| [`PRD.md`](PRD.md) | Persyaratan: masalah, pengguna, Fase 0–4, CVE B0–B2, kriteria lulus, di luar lingkup |
| [`STATUS.md`](STATUS.md) | Laporan status: lokal vs produksi, verifikasi, risiko, langkah berikutnya |
| [`HOW-TO-IMPLEMENT.md`](HOW-TO-IMPLEMENT.md) | Cara lokal, harvest, cabut API key, sumber harvest produksi, cutover 2.10 |

**Lokal (9 Sep 2026):** CKAN **2.10.11** di http://localhost:8080. Fase 0–4 + harvest JSON REST sudah jalan. Kamar Tanggap Darurat dipilih dari **dropdown navbar**. FAQ dan kamar di Postgres `sdbi_settings` (tanpa YAML). **Gempa NTT 2026** tidak di navbar; `/gempantt2026` masih terbuka lewat URL.

**Produksi:** CKAN **2.9.11** di https://data.bnpb.go.id. B0 SQL search sudah dimatikan. Cutover 2.10 belum.

Dua lubang publikasi yang **tidak** ditutup 2FA:

1. **API key pengguna** — cabut semua key 2.9; putar token DataPusher. Lihat [`HOW-TO-IMPLEMENT.md`](HOW-TO-IMPLEMENT.md) *Cabut API key produksi*.
2. **Harvest CKAN/DCAT tanpa saring** — katalog kota (contoh Integrasi Kota Malang) sudah menelan dataset non-bencana (BPJS desil, data penduduk). Pause sumber itu; hapus paket yang tidak pantas. Lihat [`HOW-TO-IMPLEMENT.md`](HOW-TO-IMPLEMENT.md) *Sumber harvest produksi*.

CLI compose: `docker-compose`. Context Docker: `colima-ckan`. Setelah edit template/Python, restart `ckan` (lihat HOW-TO).

### Lokal vs produksi

Cara baca: bandingkan `status_show`, lalu rincian di [`STATUS.md`](STATUS.md) dan [`HOW-TO-IMPLEMENT.md`](HOW-TO-IMPLEMENT.md).

| | Lokal | Produksi |
| --- | --- | --- |
| URL | http://localhost:8080 | https://data.bnpb.go.id |
| `status_show` | [/api/3/action/status_show](http://localhost:8080/api/3/action/status_show) | [/api/3/action/status_show](https://data.bnpb.go.id/api/3/action/status_show) |
| CKAN | 2.10.11 | 2.9.11 |
| B0 SQL search | Mati | Mati |
| B1 upgrade 2.10 | Selesai | Belum |
| B2 auth SQL `sdbi` terakhir | Selesai | Belum di-deploy |
| Fase 0 2FA | Selesai | Perlu image + `security migrate` |
| Fase 1 JSON REST | Selesai (harvest Jakarta live) | Perlu image + worker sama |
| Fase 2 `/sebaran-bpbd` | Selesai | Belum di-deploy |
| Fase 3 `/bantuan` | Selesai (`sdbi_settings.faq`) | Belum di-deploy |
| Fase 4 Tanggap Darurat | Selesai (dropdown navbar; `tanggap_rooms`) | Belum di-deploy |
| Plugin khas 2.10 | `activity`, `sdbi_json_harvester` | — |
| Plugin khas 2.9 | — | `resourceauthorizer`, `dcat*` |
