import tornado.web
from views import index
import config


# 应用, bytes, dict)<`2:#:, bytes`><`3:#:, dict]`>)<`4`>

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', index.IndexHandler),
            (r'/students1', index.StudentsHandler),
            (r'/students2', index.Students2Handler),
            (r'/students3', index.Students3Handler),
            (r'/HomeHandler', index.HomeHandler),
        ]

        # 添加配置
        super(Application, self).__init__(handlers, **config.settings)
        #  super(Application, self).__init__(handlers)
