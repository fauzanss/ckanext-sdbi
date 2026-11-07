# -*- coding: utf-8 -*-
import logging

from flask import Blueprint, abort, redirect, request

import ckan.authz as authz
import ckan.model as model
from ckan.lib.helpers import flash_error, flash_success
from ckan.logic import NotFound
from ckan.plugins import toolkit

log = logging.getLogger(__name__)

mfa_blueprint = Blueprint('sdbi_mfa', __name__)


def _current_username():
    return getattr(toolkit.current_user, 'name', None) or ''


def _require_sysadmin():
    if not authz.is_sysadmin(_current_username()):
        abort(403, description='Access denied. Admin privileges required.')


def reset_totp_for_user_id(user_id):
    """Rotate TOTP secret and clear last challenge so the user re-enrolls."""
    from ckanext.security.model import SecurityTOTP

    context = {
        'model': model,
        'session': model.Session,
        'user': _current_username(),
        'ignore_auth': True,
    }
    user_dict = toolkit.get_action('user_show')(context, {'id': user_id})
    username = user_dict['name']
    SecurityTOTP.create_for_user(username)
    log.info('Sysadmin %s reset 2FA for user %s', _current_username(), username)
    return user_dict


@mfa_blueprint.route('/user/<id>/reset-2fa', methods=['POST'])
def reset_2fa(id):
    _require_sysadmin()
    try:
        user_dict = reset_totp_for_user_id(id)
    except NotFound:
        abort(404)
    except Exception as exc:
        log.exception('Failed to reset 2FA for %s', id)
        flash_error('Gagal mereset 2FA: %s' % exc)
        return toolkit.redirect_to('user.read', id=id)

    flash_success(
        '2FA untuk %s sudah direset. Pengguna harus memindai QR baru saat login berikutnya.'
        % user_dict['name']
    )
    next_url = request.form.get('next') or ''
    allowed_prefix = toolkit.url_for('user.read', id=user_dict['name'])
    if not next_url.startswith('/user/'):
        next_url = allowed_prefix
    return redirect(next_url)


@mfa_blueprint.route('/user/<id>/2fa', methods=['GET', 'POST'])
def configure(id):
    from ckanext.security import utils as security_utils
    security_utils.check_user_and_access()
    extra = security_utils.configure_mfa(id)
    return toolkit.render('mfa/configure.html', extra_vars={'c': extra})


@mfa_blueprint.route('/user/<id>/2fa/new', methods=['POST'])
def new_secret(id):
    from ckanext.security import utils as security_utils
    security_utils.check_user_and_access()
    extra = security_utils.configure_mfa(id)
    if not getattr(extra, 'is_myself', False):
        abort(403)
    security_utils.new(id)
    return toolkit.redirect_to('sdbi_mfa.configure', id=id)
