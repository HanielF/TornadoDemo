import tornado.web
import os
from views import index
import config


# 应用
class Application(tornado.web.Application):
    def __init__(self):
        # 路由
        handlers = [
            (r'/', index.IndexHandler),
            (r'/index', index.IndexHandler),
            (r'/flower', index.FlowerHandler),
#            (r'/(.*)$', index.StaticFileHandler, {
#                "path": os.path.join(config.BASE_DIRS, "templates"),
#                "default_filename": "index.html"
#            }),
        ]

        # 添加配置
        super(Application, self).__init__(handlers, **config.settings)
        #  super(Application, self).__init__(handlers)
