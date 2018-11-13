# -*- coding: utf-8 -*-
'''用户管理'''
import json

from flask import (
    current_app,
    request,
    abort,
    render_template,
    jsonify,
    session
)

from .. import admin_app
from ..models import User, db
from ..secure import login_required, admin_required


@admin_app.route(r'/user/list', methods=['GET'])
@admin_required
def user_list():
    '''用户列表'''
    user_list = User.query.all()
    print(user_list)
    return render_template('admin/user/list.html', user_list=user_list)

@admin_app.route(r'/user/list', methods=['GET', 'POST'])
@admin_required
def user_list_ajax():
    _offset = request.values.get('offset', None)
    _limit = request.values.get('limit', None)
    Q = User.query.filter_by(deleted=False)
    total = Q.count()
    if not _offset is None and _offset.isdigit():
        _offset = int(_offset)
        Q = Q.offset(_offset)
    if not _limit is None and _limit.isdigit():
        _limit = int(_limit)
        Q = Q.limit(_limit)
    ret_data = []
    for user_obj in Q.all():
        ret_data.append(user_obj.to_dict(with_pwd=False))
    ret = {
        'rows': ret_data,
        'total': total,
        'error': 0,
        'desc': 'ok'
    }
    return jsonify(ret)

@admin_app.route(r'/user/delete-disable', methods=['GET', 'POST'])
@admin_required
def user_delete_or_disable():
    '''编辑用户信息'''
    action = request.values.get('action', None)
    user_id = request.values.get('id', None)
    ret = {}
    if action in ['disable', 'delete']:
        if not user_id is None and user_id.isdigit():
            user_id = int(user_id)
            if session['login_user']['id'] != user_id:
                user_obj = User.query.get(user_id)
                if isinstance(user_obj, User):
                    if action == 'disable':
                        user_obj.disable = True
                        db.session.commit()
                    elif action == 'delete':
                        user_obj.deleted = True
                        db.session.commit()
                    ret = {
                        'error': 0,
                        'desc': '操作成功'
                    }
                else:
                    ret = {
                        'error': 4,
                        'desc': '请求的用户不存在'
                    }
            else:
                ret = {
                    'error': 3,
                    'desc': '不能对自己进行权限操作'
                }
        else:
            ret = {
                'error': 2,
                'desc': '缺少参数或参数无效'
            }
    else:
        ret = {
            'error': 1,
            'desc': '参数错误'
        }
    return jsonify(ret)

@admin_app.route(r'/user/save', methods=['POST'])
@admin_required
def user_save_ajax():
    user_data = request.values.get('user_data', None)
    ret = {}
    if bool(user_data):
        try:
            json_data = json.loads(user_data)
            if isinstance(json_data, dict):
                required_fields = ['name', 'email']
                if all(i in json_data for i in required_fields):
                    ok = False
                    error = -1
                    msg = '未知错误'
                    if 'id' in json_data:
                        user_id = int(json_data['id'])
                        if User.query.filter_by(id=user_id).count() > 0:
                            (ok, error) = update_user_info(user_id, json_data)
                            msg = '修改成功' if ok else error
                    else:
                        (ok, error) = add_new_user(json_data)
                        msg = '添加成功' if ok else error
                    ret = {
                        'error': error,
                        'desc': msg
                    }
                else:
                    ret = {
                        'error': 4,
                        'desc': '数据不完整'
                    }
            else:
                ret = {
                    'error': 3,
                    'desc': '数据无效'
                }
        except json.decoder.JSONDecodeError:
            ret = {
                'error': 21,
                'desc': '数据格式有误'
            }
        except Exception as ex:
            raise ex
            ret = {
                'error': 20,
                'desc': '数据内容或结构有误'
            }
    else:
        ret = {
            'error': 1,
            'desc': '缺少参数'
        }
    return jsonify(ret)

def update_user_info(user_id, user_data):
    user_obj = User.query.get(user_id)
    if 'name' in user_data:
        user_obj.name = user_data['name']
    if 'email' in user_data:
        # TODO: email格式校验
        user_obj.email = user_data['email']
    if 'password' in user_data and len(user_data['password']) > 0:
        user_obj.password = User.encrypt_string(user_data['password'])

    change_permission = False
    if 'is_admin' in user_data:
        change_permission = True
        user_obj.is_admin = True if user_data['is_admin'] in ['1', 'true'] else False
    if 'disable' in user_data:
        change_permission = True
        user_obj.disable = True if user_data['disable'] in ['1', 'true'] else False
    if change_permission and session['login_user']['id'] == user_id:
        db.session.rollback()
        return (False, '不能对自己进行权限操作')
    db.session.commit()
    return (True, None)

def add_new_user(user_data):
    user_obj = User()
    if 'name' in user_data:
        user_obj.name = user_data['name']
    if 'email' in user_data:
        # TODO: email格式校验
        user_obj.email = user_data['email']
    if 'password' in user_data:
        user_obj.password = User.encrypt_string(user_data['password'])
    if 'is_admin' in user_data:
        user_obj.is_admin = True if user_data['is_admin'] in ['1', 'true'] else False
    db.session.add(user_obj)
    db.session.commit()
    return (True, None)