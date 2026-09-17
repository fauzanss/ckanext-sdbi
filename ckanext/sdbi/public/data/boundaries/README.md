Batas wilayah untuk peta BPBD.

- `provinsi.geojson`: layer Provinsi (disederhanakan).
- `kabupaten.geojson`: layer Kabupaten/Kota dari
  `data/maps/batas-kota-kab/Batas_Admin_Kabkot_Fix.shp`
  (field: Kode, NAMOBJ, WADMKK, WADMPR, KDPKAB, TIPADM).

Raw SHP under `data/maps/` is gitignored (too large). Keep a local copy to regenerate.

Regenerate kabupaten (target ≤ 2–3 MB):

```bash
npx --yes mapshaper \
  ckanext/sdbi/data/maps/batas-kota-kab/Batas_Admin_Kabkot_Fix.shp \
  -filter-fields Kode,NAMOBJ,WADMKK,WADMPR,KDPKAB,TIPADM \
  -simplify 0.5% keep-shapes \
  -o format=geojson precision=0.0001 \
  ckanext/sdbi/public/data/boundaries/kabupaten.geojson
```

Current simplify `0.5%` yields ~1.7 MB. Raise toward `2%` only if outlines look too crude and size stays ≤ 3 MB. Do not serve raw `.shp` to the browser.
