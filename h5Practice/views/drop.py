import tornado.web
from tornado.web import RequestHandler


class DropHandler(RequestHandler):
    def post(self, *args, **kwargs):
        self.render('drop.html')

    def get(self, *args, **kwargs):
        self.render('drop.html')
