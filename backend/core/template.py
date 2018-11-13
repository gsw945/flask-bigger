# -*- coding: utf-8 -*-
'''模板相关操作、配置'''
import uuid
from datetime import datetime

from flask import url_for


def with_template_filters(app):
    '''自定义模板过滤器'''
    @app.template_filter('UUID')
    def filter_uuid(_val=None):
        '''生成uuid'''
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        return uuid.uuid5(uuid.NAMESPACE_DNS, ts).hex

    # print(app.jinja_env.list_templates()) # debug
    
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.trim_blocks = True

    return app