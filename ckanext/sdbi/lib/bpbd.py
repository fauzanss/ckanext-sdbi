# -*- coding: utf-8 -*-
"""BPBD CSV import, record validation, and Google Maps URL helpers."""
import csv
import io

try:
    from urllib.parse import quote_plus
except ImportError:
    from urllib import quote_plus


BPBD_CSV_FIELDS = [
    'kode_wilayah',
    'tingkat',
    'nama_instansi',
    'alamat',
    'lat',
    'lng',
    'telepon',
    'email',
    'jumlah_sdm',
    'catatan_sdm',
]

VALID_TINGKAT = ('provinsi', 'kabupaten')


class BpbdImportError(ValueError):
    pass


def _parse_float(value):
    if value is None:
        return None
    text = str(value).strip()
    if text == '':
        return None
    try:
        return float(text)
    except ValueError:
        raise BpbdImportError('lat/lng must be numeric: %s' % value)


def _parse_int(value, default=0):
    if value is None or str(value).strip() == '':
        return default
    try:
        return int(float(str(value).strip()))
    except ValueError:
        raise BpbdImportError('jumlah_sdm must be numeric: %s' % value)


def csv_to_records(handle):
    reader = csv.DictReader(handle)
    if not reader.fieldnames:
        raise BpbdImportError('CSV is empty')
    missing = [field for field in BPBD_CSV_FIELDS if field not in reader.fieldnames]
    if missing:
        raise BpbdImportError('CSV missing columns: %s' % ', '.join(missing))
    records = []
    for index, row in enumerate(reader, start=2):
        tingkat = (row.get('tingkat') or '').strip().lower()
        if tingkat not in VALID_TINGKAT:
            raise BpbdImportError(
                'Row %s: tingkat must be provinsi or kabupaten' % index
            )
        nama = (row.get('nama_instansi') or '').strip()
        if not nama:
            raise BpbdImportError('Row %s: nama_instansi is required' % index)
        records.append({
            'kode_wilayah': (row.get('kode_wilayah') or '').strip(),
            'tingkat': tingkat,
            'nama_instansi': nama,
            'alamat': (row.get('alamat') or '').strip(),
            'lat': _parse_float(row.get('lat')),
            'lng': _parse_float(row.get('lng')),
            'telepon': (row.get('telepon') or '').strip(),
            'email': (row.get('email') or '').strip(),
            'jumlah_sdm': _parse_int(row.get('jumlah_sdm')),
            'catatan_sdm': (row.get('catatan_sdm') or '').strip(),
        })
    return records


def build_google_maps_url(record):
    lat = record.get('lat')
    lng = record.get('lng')
    if lat is not None and lng is not None:
        return 'https://www.google.com/maps?q=%s,%s' % (lat, lng)
    alamat = (record.get('alamat') or record.get('nama_instansi') or '').strip()
    return 'https://www.google.com/maps?q=' + quote_plus(alamat)


def records_to_geojson(records):
    features = []
    for record in records:
        if record.get('lat') is None or record.get('lng') is None:
            continue
        properties = dict(record)
        properties['maps_url'] = build_google_maps_url(record)
        features.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [record['lng'], record['lat']],
            },
            'properties': properties,
        })
    return {'type': 'FeatureCollection', 'features': features}


def geojson_to_csv(geojson):
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=BPBD_CSV_FIELDS, extrasaction='ignore')
    writer.writeheader()
    for feature in geojson.get('features') or []:
        props = feature.get('properties') or {}
        row = {}
        for field in BPBD_CSV_FIELDS:
            value = props.get(field, '')
            row[field] = '' if value is None else value
        writer.writerow(row)
    return output.getvalue()
