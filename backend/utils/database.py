# -*- coding: utf-8 -*-
'''数据库相关函数封装'''
import sys

from sqlalchemy import create_engine
from sqlalchemy_utils import (
    database_exists,
    create_database
)


def sqlalchemy_uri(db_type, user_config=None):
    '''build sqlalchmey uri'''
    supported = {
        'sqlite': sqlite_tuple,
        'mysql': mysql_tuple
    }
    if db_type.lower() not in supported:
        raise Exception('only [{0}] supported by now'.format(','.join(supported)))
    # get uri tuple of specified db type, and unpack
    (db_config, uri_format) = supported[db_type]()
    if bool(user_config):
        if not isinstance(user_config, dict):
            raise Exception('user config parameter[user_config] must dict type')
        # update config if user specified（override default config）
        db_config.update(user_config)
    return uri_format.format(**db_config)

def mysql_tuple():
    '''define mysql uri tuple'''
    default_config = {
        'driver': 'pymysql',
        'username': 'root',
        'password': 'root',
        'host': '127.0.0.1',
        'port': 3306,
        'database': 'test',
        'charset': 'utf8'
    }
    uri_format = 'mysql+{driver}://{username}:{password}@{host}:{port}/{database}?charset={charset}'
    return (default_config, uri_format)

def sqlite_tuple():
    '''define sqlite uri tuple'''
    default_config = {
        'database': ':memory:'
    }
    uri_format = 'sqlite:///{database}'
    return (default_config, uri_format)

def get_engine(db_type='sqlite', user_config=None, **kwargs):
    '''create sqlalchemy engine'''
    # build sqlalchemy uri
    db_uri = sqlalchemy_uri(db_type, user_config=user_config)
    # ensure database is exists, instantiate and return engine
    return ensure_database(db_uri, return_engine=True, **kwargs)

def ensure_database(db_uri, return_engine=False, **kwargs):
    '''
    ensure database is existed
    return_engine: True->(not dispose engine and return it), False->(dispose engine)
    '''
    # refer:
    #     https://stackoverflow.com/questions/27910829/sqlalchemy-and-sqlite-shared-cache/35143160#35143160
    #     https://docs.sqlalchemy.org/en/latest/core/engines.html
    #     https://www.sqlite.org/inmemorydb.html
    #     https://stackoverflow.com/questions/15681387/sqlite-works-with-file-dies-with-memory/15681692#15681692
    #     https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa/48234567#48234567
    if db_uri == 'sqlite:///:memory:':
        kwargs = kwargs.copy()
        if 'sqlite3' not in globals():
            import sqlite3
        sqlite_uri = 'file::memory:?cache=shared'
        sqlite_params = {
            'check_same_thread': False
        }
        if sys.version_info.major == 3:
            sqlite_params['uri'] = True
        kwargs['creator'] = lambda: sqlite3.connect(sqlite_uri, **sqlite_params)
    engine = create_engine(db_uri, **kwargs)
    if not database_exists(engine.url):
        create_database(engine.url)
    if return_engine:
        return engine
    engine.dispose()