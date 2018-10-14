# coding:utf-8


# 导入提取出去的handlers
from handlers import passport, VerifyCode, Register, Login,Profile,Logout

# 导入静态页面处理类
from handlers.BaseHandler import StaticFileHandler
import os

handlers = [
    (r'/api/imagecode', VerifyCode.ImageCode),
    (r'/api/msgcode', VerifyCode.MSGcode),
    (r'/api/register', Register.Register),
    (r'/api/login', Login.Login),
    (r'/api/logout', Logout.Logout),
    (r'/api/check_login', Login.CheckLogin),
    (r'/api/profile', Profile.Profile),
    (r'/api/profile/avatar', Profile.Avatar),
    (r'/api/profile/name', Profile.Name),
    (r'/api/profile/auth', Profile.Auth),
    (r'/(.*)', StaticFileHandler, dict(path=os.path.join(os.path.dirname(__file__), 'html'), default_filename='index.html'))


]