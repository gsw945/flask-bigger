# -*- coding: utf-8 -*-
from functools import wraps

from flask import (
    g,
    session,
    request,
    redirect,
    url_for,
    current_app,
    abort
)


def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        not_in_g = not hasattr(g, 'login_user') or g.login_user is None
        not_in_s = not 'login_user' in session or session['login_user'] is None
        if not_in_g and not_in_s:
            _route = 'admin.login_view'
            return redirect(url_for(_route, next=request.url))
        if not_in_g:
            g.login_user = session['login_user']
        return func(*args, **kwargs)
    return decorated_function

def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        in_g = hasattr(g, 'login_user') and not getattr(g, 'login_user') is None
        in_s = 'login_user' in session and not session['login_user'] is None
        if in_g or in_s:
            g_admin = in_g and getattr(g, 'login_user').is_admin
            s_admin = in_s and 'is_admin' in session['login_user'] and bool(session['login_user']['is_admin'])
            if g_admin or s_admin:
                if not in_g:
                    g.login_user = session['login_user']
                return func(*args, **kwargs)
            else:
                return abort(403)
        else:
            _route = 'admin.login_view'
            return redirect(url_for(_route, next=request.url))
    return decorated_function