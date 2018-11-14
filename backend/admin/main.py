# -*- coding: utf-8 -*-
'''管理后端入口文件'''
import os
import json
from datetime import datetime, timedelta

from flask import (
    current_app,
    request,
    render_template,
    make_response,
    jsonify,
    redirect,
    url_for,
    abort,
    flash,
    g,
    session
)

from sqlalchemy.sql.expression import and_
from sqlalchemy.sql import (
    func as db_func,
    label as db_label
)

from . import admin_app
from .models import User, db
from .. import utils
from .views import view_user
from .secure import login_required, admin_required

@admin_app.route(r'', methods=['GET'])
@login_required
def index_view():
    # 今日订单总数
    today_count = 0
    # 今日待接单数
    today_unreceived = 0
    # 今日已接单数
    today_received = 0
    # 累计总数
    total_count = 0
    # 昨日总单数
    yestoday_count = 0
    # 昨日待接单数
    yestoday_unreceived = 0

    params = {
        'today_count': today_count,
        'today_unreceived': today_unreceived,
        'today_received': today_received,
        'total_count': total_count,
        'yestoday_count': yestoday_count,
        'yestoday_unreceived': yestoday_unreceived
    }
    return render_template('admin/index.html', **params)

@admin_app.route(r'/login', methods=['GET', 'POST'])
def login_view():
    in_g = hasattr(g, 'login_user') and not getattr(g, 'login_user') is None
    in_s = 'login_user' in session and not session['login_user'] is None
    if in_g or in_s:
        g.login_user = session['login_user']
        return redirect(url_for('admin.index_view'))
    if request.method == 'POST':
        req_account = request.values.get('txt_account', None)
        req_password = request.values.get('txt_password', None)
        if not req_account is None and not req_password is None:
            _account = req_account.strip()
            _password = req_password.strip()
            if bool(_account):
                if not bool(_password):
                    flash('请填写密码')
                else:
                    dbq = User.query.filter(and_(
                        User.email == _account,
                        User.password == User.encrypt_string(_password)
                    ))
                    if dbq.count() > 0:
                        user_obj = dbq.first()
                        if user_obj.disable:
                            flash('账户已被禁用，请联系管理员')
                        else:
                            logined_user = user_obj.to_dict()
                            session['login_user'] = logined_user
                            _next = request.values.get('next', None)
                            if not bool(_next):
                                _next = url_for('admin.index_view')
                            return redirect(_next)
                    else:
                        flash('用户名或密码错误')
            else:
                flash('请填写电子邮件')
        else:
            flash('缺少参数')
    return render_template('admin/login.html')

@admin_app.route(r'/logout', methods=['GET'])
@login_required
def logout_view():
    session.pop('login_user', None)
    return redirect(url_for('admin.index_view'))

@admin_app.route(r'/gen-pwd', methods=['GET', 'POST'])
def gen_pwd_view():
    raw_str = request.values.get('raw', None)
    if raw_str is None:
        abort(400)
    return jsonify({
        'raw': raw_str,
        'encrypted': User.encrypt_string(raw_str),
        'md5': utils.md5(raw_str),
        'hashkiller': 'https://hashkiller.co.uk/md5-decrypter.aspx'
    })

@admin_app.route(r'/change-pwd', methods=['GET', 'POST'])
@login_required
def change_pwd_view():
    global db
    origin_pwd = request.values.get('origin_pwd', None)
    new_pwd = request.values.get('new_pwd', None)
    re_pwd = request.values.get('re_pwd', None)
    ret = {}
    if User.encrypt_string(origin_pwd) == g.login_user['password']:
        if new_pwd == re_pwd:
            try:
                User.query.filter_by(id=g.login_user['id']).update({
                    'password': User.encrypt_string(new_pwd)
                })
                db.session.commit()
                ret = {
                    'error': 0,
                    'desc': '修改成功'
                }
            except Exception as ex:
                db.session.rollback()
                ret = {
                    'error': 3,
                    'desc': '修改失败'
                }
        else:
            ret = {
                'error': 2,
                'desc': '两次密码输入不一致'
            }
    else:
        ret = {
            'error': 1,
            'desc': '当前密码不正确'
        }
    return json.dumps(ret)