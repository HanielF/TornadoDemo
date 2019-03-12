import tornado.web
from views import index, poem
import config


# 应用
class Application(tornado.web.Application):
    def __init__(self):
        # 路由
        handlers = [
            (r'/', index.IndexHandler),
            (r'/poem', poem.PoemHandler),
        ]

        # 添加配置
        super(Application, self).__init__(handlers, **config.settings)
        #  super(Application, self).__init__(handlers)
