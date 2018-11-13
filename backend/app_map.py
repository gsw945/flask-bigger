# -*- coding: utf-8 -*-
'''（子）应用路径映射'''
from .admin.main import admin_app


blueprints = [
    ('/admin', admin_app)
]