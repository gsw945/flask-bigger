function send_request(url, action, total, left, origin_text, $btn) {
    var _id = left.shift();
    $.ajax({
        url: url,
        data: {
            action: action,
            id: _id
        },
        dataType: 'json',
        type: 'POST',
        success: function(data) {
            var new_text = '进度: ' + (total - left.length) + '/' + total;
            $btn.attr('value', new_text);
            if(data.error != 0) {
                if(!confirm('Error: ' + data.desc + '\n是否跳过，继续操作?')) {
                    $btn.attr('value', origin_text);
                    return;
                }
            }
            if(left.length > 0) {
                send_request(url, action, total, left, origin_text, $btn);
            }
            else {
                $btn.attr('value', origin_text);
                setTimeout(function() {
                    $('#tb-users').bootstrapTable('refresh', {silent: false});
                }, 50);
            }
        }
    })
}

function delete_or_disable($self, msg, action) {
    if(confirm(msg)) {
        var origin_text = $self.attr('value');
        var ids = get_selected_ids();
        var new_text = '进度: 0/' + ids.length;
        $self.attr('value', new_text);
        send_request(USER_DELETE_DISABLE_URL, action, ids.length, ids, origin_text, $self);
    }
}

function get_selected_ids() {
    var $tb_obj = $('#tb-users');
    var selection = $tb_obj.bootstrapTable('getSelections');
    var ids = [];
    for (var i = 0; i < selection.length; i++) {
        ids.push(selection[i].id);
    }
    return ids;
}

/**
 * 按钮事件绑定
 */
function bind_click4btns() {
    var $btn_add = $('#btn-add'),
        $btn_disable = $('#btn-disable'),
        $btn_delete = $('#btn-delete');
    $btn_add.on('click', function() {
        popup_user('添加用户');
    });
    $btn_disable.on('click', function() {
        delete_or_disable($btn_disable, '确定禁用所选的用户吗？', 'disable');
    });
    $btn_delete.on('click', function() {
        delete_or_disable($btn_delete, '确定删除所选的用户吗？', 'delete');
    });
}

/**
 * 改变按钮状态
 * @param  {jQuery对象} $tb_obj 表格对象
 */
function change_enable($tb_obj) {
    var $btn_disable = $('#btn-disable'),
        $btn_delete = $('#btn-delete');
    var selection = $tb_obj.bootstrapTable('getSelections');
    if(selection.length > 0) {
        $btn_disable.removeAttr('disabled').prop('disabled', false);
        $btn_delete.removeAttr('disabled').prop('disabled', false);
    }
    else {
        $btn_disable.attr('disabled', 'disabled').prop('disabled', true);
        $btn_delete.attr('disabled', 'disabled').prop('disabled', true);
    }
}

function build_is_admin(is_admin_val) {
    return [
        '<label>',
            '<input type="radio" name="rdo-is-admin" value="1" ', (is_admin_val == '1' ? 'checked="checked"' : ''), ' />是',
        '</label>',
        '&nbsp;&nbsp;',
        '<label>',
            '<input type="radio" name="rdo-is-admin" value="0" ', (is_admin_val == '0' ? 'checked="checked"' : ''), ' />否',
        '</label>',
    ].join('');
}

function build_is_disable(is_disable_val) {
    return [
        '<label>',
            '<input type="radio" name="rdo-is-disable" value="1" ', (is_disable_val == '1' ? 'checked="checked"' : ''), ' />是',
        '</label>',
        '&nbsp;&nbsp;',
        '<label>',
            '<input type="radio" name="rdo-is-disable" value="0" ', (is_disable_val == '0' ? 'checked="checked"' : ''), ' />否',
        '</label>',
    ].join('');
}

/**
 * 弹出用户信息编辑对话框
 * @param  {String} box_title 对话框标题
 * @param  {Object} user_item 用户信息
 */
