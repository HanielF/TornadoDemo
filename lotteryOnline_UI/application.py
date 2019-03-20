import tornado.web
from views import index, lottery
import config
import os


# 应用
class Application(tornado.web.Application):
    def __init__(self):
        # 路由
        handlers = [
            (r'/', index.IndexHandler),
            (r'/lottery', lottery.LotteryHandler),
            #  (r'/(.*)$', tornado.web.StaticFileHandler, {
                #  "path": os.path.join(config.BASE_DIRS, "static/html"),
                #  "default_filename": "index.html"
            #  }),
        ]

        # 添加配置
        super(Application, self).__init__(handlers, **config.settings)
        #  super(Application, self).__init__(handlers)
