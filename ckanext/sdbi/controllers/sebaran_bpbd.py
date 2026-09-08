# -*- coding: utf-8 -*-
from flask import Blueprint, request, abort, jsonify
import io
import json
import os

from ckan.plugins import toolkit
import ckan.authz as authz

from ckanext.sdbi.lib.bpbd import (
    BpbdImportError,
    csv_to_records,
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


@sebaran_bpbd_blueprint.route('/sebaran-bpbd/import', methods=['POST'])
def import_csv():
    _require_sysadmin()
    uploaded = request.files.get('csv')
    if not uploaded:
        abort(400, description='CSV file is required')
    try:
        content = uploaded.read().decode('utf-8-sig')
        records = csv_to_records(io.StringIO(content))
        geojson = records_to_geojson(records)
        if not os.path.isdir(_PUBLIC_DATA):
            os.makedirs(_PUBLIC_DATA)
        with open(_BPBD_JSON, 'w') as handle:
            json.dump(geojson, handle, ensure_ascii=False, indent=2)
    except BpbdImportError as exc:
        abort(400, description=str(exc))
    except Exception as exc:
        abort(400, description='Import failed: %s' % exc)
    return jsonify({
        'success': True,
        'imported': len(records),
        'mapped': len(geojson.get('features') or []),
    })
