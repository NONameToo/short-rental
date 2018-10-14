# coding:utf-8


# 导入处理装饰器改变函数名使之不改变模块

import functools

# 导入返回码
from utils.response_code import RET


# 登陆验证装饰器

def require_logined(fun):
    @functools.wraps(fun)
    def wrapper(request_handler_obj, *args, **kwargs):
        # 如果session中返回的data不是空字典，证明是登陆状态
        if request_handler_obj.get_current_user():
            fun(request_handler_obj, *args, **kwargs)
        else:
            # 如果是空字典证明没有登陆
            return request_handler_obj.write(dict(errno=RET.SESSIONERR, errmsg='用户未登陆'))

    return wrapper

