import tornado.web
from views import index
import config


# 应用
class Application(tornado.web.Application):
    def __init__(self):
        # 路由
        handlers = [
            (r'/', index.IndexHandler),
            (r'/write', index.WriteHandler),
            (r'/json1', index.JsonHandler),
            (r'/json2', index.Json2Handler),
            (r'/headers', index.HeaderHandler),
            (r'/status_code', index.StatusCodeHandler),
            (r'/index', index.RedirectHandler),
            (r'/iserror', index.ErrorHandler),
        ]

        # 添加配置
        super(Application, self).__init__(handlers, **config.settings)
        #  super(Application, self).__init__(handlers)
