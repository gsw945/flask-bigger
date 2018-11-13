# -*- coding: utf-8 -*-
'''数据库调用入口'''
import sys

from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy as SQLAlchemyOriginal


# refer: http://flask-sqlalchemy.pocoo.org/2.3/config/#using-custom-metadata-and-naming-conventions
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
metadata = MetaData(naming_convention=convention)

class SQLAlchemy(SQLAlchemyOriginal):
    def apply_driver_hacks(self, app, info, options):
        # refer: https://dev.mysql.com/doc/connector-python/
        if info.drivername == 'mysql+mysqlconnector':
            options['connect_args'] = {'time_zone': 'Asia/Shanghai'}
        elif info.database == ':memory:':
            if 'sqlite3' not in globals():
                import sqlite3
            sqlite_uri = 'file::memory:?cache=shared'
            sqlite_params = {
                'check_same_thread': False
            }
            if sys.version_info.major == 3:
                sqlite_params['uri'] = True
            options['creator'] = lambda: sqlite3.connect(sqlite_uri, **sqlite_params)
        super(SQLAlchemy, self).apply_driver_hacks(app, info, options)

db = SQLAlchemy(metadata=metadata)