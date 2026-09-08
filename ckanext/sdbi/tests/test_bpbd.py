# -*- coding: utf-8 -*-
"""Unit tests for BPBD CSV import and Google Maps URL building."""
import io
import pytest

from ckanext.sdbi.lib.bpbd import (
    BPBD_CSV_FIELDS,
    BpbdImportError,
    build_google_maps_url,
    csv_to_records,
    records_to_geojson,
)


SAMPLE_CSV = u"""kode_wilayah,tingkat,nama_instansi,alamat,lat,lng,telepon,email,jumlah_sdm,catatan_sdm
31,provinsi,BPBD DKI Jakarta,Jl. Medan Merdeka Selatan,-6.175392,106.827153,021-123,bpbd@jakarta.go.id,120,Personel TRC 40
3201,kabupaten,BPBD Kabupaten Bogor,Cibinong,-6.4817,106.8540,0251-123,bpbd@bogorkab.go.id,80,SAR 12
"""


def test_csv_to_records_parses_valid_rows():
    records = csv_to_records(io.StringIO(SAMPLE_CSV))
    assert len(records) == 2
    assert records[0]['nama_instansi'] == 'BPBD DKI Jakarta'
    assert records[0]['tingkat'] == 'provinsi'
    assert records[0]['lat'] == pytest.approx(-6.175392)
    assert records[0]['jumlah_sdm'] == 120


def test_csv_to_records_rejects_missing_columns():
    with pytest.raises(BpbdImportError):
        csv_to_records(io.StringIO('nama_instansi,lat\nBPBD,-6.1\n'))


def test_csv_to_records_rejects_invalid_tingkat():
    bad = SAMPLE_CSV.replace('provinsi', 'kecamatan', 1)
    with pytest.raises(BpbdImportError):
        csv_to_records(io.StringIO(bad))


def test_build_google_maps_url_prefers_coordinates():
    url = build_google_maps_url({'lat': -6.175392, 'lng': 106.827153, 'alamat': 'Monas'})
    assert url == 'https://www.google.com/maps?q=-6.175392,106.827153'


def test_build_google_maps_url_falls_back_to_address():
    url = build_google_maps_url({'lat': None, 'lng': None, 'alamat': 'Jl. Medan Merdeka Selatan'})
    assert url.startswith('https://www.google.com/maps?q=')
    assert 'Medan' in url


def test_records_to_geojson_skips_rows_without_coordinates():
    records = csv_to_records(io.StringIO(SAMPLE_CSV))
    records.append({
        'kode_wilayah': '99',
        'tingkat': 'provinsi',
        'nama_instansi': 'Tanpa koordinat',
        'alamat': 'Unknown',
        'lat': None,
        'lng': None,
        'telepon': '',
        'email': '',
        'jumlah_sdm': 0,
        'catatan_sdm': '',
    })
    geojson = records_to_geojson(records)
    assert geojson['type'] == 'FeatureCollection'
    assert len(geojson['features']) == 2
    assert BPBD_CSV_FIELDS
