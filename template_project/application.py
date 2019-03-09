import tornado.web
from views import index
import config


# 应用
class Application(tornado.web.Application):
    def __init__(self):
        # 路由
        handlers = [
            (r'/', index.IndexHandler)
        ]

        # 添加配置
        # super(Application, self).__init__(handlers, **config.settings)
        super(Application, self).__init__(handlers)
