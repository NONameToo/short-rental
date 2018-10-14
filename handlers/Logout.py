# coding:utf-8


from handlers.BaseHandler import BaseHandler

from common import require_logined
from utils.response_code import RET

class Logout(BaseHandler):
    """退出登陆"""
    @require_logined
    def get(self):
        # 删除用户的session信息
        if self.get_current_user():
            self.session.clear()
            self.write(dict(errno=RET.OK, errmsg='退出成功'))







