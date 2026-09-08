# -*- coding: utf-8 -*-
"""Key-value JSON settings stored in PostgreSQL (sdbi_settings)."""
import json
import logging

from sqlalchemy import text

log = logging.getLogger(__name__)

KEY_FAQ = 'faq'
KEY_TANGGAP_ROOMS = 'tanggap_rooms'

_TABLE_ENSURED = False

_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS sdbi_settings (
    key TEXT PRIMARY KEY,
    value JSONB NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_by TEXT
)
"""


class SettingsError(ValueError):
    pass


def ensure_table():
    global _TABLE_ENSURED
    if _TABLE_ENSURED:
        return
    import ckan.model as model
    model.Session.execute(text(_CREATE_TABLE))
    model.Session.commit()
    _TABLE_ENSURED = True


def get_json(key):
    try:
        ensure_table()
        import ckan.model as model
        result = model.Session.execute(
            text('SELECT value FROM sdbi_settings WHERE key = :key'),
            {'key': key},
        )
        row = result.fetchone()
    except Exception as exc:
        log.warning('sdbi_settings get_json(%s) failed: %s', key, exc)
        return None
    if not row:
        return None
    value = row[0]
    if isinstance(value, str):
        try:
            return json.loads(value)
        except ValueError:
            return None
    return value


def set_json(key, value, user=''):
    if not key:
        raise SettingsError('settings key is required')
    if not isinstance(value, (dict, list)):
        raise SettingsError('settings value must be a JSON object or list')
    ensure_table()
    import ckan.model as model
    model.Session.execute(text("""
        INSERT INTO sdbi_settings (key, value, updated_at, updated_by)
        VALUES (:key, CAST(:value AS jsonb), CURRENT_TIMESTAMP, :updated_by)
        ON CONFLICT (key) DO UPDATE SET
            value = EXCLUDED.value,
            updated_at = CURRENT_TIMESTAMP,
            updated_by = EXCLUDED.updated_by
    """), {
        'key': key,
        'value': json.dumps(value, ensure_ascii=False),
        'updated_by': user or '',
    })
    model.Session.commit()


def resolve_json(parse_fn, db_value, fallback_fn):
    """Parse DB JSON when valid; otherwise use fallback_fn()."""
    if db_value is not None:
        try:
            return parse_fn(db_value)
        except (ValueError, TypeError) as exc:
            log.warning('sdbi_settings value rejected: %s', exc)
    return fallback_fn()
