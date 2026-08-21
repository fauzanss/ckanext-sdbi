import logging
import re

from flask import Blueprint, abort
from sqlalchemy import text

import ckan.model as model
from ckan.plugins import toolkit

log = logging.getLogger(__name__)

tanggap_darurat_blueprint = Blueprint('tanggap_darurat', __name__)

_LINK_RE = re.compile(r'^[A-Za-z0-9_-]{1,100}$')
_TABLE_ENSURED = False


def _ensure_embed_pages_table():
    """Create sdbi_embed_pages if missing (existing Postgres volumes skip initdb)."""
    global _TABLE_ENSURED
    if _TABLE_ENSURED:
        return
    model.Session.execute(text("""
        CREATE TABLE IF NOT EXISTS sdbi_embed_pages (
            id SERIAL PRIMARY KEY,
            link VARCHAR(100) NOT NULL UNIQUE,
            src_url TEXT NOT NULL,
            title TEXT NOT NULL,
            created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT CURRENT_TIMESTAMP
        )
    """))
    model.Session.execute(text("""
        CREATE INDEX IF NOT EXISTS idx_sdbi_embed_pages_link
            ON sdbi_embed_pages (link)
    """))
    model.Session.commit()
    _TABLE_ENSURED = True


def _get_embed_page(link):
    _ensure_embed_pages_table()
    result = model.Session.execute(text("""
        SELECT link, src_url, title
        FROM sdbi_embed_pages
        WHERE link = :link
    """), {'link': link})
    row = result.fetchone()
    if not row:
        return None
    return {
        'link': row[0],
        'src_url': row[1],
        'title': row[2],
    }


@tanggap_darurat_blueprint.route('/tanggap-darurat', methods=['GET'])
def index():
    return toolkit.render('tanggap_darurat/index.html')


@tanggap_darurat_blueprint.route('/gempantt2026', methods=['GET'])
def gis_index():
    return toolkit.render('tanggap_darurat/gis.html')


@tanggap_darurat_blueprint.route('/q/<link>', methods=['GET'])
def embed_page(link):
    if not _LINK_RE.match(link):
        abort(404)

    try:
        page = _get_embed_page(link)
    except Exception as e:
        log.error('embed_page lookup error for %s: %s', link, e)
        abort(404)

    if not page:
        abort(404)

    src_url = (page.get('src_url') or '').strip()
    if not (src_url.startswith('http://') or src_url.startswith('https://')):
        abort(404)

    page_title = page.get('title') or 'Tanggap Darurat'
    return toolkit.render(
        'tanggap_darurat/embed.html',
        extra_vars={
            'iframe_src': src_url,
            'page_title': page_title,
        },
    )
