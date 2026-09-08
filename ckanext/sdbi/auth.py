_DENY_MSG = 'Only sysadmins may use datastore_search_sql'


def _ckan_is_sysadmin(user):
    import ckan.authz as authz

    return bool(authz.is_sysadmin(user))


def datastore_search_sql(context, data_dict, is_sysadmin=None):
    user = context.get('user') or ''
    if not user:
        return {'success': False, 'msg': _DENY_MSG}
    if is_sysadmin is None:
        is_sysadmin = _ckan_is_sysadmin
    if is_sysadmin(user):
        return {'success': True}
    return {'success': False, 'msg': _DENY_MSG}


def get_auth_functions():
    return {
        'datastore_search_sql': datastore_search_sql,
    }
