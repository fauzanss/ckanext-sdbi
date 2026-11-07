# -*- coding: utf-8 -*-
"""Dashboard room JSON loader for Tanggap Darurat."""
import os

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

import yaml

from ckanext.sdbi.lib.settings import KEY_TANGGAP_ROOMS, get_json, resolve_json


class DashboardRoomsError(ValueError):
    pass


def _empty_rooms():
    return []


def _https_iframe_url(url):
    raw = (url or '').strip()
    if not raw:
        return ''
    parsed = urlparse(raw)
    scheme = (parsed.scheme or '').lower()
    if scheme in ('javascript', 'data', 'vbscript'):
        raise DashboardRoomsError('iframe_url scheme is not allowed')
    if scheme != 'https' or not parsed.netloc:
        raise DashboardRoomsError('iframe_url must be HTTPS: %s' % raw)
    return raw


def parse_rooms(data):
    if isinstance(data, list):
        data = {'rooms': data}
    if not isinstance(data, dict):
        raise DashboardRoomsError('rooms payload must be a JSON object')
    rooms = data.get('rooms')
    if not isinstance(rooms, list) or not rooms:
        raise DashboardRoomsError('rooms must be a non-empty list')
    cleaned = []
    for room in rooms:
        if not isinstance(room, dict):
            raise DashboardRoomsError('Each room must be an object')
        slug = (room.get('slug') or '').strip()
        label = (room.get('label') or '').strip()
        if not slug or not label:
            raise DashboardRoomsError('Each room needs slug and label')
        dashboards = room.get('dashboards') or []
        if not isinstance(dashboards, list):
            raise DashboardRoomsError('dashboards must be a list')
        items = []
        for item in dashboards:
            if not isinstance(item, dict):
                raise DashboardRoomsError('Each dashboard must be an object')
            url = _https_iframe_url(item.get('iframe_url') or '')
            if not url:
                continue
            items.append({
                'title': item.get('title') or '',
                'iframe_url': url,
                'sumber': item.get('sumber') or '',
            })
        cleaned.append({
            'slug': slug,
            'label': label,
            'dashboards': items,
        })
    return cleaned


def rooms_payload(rooms):
    return {'rooms': rooms}


def _read_yaml(path):
    if not path or not os.path.isfile(path):
        raise DashboardRoomsError('Dashboard rooms file not found: %s' % path)
    with open(path, 'r') as handle:
        return yaml.safe_load(handle) or {}


def load_rooms(path=None):
    """Load rooms from a YAML path (tests), or from sdbi_settings."""
    if path:
        return parse_rooms(_read_yaml(path))
    return resolve_json(parse_rooms, get_json(KEY_TANGGAP_ROOMS), _empty_rooms)


def get_room(rooms, slug):
    for room in rooms or []:
        if room.get('slug') == slug:
            return room
    return None
