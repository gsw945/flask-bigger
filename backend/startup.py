# -*- coding: utf-8 -*-
'''后端启动文件

web启动入口文件，封装flask-app全局设置
'''
from flask import (
    Flask
)
from werkzeug.contrib.fixers import ProxyFix

from flask_debugtoolbar import DebugToolbarExtension


from .core.cdn import with_cdn_setting
from .core.database import db
from .core.exception import get_http_exception_handler
from .core.hook import with_request_hook
from .core.route import (
    with_top_level_routes, RegexConverter
)
from .core.middlewares import PrefixMiddleware
from .core.template import with_template_filters
from .utils import ensure_database, get_engine
from .app_env import get_config

from .app_map import blueprints


def create_app(config):
    '''创建应用实例'''
    env_cfg = get_config()
    template_folder = env_cfg.get('template_folder', None)
    static_folder = env_cfg.get('static_folder', None)
    app = Flask(
        __name__,
        template_folder=template_folder,
        static_folder=static_folder
    )
    
    # Flask内部选项配置    
    app.config['SECRET_KEY'] = config.get('secret', '!secret!')
    app.debug = config.get('debug', False) # app.config['DEBUG']
    app.config['JSON_AS_ASCII'] = False
    if config.get('debugtoolbar', False):
        # 分析器
        app.config['DEBUG_TB_PROFILER_ENABLED'] = True
        # 启用模板编辑
        app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True
        # 禁用 拦截重定向
        app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
        toolbar = DebugToolbarExtension(app)

    # 路径前缀
    if app.debug and bool(config.get('url_prefix', None)):
        app.wsgi_app = PrefixMiddleware(app.wsgi_app, prefix=config['url_prefix'])

    # 配置数据库
    db_cfg = env_cfg['db_config']
    # 数据库类型
    db_type = db_cfg['type']
    db_cfg.pop('type')
    db_kwargs = config.get('db_kwargs', {})
    engine = get_engine(db_type, user_config=db_cfg, **db_kwargs)
    # Flask-SQLAlchemy配置
    app.config['SQLALCHEMY_DATABASE_URI'] = engine.url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # 关联Flask-SQLAlchemy到当前app
    db.init_app(app)
    app.db = db
    with app.app_context():
        db.create_all()

    # cdn 配置
    app.config['CDN_LIST'] = env_cfg.get('cdn_list', {})
    app.config['USE_CDN'] = config.get('use_cdn', False)

    # 对路由规则增加正则支持
    app.url_map.converters['regex'] = RegexConverter

    # HTTP异常处理
    app.handle_http_exception = get_http_exception_handler(app)

    # 加载CDN配置
    app = with_cdn_setting(app)

    # 加载自定义模板过滤器
    app = with_template_filters(app)
    
    # 设置应用钩子
    app = with_request_hook(app)

    # 设置应用路由(顶级)
    app = with_top_level_routes(app)

    # 注册蓝图(子应用)
    for item in blueprints:
        app.register_blueprint(item[1], url_prefix=item[0])
    
    # WSGI代理支持
    app.wsgi_app = ProxyFix(app.wsgi_app, num_proxies=1)

    return app