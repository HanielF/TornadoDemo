import tornado.web
import os
from views import index
import config


# 应用
class Application(tornado.web.Application):
    def __init__(self):
        # 路由
        handlers = [
            (r'/', index.LoginHandler),
            (r'/index', index.IndexHandler),
            (r'/login(.*)$', index.IndexHandler),
            (r'/home', index.HomeHandler),
            (r'/chat', index.ChatHandler),
            (r'/allrom', index.AllromHandler),
            (r'/(.*)$', index.StaticFileHandler, {
                "path": os.path.join(config.BASE_DIRS, "templates"),
                "default_filename": "login.html"
            }),
        ]

        # 添加配置
        super(Application, self).__init__(handlers, **config.settings)
        #  super(Application, self).__init__(handlers)
