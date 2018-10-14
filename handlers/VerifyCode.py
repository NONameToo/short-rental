# coding:utf-8

from handlers.BaseHandler import BaseHandler
import logging

# 导入设置的常量
from constants import *

# 导入生成图片验证码模块
from utils.captcha import captcha

# 导入异步客户端
from tornado.httpclient import AsyncHTTPClient
import tornado.gen

# 导入设置的状态码
from utils.response_code import RET

# 导入发送短信模块
from libs.yuntongxun.SendTemplateSMS import CCP
import random
import re



class ImageCode(BaseHandler):
    """"图片验证码接口"""
    def get(self):

        codeid = self.get_argument('codeid')
        print('pcodeid的值是：%s'%codeid)
        pcodeid = self.get_argument('pcodeid')

        if pcodeid:
            try:
                self.redis.delete('')
            except Exception as e:
                self.logging.error(e)

        # name图片验证码的名字
        # text图片验证码的内容
        # image图片验证码的二进制数据

        name, text, image = captcha.captcha.generate_captcha()

        # 把验证码的值存到redis数据库
        try:
            # redis.setex可以设置过期时间
            self.redis.setex('image_code_%s' % codeid, IMAGE_CODE_SPIRES_SECONDS, text)
        except Exception as e:
            logging.error(e)
            return self.write("")

        # 返回验证码图片的二进制数据
        self.write(image)


# 发送短信验证码
class MSGcode(BaseHandler):
    """短信验证码接口"""
    @tornado.gen.coroutine
    def post(self):
        # 获取传过来的参数
        mobile = self.json_args.get('mobile')
        image_code_id = self.json_args.get('image_code_id')
        image_code_text = self.json_args.get('image_code_text')
        print(mobile)
        print(image_code_id)
        print(image_code_text)


        # 判断三个参数是否都传了
        if not all((mobile, image_code_id, image_code_text)):
            return self.write(dict(errno=RET.PARAMERR, errmsg=u'参数错误'))

        if not re.match(r'1\d{10}', mobile):
            print(re.match(r'1\d{10}', mobile))
            return self.write(dict(errno=RET.PARAMERR, errmsg=u'无效的手机号码'))





        # 判断验证码是否正确
        try:
            # 根据验证码的id找到验证码对应的值
            print(image_code_id)
            image_content = self.redis.get('image_code_%s' % image_code_id)
            print('image_code_%s' % image_code_id)
            print(image_content)

        except Exception as e:
            return self.write(dict(errno=RET.DBERR, errmsg=u'数据库查询错误'))

        if image_content is None:
            return self.write(dict(errno=RET.NODATA, errmsg=u'验证码已经过期'))


        if image_code_text.lower() != image_content.lower():
            return self.write(dict(errno=RET.DATAERR, errmsg=u'验证码错误'))


        # 生成随机验证码
        msg_code = "%4d" % random.randint(0, 9999)
        print('短信验证码是：%s' % msg_code)

        # 把验证码存到数据库
        try:
            self.redis.setex('msg_code_%s' % mobile, MSG_CODE_SPIRES_SECONDS, msg_code)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DBERR, errmsg=u'生成验证码出错'))

        # 发送短信
        try:
            cpp = CCP.instance()
            cpp.sendTemplateSMS(mobile, [msg_code, MSG_CODE_SPIRES_SECONDS], 1)

        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.THIRDERR, errmsg=u'第三方出错,发送失败'))

        self.write(dict(errno=RET.OK, errmsg=u'短信发送成功！'))
































