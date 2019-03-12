import tornado.web
from tornado.web import RequestHandler


class CanvasHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render("canvas.html")
