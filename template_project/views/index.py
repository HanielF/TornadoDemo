import tornado.web
from tornado.web import RequestHandler


# 视图类
class IndexHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.write("Hello World")