function popup_user(box_title, user_item) {
    var is_new = false;
    if(!user_item) {
        is_new = true;
        user_item = {
            name: '',
            is_admin: 0,
            email: '',
            advertising: '',
            is_hot: 0,
            pic_url_0: '',
            pic_url_1: '',
            pic_url_2: '',
            pic_url_3: ''
        };
    }
    // console.log(user_item);
    var htmls = [
        '<div class="box-form-wrapper">'
    ];
    if(!is_new) {
        htmls.push(build_line(
            'ID',
            '<span>' + user_item.id + '</span>'
        ));
    }
    htmls.push(build_line(
        '姓名',
        '<input type="text" name="txt-name" value="' + user_item.name + '" placeholder="姓名" />'
    ));
    htmls.push(build_line(
        '邮箱',
        '<input type="text" name="txt-email" value="' + user_item.email + '" placeholder="邮箱" />'
    ));
    htmls.push(build_line(
        '密码',
        '<input type="text" name="txt-password" value="" placeholder="' + (is_new ? '密码' : '不修改请留空') + '" />'
    ));
    htmls.push(build_line(
        '管理员',
        build_is_admin(user_item.is_admin)
    ));
    if(!is_new) {
        htmls.push(build_line(
            '禁用',
            build_is_disable(user_item.disable)
        ));
    }
    htmls.push('</div>');
    htmls.push([
        '<div class="popup-tip-msg">',
            '注意: 操作完成后，请手动点击 [提交] 按钮',
        '</div>'
    ].join(''));
    // http://bootboxjs.com/documentation.html
    bootbox.setLocale('zh_CN');
    var dialog = bootbox.dialog({
        title: box_title,
        message: htmls.join(''),
        show: true,
        backdrop: undefined,
        closeButton: true,
        onEscape: false,
        // size: 'large',
        className: "my-modal",
        buttons: {
            submit: {
                label: '提交',
                className: 'btn-primary',
                callback: function() {
                    console.log(user_item);
                    var _data = collect_submit_info(dialog, user_item);
                    if(!!_data) {
                        submit_user_request(_data);
                        return true;
                    }
                    console.log(_data)
                    return false;
                }
            },
            close: {
                label: '取消',
                className: 'btn-primary',
                callback: function() {
                    return true;
                }
            }
        },
        callback: function(result) {
            return true;
        }
    });
}

function get_user_by_id(d_id) {
    var ret = null;
    var dl = $('#tb-users').data('bootstrap.table').data;
    for (var i = 0; i < dl.length; i++) {
        if(dl[i].id == d_id) {
            ret = dl[i];
            break;
        }
    }
    return ret;
}

function user_detail(user_id) {
    if(user_id) {
        var user_item = get_user_by_id(user_id);
        popup_user('用户详情', user_item);
    }
}

/**
 * 提交用户信息
 * @param  {Object} user_data 用户信息
 */
function submit_user_request(user_data) {
    $.ajax({
        url: USER_SAVE_AJAX,
        type: 'POST',
        data: {
            user_data: JSON.stringify(user_data)
        },
        dataType: 'json'
    }).done(function(data) {
        console.log(data);
        if(data.error == 0) {
            $('#tb-users').bootstrapTable('refresh');
        }
        else {
            alert(data.desc);
        }
    }).fail(function(e) {
        console.error(e);
        alert(e.responseText)
    });
}

function collect_submit_info($dialog, user_item) {
    var $form = $dialog.find('.bootbox-body .box-form-wrapper');
    var is_new = true;
    var _ret = {};
    if(!!user_item.id) {
        is_new = false;
        _ret['id'] = user_item.id;
    }
    var _name = $form.find('input[name="txt-name"]').val();
    if(!_name || _name.length < 1) {
        alert('[姓名]必填');
        return null;
    }
    _ret['name'] = _name;
    var _email = $form.find('input[name="txt-email"]').val();
    if(!_email || _email.length < 1) {
        alert('[邮箱]必填');
        return null;
    }
    _ret['email'] = _email;
    var _is_admin = $form.find('input[name="rdo-is-admin"]:checked').val();
    _ret['is_admin'] = _is_admin;
    if(!is_new) {
        var _disable = $form.find('input[name="rdo-is-disable"]:checked').val();
        _ret['disable'] = _disable;
    }
    var _password = $form.find('input[name="txt-password"]').val();
    if(_password && _password.length > 0) {
        _ret['password'] = _password;
    }

    return _ret;
}