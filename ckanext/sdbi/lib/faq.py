# -*- coding: utf-8 -*-
"""FAQ YAML loader and client-side search helper."""
import os

import yaml


class FaqError(ValueError):
    pass


def load_faq(path):
    if not path or not os.path.isfile(path):
        raise FaqError('FAQ file not found: %s' % path)
    with open(path, 'r') as handle:
        data = yaml.safe_load(handle) or {}
    categories = data.get('categories')
    if not isinstance(categories, list):
        raise FaqError('FAQ YAML must contain a categories list')
    for category in categories:
        if not category.get('id') or not category.get('title'):
            raise FaqError('Each FAQ category needs id and title')
        questions = category.get('questions') or category.get('items') or []
        if not isinstance(questions, list):
            raise FaqError('FAQ category questions must be a list')
        for item in questions:
            if not item.get('q') or not item.get('a'):
                raise FaqError('Each FAQ item needs q and a')
        category['questions'] = questions
        category.pop('items', None)
    return {'categories': categories}


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
