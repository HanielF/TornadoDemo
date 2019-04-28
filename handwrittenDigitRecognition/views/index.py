import tornado.web
from tornado.websocket import WebSocketHandler
from tornado.web import RequestHandler
import os
import json
import uuid
import datetime
import time
import imageHandler



# 视图类
class IndexHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render("index.html")


# 在新的websocket连接之后执行open函数
class PreNumHandler(WebSocketHandler, RequestHandler):
    # 连接时的函数
    def open(self):
        print("ws opened")


    # 当websocket连接关闭后调用，客户端主动的关闭
    def on_close(self):
        print("ws closed")


    #  当客户端发送消息过来时调用
    def on_message(self, message):
        msg = json.loads(message)
        msgData = list(msg["number"].values())
        resNum = imageHandler.imageRecognize(msgData)
        print(resNum)
        self.write_message(json.dumps({
            'result':str(resNum)
        }))


    # 判断请求源 对于符合条件的请求源允许连接
    def check_origin(self, origin):
        return True


