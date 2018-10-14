# coding:utf-8

from handlers.BaseHandler import BaseHandler
from utils.response_code import RET
import logging
from hashlib import sha1

# 导入封装的Session
from utils.Session import Session


class Register(BaseHandler):
    """注册处理类"""
    def post(self):
        # 解析提交过来的数据
        print(self.json_args)
        mobile = self.json_args.get('mobile')
        imagecode = self.json_args.get('imagecode')
        phonecode =self.json_args.get('phonecode')
        password = self.json_args.get('password')
        password2= self.json_args.get('password2')

        if not all((mobile, imagecode, phonecode, password, password2)):
            return self.write(dict(errno=RET.PARAMERR, errmsg=u'参数错误'))

        try:

            # 从redis数据库中取出短信验证码
            msg_code = self.redis.get('msg_code_%s' % mobile)
            print(msg_code)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg=u'数据库查询错误'))

        if not msg_code:
            return self.write(dict(errno=RET.NODATA, errmsg=u'短信验证码已经过期'))

        if msg_code != phonecode:
            return self.write(dict(errno=RET.DATAERR, errmsg=u'短信验证码错误'))

        if password != password2:
            return self.write(dict(errno=RET.DATAERR, errmsg=u'两次密码不一致'))
        # 查询用户是否已经存在
        if self.db.get("select * from ih_user_profile where up_mobile=%s", mobile):

            return self.write(dict(errno=RET.DATAEXIST, errmsg=u'用户已经存在'))

        try:
            # 对密码进行加密
            pwd = sha1(password).hexdigest()
            print('加密后的密码：%s' % pwd)


            # 把用户存到数据库,并返回自增id
            num = self.db.execute("insert into ih_user_profile(up_user_name,up_mobile, up_password) values(%s,%s,%s)",  "用户:%s"%mobile, mobile, pwd)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg=u'数据库写入错误'))
        print('用户注册成功')
        # 注册成功,存储session
        try:

            self.session = Session(self)
            self.session.data['user_id'] = num
            self.session.data['name'] = mobile
            self.session.data['mobile'] = mobile
            self.session.save()
        except Exception as e:
            logging.error(e)


        self.write(dict(errno=RET.OK, errmsg=u'注册成功'))

