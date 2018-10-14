# coding:utf-8


from handlers.BaseHandler import BaseHandler
import logging
from utils.response_code import RET

# 导入常量
from constants import *

import json

# 导入登陆验证
from common import require_logined

# 导入腾讯云
from libs.tencent import image_storage

from constants import START_FILE_NAME





class Profile(BaseHandler):
    """用户个人中心"""
    @require_logined
    def get(self):

        # 这里面只负责个人中心的逻辑，判断用户是否登陆的状态由装饰器去做

        # 取出user_id

        user_id = self.session.data['user_id']

        try:
            # 查询用户的个人信息
            profile = self.db.get('select * from ih_user_profile where up_user_id=%s', user_id)
            print(profile)

        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg=u'数据库查询错误'))

        # 如果保存有头像信息，就把头像的url和存储的地址的前缀拼接起来
        if profile['up_avatar']:
            avatar_url = profile['up_avatar']

        else:
            avatar_url = None


        data = {
            'errno': RET.OK,
            'errmsg': '获取个人信息成功',
            'data': {
                'user_id': user_id,
                'name': profile['up_user_name'],
                'mobile': profile['up_mobile'],
                'avatar': avatar_url
            }
        }
        json_data = json.dumps(data)
        print(json_data)
        self.write(json_data)


class Avatar(BaseHandler):
    """头像上传"""
    @require_logined
    def post(self):
        # 提取出上传过来的图片数据
        image_name = self.request.files['avatar'][0]['filename']
        print(image_name)
        image_data = self.request.files['avatar'][0]['body']
        if not image_data:
            return self.write(dict(errno=RET.NODATA, errmsg='参数错误'))

        try:
            file_name = image_storage(image_name, image_data)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno='1', errmsg='保存头像失败'))

        print('%s存入成功' % file_name)


        avatar_url = START_FILE_NAME + file_name
        print('完整url路径:%s' % avatar_url)


        # 把用户的头像存入数据库
        print('---------------把头像地址存到数据库----------------------')
        user_id = self.session.data['user_id']
        self.db.execute('update ih_user_profile set up_avatar=%s where up_user_id=%s', avatar_url, user_id)

        # 向前段返回新头像的url地址
        resp_data = dict(errno=RET.OK, errmsg='保存头像成功', data=dict(avatar=avatar_url))
        json_data = json.dumps(resp_data)
        print(json_data)

        self.write(json_data)



class Name(BaseHandler):
    """更新用户名"""
    @require_logined
    def post(self):
        print('----------------更改用户名-----------------')
        name = self.json_args['name']
        print('新的用户名:%s' % name)

        user_id = self.session.data['user_id']
        # 查询数据库中此用户名是否已经存在
        result = self.db.get('select * from ih_user_profile where up_user_name=%s', name)
        print('在数据库中查询的用户名结果是:%s' % result)
        if result:
            # 如果两个名字相同,且是同一个人的
            if result['up_user_name'] == name and result['up_user_id'] == user_id:
                return self.write(dict(errno=RET.OK, errmsg='OK'))

            return self.write(dict(errno=RET.DATAEXIST, errmsg='用户名已经存在'))

        # 在数据库中更改用户名

        try:
            self.db.execute('update ih_user_profile set up_user_name=%s where up_user_id=%s', name, user_id)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg='保存用户名失败'))

        self.write(dict(errno=RET.OK, errmsg='OK'))



# 实名认证

class Auth(BaseHandler):
    """用户实名认证"""
    @require_logined
    def get(self):
        # 从数据库中查询用户的实名信息
        user_id = self.session.data['user_id']
        result = self.db.get('select up_real_name, up_id_card from ih_user_profile where up_user_id=%s', user_id)
        print('真实姓名:%s' % result['up_real_name'])
        print('真实身份证:%s' % result['up_id_card'])
        up_real_name, up_id_card = result['up_real_name'],result['up_id_card']


        # 如果没有值的话就证明没有进行过实名认证
        if not all((up_real_name, up_id_card)):
            return self.write(dict(errno='0', errmsg='尚未进行实名认证'))
        else:
            return self.write(dict(errno='1', errmsg='已经进行过实名认证', data=dict(real_name=up_real_name, id_card=up_id_card)))

    @require_logined
    def post(self):

        # 从数据库中查询用户的实名信息
        user_id = self.session.data['user_id']
        result = self.db.get('select up_real_name, up_id_card from ih_user_profile where up_user_id=%s', user_id)
        print('真实姓名:%s' %result['up_real_name'])
        print('真实身份证:%s' % result['up_id_card'])
        up_real_name, up_id_card = result['up_real_name'],result['up_id_card']

        if not all((up_real_name, up_id_card)):
            try:
                # 把用户提交的实名信息进行保存
                print('传过来的数据是:%s'%self.json_args)

                real_name = self.json_args.get('real_name')
                id_card = self.json_args.get('id_card')

                self.db.execute('update ih_user_profile set up_real_name=%s, up_id_card=%s where up_user_id=%s', real_name, id_card, user_id)
            except Exception as e:
                logging.error(e)
                return self.write(dict(errno=RET.DBERR, errmsg='保存实名信息失败'))

        return self.write(dict(errno='1', errmsg='已经进行过实名认证', data=dict(real_name=up_real_name, id_card=up_id_card)))



