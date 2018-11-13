# -*- coding: utf-8 -*-
'''应用钩子

请求前验证、请求后清理资源、访问统计等操作
'''
from flask import (
    redirect,
    request,
    abort,
    session
)


def with_request_hook(app):
    '''请求钩子'''
    @app.before_request
    def before_request():
        if app.debug:
            script_name = request.environ.get('SCRIPT_NAME', '/')
            # 调试模式，而且带有地址前缀时，为强制调试模式(多为本地)
            if len(script_name) > 1:
                if request.values.get('clear_session', 'None') in ['1', 'true']:
                    session.clear()
                    print('execute `session.clear()`')
                # 暂时禁用模板缓存
                app.jinja_env.cache = {}
            user_info = session.get('user_info', None)
            if user_info is None:
                if request.values.get('local_debug', 'None') in ['1', 'true']:
                    print('local debug set session')
                    user_info = {
                    }
                    session['user_info'] = user_info

    @app.after_request
    def after_request(response):
        pass
        return response

    @app.teardown_request
    def teardown_request(exception):
        pass

    return app
