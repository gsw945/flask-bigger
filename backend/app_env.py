# -*- coding: utf-8 -*-
'''读取应用环境变量配置'''
import os
import json


def get_config():
    '''读取配置'''
    root = os.environ.get('PROJ_ROOT', os.getcwd())

    # cdn列表
    cdn_list = {}
    with open(os.path.join(root, 'config', 'cdn.json'), 'r') as cdn_f:
        cdn_list = json.loads(cdn_f.read())

    # 数据库配置
    db_config = {}
    with open(os.path.join(root, 'config', 'database.json'), 'r') as db_f:
        db_config = json.loads(db_f.read())

    return {
        'cdn_list': cdn_list,
        'db_config': db_config,
        'template_folder': os.path.join(root, 'frontend', 'templates'),
        'static_folder': os.path.join(root, 'frontend', 'static')
    }