# -*- coding: utf-8 -*-
'''异常处理'''
from functools import wraps

from flask import (
    request,
    jsonify,
    render_template_string
)


def get_http_exception_handler(app):
    """
    # refer: https://stackoverflow.com/questions/29332056/global-error-handler-for-any-exception#44083675
    Overrides the default http exception handler to return JSON.
    """
    handle_http_exception = app.handle_http_exception
    @wraps(handle_http_exception)
    def ret_val(exception):
        exc = handle_http_exception(exception)
        is_ajax = request.headers.get('X-Requested-With', None) == 'XMLHttpRequest'
        is_api = 'X-Api' in request.headers
        resp = ''
        err = {
            'code': exc.code,
            'name': exc.name,
            'description': exc.description
        }
        if is_ajax or is_api:
            resp = jsonify(err)
        else:
            tmpl = ''.join([
                '<!DOCTYPE html>',
                '<html>',
                '<head>',
                    '<title>{{ code }} {{ name }}</title>',
                '</head>',
                '<body>',
                    '<h2>{{ code }} {{ name }}</h2>',
                    '<p>{{ description }}</p>',
                    '<p>&#8674;&#8608; <a href="/">Home Page</a></p>'
                '</body>',
                '</html>'
            ])
            resp = render_template_string(tmpl, **err)
        return resp, exc.code
    return ret_val