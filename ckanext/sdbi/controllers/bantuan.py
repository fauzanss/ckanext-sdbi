# -*- coding: utf-8 -*-
import os

from flask import Blueprint, request, jsonify

from ckan.plugins import toolkit

from ckanext.sdbi.lib.faq import FaqError, load_faq, search_faq

bantuan_blueprint = Blueprint('bantuan', __name__)

_FAQ_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), 'data', 'faq.yaml'
)


def _faq():
    return load_faq(_FAQ_PATH)


@bantuan_blueprint.route('/bantuan', methods=['GET'])
def index():
    try:
        faq = _faq()
    except FaqError:
        faq = {'categories': []}
    faq_categories = []
    for category in faq.get('categories') or []:
        faq_categories.append({
            'id': category.get('id'),
            'title': category.get('title'),
            'entries': list(category.get('questions') or []),
        })
    return toolkit.render(
        'bantuan/index.html',
        extra_vars={'faq_categories': faq_categories},
    )


@bantuan_blueprint.route('/bantuan/search', methods=['GET'])
def search():
    query = request.args.get('q') or ''
    try:
        faq = _faq()
    except FaqError:
        return jsonify({'results': []})
    return jsonify({'results': search_faq(faq, query)})
