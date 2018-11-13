# -*- coding: utf-8 -*-
'''通用零散的函数封装'''
import os
import sys
from datetime import datetime
import uuid
import re
import hashlib
try:
    # python 3
    from urllib.parse import (
        urlencode,
        parse_qs,
        urlsplit,
        urlunsplit
    )
except ImportError:
    # python 2
    from urllib import urlencode
    from urlparse import (
        parse_qs,
        urlsplit,
        urlunsplit
    )


def md5(origin_str):
    '''计算md5'''
    m5 = hashlib.md5()
    try:
        m5.update(origin_str)
    except (TypeError, UnicodeEncodeError):
        m5.update(origin_str.encode('utf-8', 'ignore'))
    return m5.hexdigest()

def random_uuid():
    '''获取随机uuid'''
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    return uuid.uuid5(uuid.NAMESPACE_DNS, ts).hex

def touch(fname):
    '''创建文件'''
    open(fname, 'ab').close()
    os.utime(fname, None)

def email_validate(text):
    pattern = r'^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{1,5}|[0-9]{1,3})(\]?)$'
    return bool(re.match(pattern, text))

def phone_validate(text):
    pattern = r'^[1][3,4,5,7,8][0-9]{9}$'
    return bool(re.match(pattern, text))

def datetime_validate(dt_str, dt_fmt):
    '''
    验证时间字符串是否符合指定的格式

    :param dt_str: 时间字符串
    :param dt_fmt: 时间格式
    :type dt_str: str
    :type dt_fmt: str
    :return: 验证是否通过
    :rtype: bool
    '''
    is_ok = False
    try:
        datetime.strptime(dt_str, dt_fmt)
        is_ok = True
    except ValueError:
        pass
    return is_ok

def set_query_parameter(url, param_name, param_value):
    """
    Given a URL, set or replace a query parameter and return the modified URL.

    >>> set_query_parameter('http://example.com?foo=bar&biz=baz', 'foo', 'stuff')
    'http://example.com?foo=stuff&biz=baz'
    """
    # from: https://stackoverflow.com/questions/4293460/how-to-add-custom-parameters-to-an-url-query-string-with-python#12897375
    scheme, netloc, path, query_string, fragment = urlsplit(url)
    query_params = parse_qs(query_string)

    query_params[param_name] = [param_value]
    new_query_string = urlencode(query_params, doseq=True)

    return urlunsplit((scheme, netloc, path, new_query_string, fragment))