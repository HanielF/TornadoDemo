import tornado.web
import tornado.ioloop
import tornado.httpserver

import config
from application import Application

if __name__ == "__main__":
    # 创建app
    app = Application()
    # 创建http服务器
    httpServer = tornado.httpserver.HTTPServer(app)
    # 绑定并开单进程
    httpServer.bind(config.options["port"])
    httpServer.start(1)
    # 别忘了主循环开启
    tornado.ioloop.IOLoop.current().start()
