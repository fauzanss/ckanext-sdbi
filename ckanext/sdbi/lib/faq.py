# -*- coding: utf-8 -*-
"""FAQ JSON loader and client-side search helper."""
import os

import yaml

from ckanext.sdbi.lib.settings import KEY_FAQ, get_json, resolve_json


class FaqError(ValueError):
    pass


def _empty_faq():
    return {'categories': []}


def parse_faq(data):
    if not isinstance(data, dict):
        raise FaqError('FAQ must be a JSON object')
    categories = data.get('categories')
    if not isinstance(categories, list):
        raise FaqError('FAQ must contain a categories list')
    cleaned = []
    for category in categories:
        if not isinstance(category, dict):
            raise FaqError('Each FAQ category must be an object')
        if not category.get('id') or not category.get('title'):
            raise FaqError('Each FAQ category needs id and title')
        questions = category.get('questions') or category.get('items') or []
        if not isinstance(questions, list):
            raise FaqError('FAQ category questions must be a list')
        entries = []
        for item in questions:
            if not isinstance(item, dict) or not item.get('q') or not item.get('a'):
                raise FaqError('Each FAQ item needs q and a')
            entries.append({'q': item['q'], 'a': item['a']})
        cleaned.append({
            'id': category['id'],
            'title': category['title'],
            'questions': entries,
        })
    return {'categories': cleaned}


def _read_yaml(path):
    if not path or not os.path.isfile(path):
        raise FaqError('FAQ file not found: %s' % path)
    with open(path, 'r') as handle:
        return yaml.safe_load(handle) or {}


def load_faq(path=None):
    """Load FAQ from a YAML path (tests), or from sdbi_settings."""
    if path:
        return parse_faq(_read_yaml(path))
    return resolve_json(parse_faq, get_json(KEY_FAQ), _empty_faq)


def search_faq(faq, query):
    needle = (query or '').strip().lower()
    if not needle:
        return []
    matches = []
    for category in faq.get('categories') or []:
        for item in category.get('questions') or []:
            haystack = u' '.join([
                item.get('q') or '',
                item.get('a') or '',
                category.get('title') or '',
            ]).lower()
            if needle in haystack:
                matches.append({
                    'category_id': category.get('id'),
                    'category_title': category.get('title'),
                    'q': item.get('q'),
                    'a': item.get('a'),
                })
    return matches
