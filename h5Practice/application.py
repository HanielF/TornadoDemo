import tornado.web
from views import index, drop, canvas, upload
import config


# 应用
class Application(tornado.web.Application):
    def __init__(self):
        # 路由
        handlers = [
            (r'/', index.IndexHandler),
            #  (r'/canvas.html', canvas.CanvasHandler),
            (r'/drop', drop.DropHandler),
            (r'/canvas', canvas.CanvasHandler),
            (r'/upload', upload.UploadHandler),
        ]

        # 添加配置
        super(Application, self).__init__(handlers, **config.settings)
        #  super(Application, self).__init__(handlers)
