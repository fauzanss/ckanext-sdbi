# -*- coding: utf-8 -*-
"""Dashboard room YAML loader for Tanggap Darurat."""
import os

import yaml


class DashboardRoomsError(ValueError):
    pass


def load_rooms(path):
    if not path or not os.path.isfile(path):
        raise DashboardRoomsError('Dashboard rooms file not found: %s' % path)
    with open(path, 'r') as handle:
        data = yaml.safe_load(handle) or {}
    rooms = data.get('rooms')
    if not isinstance(rooms, list) or not rooms:
        raise DashboardRoomsError('rooms must be a non-empty list')
    cleaned = []
    for room in rooms:
        slug = (room.get('slug') or '').strip()
        label = (room.get('label') or '').strip()
        if not slug or not label:
            raise DashboardRoomsError('Each room needs slug and label')
        dashboards = room.get('dashboards') or []
        if not isinstance(dashboards, list):
            raise DashboardRoomsError('dashboards must be a list')
        cleaned.append({
            'slug': slug,
            'label': label,
            'dashboards': [
                {
                    'title': item.get('title') or '',
                    'iframe_url': item.get('iframe_url') or '',
                    'sumber': item.get('sumber') or '',
                }
                for item in dashboards
                if item.get('iframe_url')
            ],
        })
    return cleaned


def get_room(rooms, slug):
    for room in rooms or []:
        if room.get('slug') == slug:
            return room
    return None
