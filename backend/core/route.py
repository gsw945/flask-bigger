# -*- coding: utf-8 -*-
'''路由相关操作、配置'''
import os

from flask import (
    make_response,
    render_template,
    send_from_directory
)
from werkzeug.routing import BaseConverter


class RegexConverter(BaseConverter):
    '''
    正则路由规则支持
    from: https://stackoverflow.com/questions/5870188/does-flask-support-regular-expressions-in-its-url-routing/5872904#5872904
    '''
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


def with_top_level_routes(app):
    '''顶级路由'''

    @app.route(r'/<regex("(favicon\.(ico|png))|(robots\.txt)"):_file>')
    def favicon_robots(_file):
        _dir = os.path.dirname(app.static_folder)
        file_path = os.path.join(_dir, _file)
        if os.path.exists(file_path):
            # return app.send_static_file(_file)
            return send_from_directory(_dir, _file)
        else:
            return make_response(''), 204

    @app.route(r'/')
    def view_index():
        return render_template('index.html')

    return app
