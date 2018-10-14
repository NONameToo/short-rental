# coding:utf-8
import os


# Application中的参数
settings = {
    "template_path": os.path.join(os.path.dirname(__file__), "template"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "fGDQ+XSMQZOdiT3nmoe7SeL8/xABZEuVkpGx1bR1ejc=",
    "xsrf_cookies": True,
    "debug": True,
}

# 数据库的参数

#Mydql数据库
db_options = dict(
    host='127.0.0.1',
    database='ihome',
    user='root',
    password='fushaokai',

)

# redis数据库
redis_options = dict(
    host='127.0.0.1',
    port=6379,

)

log_file = os.path.join(os.path.dirname(__file__), 'logs/log.txt')
log_level = 'debug'


# session的有效期,单位：秒
SESSION_EXPIRES_SECONDES = 86400
