# -*- coding: utf-8 -*-
from flask import Blueprint, Response, request, abort, jsonify
import io
import json
import os

from ckan.plugins import toolkit
import ckan.authz as authz

from ckanext.sdbi.lib.bpbd import (
    BpbdImportError,
    csv_to_records,
    geojson_to_csv,
    records_to_geojson,
)

sebaran_bpbd_blueprint = Blueprint('sebaran_bpbd', __name__)

_PUBLIC_DATA = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), 'public', 'data'
)
_BPBD_JSON = os.path.join(_PUBLIC_DATA, 'bpbd.json')


def _require_sysadmin():
    user = getattr(toolkit.current_user, 'name', None) or ''
    if not authz.is_sysadmin(user):
        abort(403, description='Access denied. Admin privileges required.')


def _load_bpbd_geojson():
    if not os.path.isfile(_BPBD_JSON):
        return {'type': 'FeatureCollection', 'features': []}
    with open(_BPBD_JSON, 'r') as handle:
        return json.load(handle)


@sebaran_bpbd_blueprint.route('/sebaran-bpbd', methods=['GET'])
def index():
    geojson = _load_bpbd_geojson()
    return toolkit.render(
        'sebaran_bpbd/index.html',
        extra_vars={
            'bpbd_count': len(geojson.get('features') or []),
        },
    )


@sebaran_bpbd_blueprint.route('/sebaran-bpbd/data.geojson', methods=['GET'])
def data_geojson():
    return jsonify(_load_bpbd_geojson())


@sebaran_bpbd_blueprint.route('/sebaran-bpbd/data.csv', methods=['GET'])
def data_csv():
    csv_text = geojson_to_csv(_load_bpbd_geojson())
    return Response(
        csv_text.encode('utf-8-sig'),
        mimetype='text/csv',
        headers={
            'Content-Disposition': 'attachment; filename="sebaran-bpbd.csv"',
        },
    )


@sebaran_bpbd_blueprint.route('/sebaran-bpbd/import', methods=['POST'])
def import_csv():
    _require_sysadmin()
    uploaded = request.files.get('csv')
    if not uploaded:
        return _import_error('Berkas CSV wajib diunggah.')
    try:
        content = uploaded.read().decode('utf-8-sig')
        records = csv_to_records(io.StringIO(content))
        geojson = records_to_geojson(records)
        if not os.path.isdir(_PUBLIC_DATA):
            os.makedirs(_PUBLIC_DATA)
        with open(_BPBD_JSON, 'w') as handle:
            json.dump(geojson, handle, ensure_ascii=False, indent=2)
    except BpbdImportError as exc:
        return _import_error(str(exc))
    except Exception as exc:
        return _import_error('Impor gagal: %s' % exc)
    return jsonify({
        'success': True,
        'imported': len(records),
        'mapped': len(geojson.get('features') or []),
    })


def _import_error(message, status=400):
    return jsonify({'success': False, 'error': message}), status
