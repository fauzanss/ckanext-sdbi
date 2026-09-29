# Portal Data BNPB — dokumentasi implementasi

Prefiks tiket: `SCOL-1234` sampai nomor resmi ada. Tree: `ckanext-sdbi` + `ckan-compose`.

## Dokumen utama (paparan 29 Sep 2026)

**[`DOC-2026-09-29.md`](DOC-2026-09-29.md)** — status + justifikasi embed dinamis + screenshot (termasuk kelola Bantuan / Tanggap) + how-to step-by-step.

| Dokumen pendukung | Isi |
| --- | --- |
| [`PRD.md`](PRD.md) | Persyaratan resmi Fase 0–4, B0–B2 |
| [`STATUS.md`](STATUS.md) | Ringkas; detail di DOC |
| [`HASIL.md`](HASIL.md) | Indeks screenshot; detail di DOC |
| [`HOW-TO-IMPLEMENT.md`](HOW-TO-IMPLEMENT.md) | How-to panjang; ringkas di DOC |

**Lokal:** CKAN **2.10.11** di http://localhost:8080. Fase 0–4 + harvest JSON REST jalan.  
**Produksi:** CKAN **2.9.11** di https://data.bnpb.go.id. B0 SQL search mati. Cutover 2.10 belum.

Dua lubang publikasi yang **tidak** ditutup 2FA:

1. **API key pengguna** — cabut semua key 2.9; putar DataPusher. Lihat DOC bagian B.
2. **Harvest tanpa saring** — jeda katalog penuh; hapus paket non-bencana. Lihat DOC bagian B.

CLI: `docker-compose`. Context Docker: `colima-ckan`.

### Lokal vs produksi

| | Lokal | Produksi |
| --- | --- | --- |
| URL | http://localhost:8080 | https://data.bnpb.go.id |
| `status_show` | [/api/3/action/status_show](http://localhost:8080/api/3/action/status_show) | [/api/3/action/status_show](https://data.bnpb.go.id/api/3/action/status_show) |
| CKAN | 2.10.11 | 2.9.11 |
| B0 SQL search | Mati | Mati |
| B2 Auth SQL / `sdbi` terakhir | Selesai | Selesai |
| B1 upgrade 2.10 | Selesai | Belum |
| Fase 0–4 | Selesai di lokal | Belum cutover |
