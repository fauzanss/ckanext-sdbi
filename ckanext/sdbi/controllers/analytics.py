import io
from datetime import datetime, timedelta

from flask import Blueprint, request, make_response as response

from ckan import model
from ckan.common import c
from ckan.plugins import toolkit

# Flask Blueprint for Analytics
analytics_blueprint = Blueprint('analytics', __name__)


def _require_login():
    if not c.user:
        return toolkit.redirect_to(toolkit.url_for('user.login'))
    return None


@analytics_blueprint.route('/analytics', methods=['GET'])
def analytics_index():
    need_login = _require_login()
    if need_login:
        return need_login

    end_default = datetime.utcnow().date()
    start_default = end_default - timedelta(days=7)

    return toolkit.render('analytics/index.html', extra_vars={
        'start_date': request.args.get('start_date', start_default.isoformat()),
        'end_date': request.args.get('end_date', end_default.isoformat()),
    })


@analytics_blueprint.route('/analytics/export', methods=['GET', 'POST'])
def analytics_export():
    need_login = _require_login()
    if need_login:
        return need_login

    start_str = request.args.get('start_date') or request.form.get('start_date')
    end_str = request.args.get('end_date') or request.form.get('end_date')

    try:
        if start_str:
            start_dt = datetime.fromisoformat(start_str)
        else:
            start_dt = datetime.utcnow() - timedelta(days=7)
        if end_str:
            end_dt = datetime.fromisoformat(end_str) + timedelta(days=1)
        else:
            end_dt = datetime.utcnow() + timedelta(days=1)
    except ValueError:
        start_dt = datetime.utcnow() - timedelta(days=7)
        end_dt = datetime.utcnow() + timedelta(days=1)

    from sqlalchemy import text
    query = text(
        """
        SELECT access_timestamp, url, tracking_type, COALESCE(user_key, 'anonymous') AS user_key
        FROM tracking_raw
        WHERE access_timestamp >= :start_dt AND access_timestamp < :end_dt
        ORDER BY access_timestamp ASC
        """
    )

    rows = model.Session.execute(query, {
        'start_dt': start_dt,
        'end_dt': end_dt,
    })

    html = io.StringIO()
    html.write("<!DOCTYPE html><html><head><meta charset=\"utf-8\"></head><body>")
    html.write("<table border=\"1\" cellspacing=\"0\" cellpadding=\"4\">")
    html.write("<tr><th>Timestamp</th><th>URL</th><th>Type</th><th>User</th></tr>")
    for r in rows:
        ts = r.access_timestamp.isoformat() if r.access_timestamp else ''
        url = r.url or ''
        t = r.tracking_type or ''
        user = r.user_key or ''

        def esc(s):
            return (s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')) if isinstance(s, str) else s

        html.write(f"<tr><td>{esc(ts)}</td><td>{esc(url)}</td><td>{esc(t)}</td><td>{esc(user)}</td></tr>")
    html.write("</table></body></html>")

    data = html.getvalue().encode('utf-8')
    resp = response(data)
    resp.headers['Content-Type'] = 'application/vnd.ms-excel; charset=utf-8'
    filename = f"analytics_{start_dt.date().isoformat()}_{(end_dt - timedelta(days=1)).date().isoformat()}.xls"
    resp.headers['Content-Disposition'] = f'attachment; filename=\"{filename}\"'
    return resp


