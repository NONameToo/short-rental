# coding:utf-8

from handlers.BaseHandler import BaseHandler

class IndexHandler(BaseHandler):
    def get(self):
        # self.write(u'付绍凯大帅哥')
        self.render('index.html')

