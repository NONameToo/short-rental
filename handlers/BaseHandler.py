# coding:utf-8

from tornado.web import RequestHandler
import json
import tornado.web

# 导入自己封装的session模块
from utils.Session import Session



class BaseHandler(RequestHandler):
    """handler的基类"""

    # 方便调用数据库

    @property
    def db(self):
        return self.application.db

    @property
    def redis(self):
        return self.application.redis


    def prepare(self):
        self.xsrf_token

        # 判断传过来的数据如果是json的话
        print(self.request.body)
        # self.json_args=self.request.body

        if self.request.headers.get('Content-Type', '').startswith('application/json'):
            print('内容是json格式')
            self.json_args = json.loads(self.request.body)
        else:
            self.json_args = None

    def write_error(self, status_code, **kwargs):
        pass

    def set_default_headers(self):
        pass

    def initialize(self):
        pass

    def on_finish(self):
        pass



    # 用户登陆验证

    def get_current_user(self):

        # 实例化session模块
        self.session = Session(self)
        return self.session.data




# 重写StaticFileHandler,使用户第一次访问就能开启xsrf

class StaticFileHandler(tornado.web.StaticFileHandler):
    def __init__(self, *args, **kwargs):
        super(StaticFileHandler, self).__init__(*args, **kwargs)
        self.xsrf_token




