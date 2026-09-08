Batas wilayah untuk peta BPBD.

- provinsi.geojson: layer Provinsi (disederhanakan, sumber turunan BIG/Kemendagri).
- kabupaten.geojson: layer Kabupaten/Kota. File ini mulai kosong agar repo tetap ringan.
  Untuk mengisi, letakkan GeoJSON FeatureCollection Kabupaten/Kota yang sudah di-simplify
  (sumber open: geoBoundaries IDN ADM2 atau GeoJSON Kemendagri/BIG).
  Jangan commit file > 2 MB; load on demand per provinsi lebih baik untuk produksi.
