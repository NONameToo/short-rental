# coding:utf-8

import tornado.web

# 导入生成全局唯一id模块
import uuid
import logging
import json
from config import SESSION_EXPIRES_SECONDES


class Session(object):
    """session处理类"""
    # 把请求传给session作为参数
    def __init__(self, request_handler):
        self.request_handler = request_handler
        self.session_id = self.request_handler.get_secure_cookie('session_id')

        # 如果没有取到证明是第一次访问
        if not self.session_id:
            # 就给用户生成一个
            self.session_id = uuid.uuid4().get_hex()
            print('给用户生成的session:%s' % self.session_id)
            self.data = {}

        else:
            # 如果有，进行比对
            try:

                # 从redis中获取session对应的值
                data = self.request_handler.redis.get('sess_%s' % self.session_id)

            except Exception as e:
                logging.error(e)
                self.data = {}

            if not data:
                self.data = {}

            # 如果取到了数据
            else:
                self.data = json.loads(data)
                print('--------------------session的数据-----------------')
                print(self.data)
    # 保存session
    def save(self):
        json_data = json.dumps(self.data)
        try:
            self.request_handler.redis.setex('sess_%s' % self.session_id, SESSION_EXPIRES_SECONDES, json_data)

        except Exception as e:
            logging.error(e)
            raise Exception(u'保存session出错')
        # 设置安全cookie
        else:
            self.request_handler.set_secure_cookie('session_id', self.session_id)


    # 删除session

    def clear(self):
        try:
            self.request_handler.redis.delete('sess_%s' % self.session_id)

        except Exception as e:
            logging.error(e)



















