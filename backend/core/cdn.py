# -*- coding: utf-8 -*-
'''后端主要业务文件'''
import os

from flask import url_for

from ..utils import (
    set_query_parameter,
    random_uuid
)


def with_cdn_setting(app):
    '''cdn设置'''
    @app.template_global('static_url')
    def static_url(filename):
        use_cdn = app.config['USE_CDN']

        url = ''
        is_cdn = False
        if filename in app.config['CDN_LIST']:
            cdn_item = app.config['CDN_LIST'][filename]
            if use_cdn and 'cdn' in cdn_item:
                url = cdn_item['cdn']
                is_cdn = True
            else:
                url = url_for('static', filename=cdn_item['local'])
        else:
            url = url_for('static', filename=filename)
        '''
        # 使用第三方库furl添加查询参数
        from furl import furl
        url = furl(url).add({'_v': app.site_version}).url
        '''
        # 使用标准库构造的方法添加查询参数
        url = set_query_parameter(url, '_v', app.site_version)
        if app.debug and not is_cdn:
            url = set_query_parameter(url, '_t', random_uuid())
        return url

    return app