# -*- coding: utf-8 -*-
'''子应用s'''
from ..app_env import get_config


env_cfg = get_config()
template_folder = env_cfg.get('template_folder', None)
static_folder = env_cfg.get('static_folder', None)