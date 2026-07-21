from flask import Blueprint

from ckan.plugins import toolkit

tanggap_darurat_blueprint = Blueprint('tanggap_darurat', __name__)


@tanggap_darurat_blueprint.route('/tanggap-darurat', methods=['GET'])
def index():
    return toolkit.render('tanggap_darurat/index.html')
