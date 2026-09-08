# -*- coding: utf-8 -*-
"""Unit tests for FAQ JSON/YAML loader."""
import os
import tempfile

import pytest

from ckanext.sdbi.lib.faq import FaqError, load_faq, search_faq


SAMPLE_YAML = u"""
categories:
  - id: akun
    title: Akun dan login
    items:
      - q: Bagaimana cara mengaktifkan 2FA?
        a: Setelah username dan password, pindai QR code dengan aplikasi authenticator.
      - q: Saya terkunci dari akun.
        a: Hubungi sysadmin untuk reset TOTP.
  - id: dataset
    title: Dataset
    items:
      - q: Bagaimana cara mengunduh dataset?
        a: Buka halaman dataset lalu pilih sumber daya yang ingin diunduh.
"""


def test_load_faq_reads_categories_and_items():
    with tempfile.NamedTemporaryFile('w', suffix='.yaml', delete=False) as handle:
        handle.write(SAMPLE_YAML)
        path = handle.name
    try:
        data = load_faq(path)
    finally:
        os.unlink(path)
    assert len(data['categories']) == 2
    assert data['categories'][0]['id'] == 'akun'
    assert data['categories'][0]['questions'][0]['q'].startswith('Bagaimana')


def test_load_faq_rejects_missing_file():
    with pytest.raises(FaqError):
        load_faq('/tmp/does-not-exist-sdbi-faq.yaml')


def test_load_faq_without_path_falls_back_to_empty(monkeypatch):
    from ckanext.sdbi.lib import faq as faq_mod

    monkeypatch.setattr(faq_mod, 'get_json', lambda key: None)
    assert load_faq() == {'categories': []}


def test_parse_faq_from_dict():
    from ckanext.sdbi.lib.faq import parse_faq
    parsed = parse_faq({
        'categories': [{
            'id': 'akun',
            'title': 'Akun',
            'questions': [{'q': 'Apa itu 2FA?', 'a': 'Kode sekali pakai.'}],
        }],
    })
    assert parsed['categories'][0]['questions'][0]['q'] == 'Apa itu 2FA?'


def test_resolve_json_falls_back_when_db_invalid():
    from ckanext.sdbi.lib.faq import parse_faq
    from ckanext.sdbi.lib.settings import resolve_json
    called = []

    def fallback():
        called.append(True)
        return parse_faq({
            'categories': [{
                'id': 'x',
                'title': 'X',
                'questions': [{'q': 'Q', 'a': 'A'}],
            }],
        })

    result = resolve_json(parse_faq, {'not': 'faq'}, fallback)
    assert called == [True]
    assert result['categories'][0]['id'] == 'x'


def test_search_faq_filters_by_query():
    faq = {
        'categories': [
            {
                'id': 'akun',
                'title': 'Akun',
                'questions': [
                    {'q': 'Apa itu 2FA?', 'a': 'Kode sekali pakai.'},
                    {'q': 'Lupa password?', 'a': 'Gunakan reset password.'},
                ],
            }
        ]
    }
    matches = search_faq(faq, '2fa')
    assert len(matches) == 1
    assert matches[0]['q'] == 'Apa itu 2FA?'
