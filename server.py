# coding:utf-8

import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop

from tornado.options import options,define
from tornado.web import RequestHandler
import os

# 导入提取出去的路由列表
from urls import handlers

# 导入提取出去的Application配置
import config

# 导入mysql数据库支持
import torndb

# 导入redis数据库支持
import redis



define('port', type=int, default=8000, help='服务器端口')


class Application(tornado.web.Application):

    def __init__(self, *args, **kwargs):
        super(Application, self).__init__(*args, **kwargs)
        # self.db = torndb.Connection(
        #     host=config.db_options["host"],
        #     database=config.db_options["database"],
        #     user=config.db_options["user"],
        #     password=config.db_options["password"],
        # )
        #
        # self.redis = redis.StrictRedis(
        #     host=config.redis_options["host"],
        #     port=config.redis_options["port"],
        #
        # )

        # 使用解包的方式更简单
        self.db = torndb.Connection(**config.db_options)
        self.redis = redis.StrictRedis(**config.redis_options)







def main():
    # 设置日志
    options.logging = config.log_level
    options.log_file_prefix = config.log_file

    # 解析命令行
    tornado.options.parse_command_line()

    app = Application(
        handlers, **config.settings
    )


    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    # http_server.bind(options.port)
    # http_server.start(0)
    tornado.ioloop.IOLoop.current().start()





if __name__ == '__main__':
    main()