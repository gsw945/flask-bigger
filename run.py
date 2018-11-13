# -*- coding: utf-8 -*-
'''测试阶段-启动文件'''
import os
import sys

from werkzeug.routing import EndpointPrefix

from backend.startup import create_app
from backend.utils import touch, md5


def get_site_version(root):
    '''获取网站版本'''
    vf = os.path.join(root, 'site.version')
    if not os.path.exists(vf):
        touch(vf)
    v = None
    with open(vf, 'r+') as f:
        v = f.read().strip()
        if not bool(v):
            v = '0.0.0'
            f.write(v)
    return v

def init_admin(app):
    '''初始化管理员用户'''
    with app.test_request_context():
        from backend.admin.models import User

        db = app.db
        default_email = 'admin@gsw945.com'
        if User.query.filter_by(email=default_email).count() < 1:
            user_obj = User()
            user_obj.name = '玖亖伍'
            user_obj.email = default_email
            user_obj.password = User.encrypt_string('administrator')
            user_obj.is_admin = True
            db.session.add(user_obj)
            db.session.commit()
            print('添加初始数据成功')
        else:
            user_obj = User.query.first().to_dict()
        if isinstance(user_obj, User):
            print(user_obj)

def start_server(run_cfg=None, is_deploy=False):
    '''启动web服务器'''
    if not bool(run_cfg):
        run_cfg = {}
    proj_root = os.path.abspath(os.path.dirname(__file__))
    os.environ['PROJ_ROOT'] = proj_root
    site_version = get_site_version(proj_root)
    os.environ['SITE_VERSION'] = site_version
    config = {
        'use_cdn': False,
        'debug': run_cfg.get('debug', False),
        'secret': md5('!secret!'),
        'url_prefix': None,
        'debugtoolbar': True
    }
    app = create_app(config)
    app.proj_root = proj_root
    app.site_version = site_version

    @app.before_first_request
    def init_user(*args, **kwargs):
        print(args)
        print(kwargs)
        init_admin(app)

    if 'host' in run_cfg and 'port' in run_cfg:
        print_host = run_cfg['host']
        if print_host == '0.0.0.0':
            if sys.platform == 'win32' or os.name == 'nt':
                print_host = '127.0.0.1'
        print('=' * 28, 'visit by', '=' * 28)
        print('    http://{0}:{1}/'.format(print_host, run_cfg['port']))
        print('=' * 66)

    if is_deploy:
        return app
    app.run(**run_cfg)

if __name__ == '__main__':
    run_cfg = {
        'host': '0.0.0.0',
        'port': 5556,
        'debug': True,
        'threaded': True
    }
    start_server(run_cfg)