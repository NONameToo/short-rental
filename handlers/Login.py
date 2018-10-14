# coding:utf-8

from handlers.BaseHandler import BaseHandler

from utils.response_code import RET

from hashlib import sha1

import logging

# 导入封装的session
from utils.Session import Session

# 登陆处理类
class Login(BaseHandler):

    def post(self):
        # 提出出传过来的参数
        print(self.json_args)
        mobile = self.json_args['mobile']
        password = self.json_args['password']

        if not all((mobile, password)):
            return self.write(dict(errno=RET.PARAMERR, errmsg=u'参数错误'))

        # 对密码进行加密

        pwd = sha1(password).hexdigest()
        print('登陆密码加密后的结果：%s' % pwd)

        # 从数据库中查询
        try:
            password2 = self.db.get('select * from ih_user_profile where up_mobile=%s', mobile)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg=u'数据库查询错误'))
        # 如果没有查询到结果
        print(password2)
        if not password2:
            return self.write(dict(errno=RET.DATAERR, errmsg=u'用户名错误'))


        # 判断密码是否正确
        print("***************")
        print(pwd)
        print(password2)
        if pwd != password2['up_password']:
            return self.write(dict(errno=RET.DATAERR, errmsg=u'密码错误'))

        print('登陆成功')

        # 登陆成功，保存session
        try:
            self.session = Session(self)
            self.session.data['user_id'] = password2['up_user_id']
            self.session.data['name'] = password2['up_user_name']
            self.session.data['mobile'] = mobile
            self.session.save()

        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DATAERR, errmsg=u'存入session失败'))



        self.write(dict(errno=RET.OK, errmsg=u'登陆成功'))




# 检查登陆状态

class CheckLogin(BaseHandler):
    """检查登陆状态"""
    def get(self):
        if self.get_current_user():
            # 函数返回的是self.data,通过判断是否为空来确定session是否有值
            print('-----------------------')
            user_id = self.session.data['user_id']

            # 根据user_id查询用户名
            try:
                user_name = self.db.get('select up_user_name from ih_user_profile where up_user_id=%s' % user_id)['up_user_name']
                print('查询到的用户名是:%s' % user_name)

            except Exception as e:
                logging.error(e)
                return self.write(dict(errno=RET.DBERR, errmsg='查询数据库失败'))

            self.write(dict(errno='0', errmsg='True', data=dict(user_name=user_name)))
        else:
            self.write(dict(errno='1', errmsg='False'))










