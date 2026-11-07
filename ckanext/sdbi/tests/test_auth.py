from ckanext.sdbi.auth import datastore_search_sql, get_auth_functions


def test_anonymous_denied():
    for context in ({}, {'user': None}, {'user': ''}):
        result = datastore_search_sql(context, {})
        assert result['success'] is False
        assert 'sysadmin' in result['msg'].lower()


def test_normal_user_denied():
    result = datastore_search_sql(
        {'user': 'alice'}, {}, is_sysadmin=lambda _user: False
    )
    assert result['success'] is False


def test_sysadmin_allowed():
    result = datastore_search_sql(
        {'user': 'admin'}, {}, is_sysadmin=lambda _user: True
    )
    assert result == {'success': True}


def test_only_sql_action_is_registered():
    funcs = get_auth_functions()
    assert set(funcs) == {'datastore_search_sql'}
    assert funcs['datastore_search_sql'] is datastore_search_sql
    assert 'datastore_search' not in funcs
    assert 'datastore_create' not in funcs
