import tornado.web
from tornado.web import RequestHandler


# 视图类
class UploadHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.write("http get")

    def post(self, *args, **kwargs):
        files = self.request.files['file']
        self.write(files[0]['body'])
