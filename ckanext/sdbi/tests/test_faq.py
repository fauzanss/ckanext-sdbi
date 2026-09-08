# -*- coding: utf-8 -*-
"""Unit tests for FAQ YAML loader."""
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
