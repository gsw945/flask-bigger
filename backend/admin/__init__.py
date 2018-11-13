# -*- coding: utf-8 -*-
'''管理后端'''
from flask import Blueprint

from ..app_env import get_config


env_cfg = get_config()
template_folder = env_cfg.get('template_folder', None)
static_folder = env_cfg.get('static_folder', None)


app_name = 'admin'
admin_app = Blueprint(
    app_name,
    __name__,
    static_folder=template_folder,
    template_folder=static_folder
)