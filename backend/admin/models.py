# -*- coding: utf-8 -*-
'''模型'''
from ..core.database import db
from ..utils import md5


class User(db.Model):
    '''后台操作人员(用户)'''
    __tablename__ = 'user'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    email = db.Column("email", db.String(64), index=True, unique=True) # 邮箱
    name = db.Column("name", db.String(64)) # 姓名
    password = db.Column("password", db.String(32)) # 密码
    is_admin = db.Column("is_admin", db.Boolean(create_constraint=False), default=0) # 是否是管理员
    disable = db.Column("disable", db.Boolean(create_constraint=False), default=0) # 是否禁用
    deleted = db.Column("deleted", db.Boolean(create_constraint=False), default=0) # 是否标记为删除

    def to_dict(self, with_pwd=True):
        ret = {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'is_admin': self.is_admin,
            'disable': self.disable,
            'deleted': self.deleted
        }
        if with_pwd:
            ret['password'] = self.password
        return ret

    @classmethod
    def encrypt_string(cls, raw_str, mix=''):
        '''加密算法(需要保密)'''
        ret = md5(raw_str)
        ret = md5(ret[::2]) + md5(ret[::3])
        ret = md5(ret) + md5(ret[::5])
        ret = ret[3:-3][5:] + mix
        ret = md5(ret)
        return ret

    @classmethod
    def verify_encrypt(cls, raw_str, encrypted_str, mix=''):
        '''
        验证明文和密文是否对应

        :param raw_str: 明文
        :param encrypted_str: 密文
        :param_str raw_str: str
        :param_str encrypted_str: str
        :return_type: bool
        '''
        return cls.encrypt_string(raw_str, mix=mix) == encrypted_str