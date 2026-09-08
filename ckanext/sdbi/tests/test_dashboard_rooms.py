# -*- coding: utf-8 -*-
"""Unit tests for tanggap darurat dashboard rooms."""
import os
import tempfile

import pytest

from ckanext.sdbi.lib.dashboard_rooms import (
    DashboardRoomsError,
    get_room,
    load_rooms,
    parse_rooms,
    rooms_payload,
)


SAMPLE_YAML = u"""
rooms:
  - slug: gempa-bumi
    label: Gempa Bumi
    dashboards:
      - title: Dashboard Cianjur 2022
        iframe_url: https://gis.bnpb.go.id/cianjur2022
        sumber: GIS BNPB
  - slug: banjir
    label: Banjir
    dashboards: []
  - slug: lainnya
    label: Lainnya
    dashboards:
      - title: Tanggap Darurat Nasional
        iframe_url: https://dibi.bnpb.go.id/superset/dashboard/83/?standalone=1
        sumber: DIBI Superset
"""


def _write_yaml(content):
    handle = tempfile.NamedTemporaryFile('w', suffix='.yaml', delete=False)
    handle.write(content)
    handle.close()
    return handle.name


def test_load_rooms_reads_slugs_and_empty_rooms():
    path = _write_yaml(SAMPLE_YAML)
    try:
        rooms = load_rooms(path)
    finally:
        os.unlink(path)
    assert [room['slug'] for room in rooms] == ['gempa-bumi', 'banjir', 'lainnya']
    banjir = get_room(rooms, 'banjir')
    assert banjir['dashboards'] == []


def test_get_room_returns_none_for_unknown_slug():
    path = _write_yaml(SAMPLE_YAML)
    try:
        rooms = load_rooms(path)
    finally:
        os.unlink(path)
    assert get_room(rooms, 'tsunami') is None


def test_load_rooms_rejects_missing_file():
    with pytest.raises(DashboardRoomsError):
        load_rooms('/tmp/does-not-exist-sdbi-rooms.yaml')


def test_load_rooms_without_path_falls_back_to_empty(monkeypatch):
    from ckanext.sdbi.lib import dashboard_rooms as rooms_mod

    monkeypatch.setattr(rooms_mod, 'get_json', lambda key: None)
    assert load_rooms() == []


def test_parse_rooms_rejects_http_iframe():
    with pytest.raises(DashboardRoomsError):
        parse_rooms({
            'rooms': [{
                'slug': 'banjir',
                'label': 'Banjir',
                'dashboards': [{'iframe_url': 'http://example.com/dash'}],
            }],
        })


def test_parse_rooms_rejects_javascript_url():
    with pytest.raises(DashboardRoomsError):
        parse_rooms({
            'rooms': [{
                'slug': 'banjir',
                'label': 'Banjir',
                'dashboards': [{'iframe_url': 'javascript:alert(1)'}],
            }],
        })


def test_rooms_payload_wraps_list():
    rooms = parse_rooms({
        'rooms': [{'slug': 'banjir', 'label': 'Banjir', 'dashboards': []}],
    })
    assert rooms_payload(rooms) == {
        'rooms': [{'slug': 'banjir', 'label': 'Banjir', 'dashboards': []}],
    }
