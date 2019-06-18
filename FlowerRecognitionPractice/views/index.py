import tornado.web
from tornado.websocket import WebSocketHandler
from tornado.web import RequestHandler
import os
import json
import imagesProcess
import base64
import recognizeImg


# 视图类
class IndexHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render("index.html")


# 在新的websocket连接之后执行open函数
class FlowerHandler(WebSocketHandler, RequestHandler):
    def post(self, *args, **kwargs):
        print("Flower recognition: post function")

    # 连接时的函数
    def open(self):
        print("Flower recognition: ws opened")

    # 当websocket连接关闭后调用，客户端主动的关闭
    def on_close(self):
        print("Flower recognition: ws closed")

    #  当客户端发送消息过来时调用
    def on_message(self, message):
        print("Flower recognition: on message")
        msg = json.loads(message)
        # 这里删掉前面的23个字符，是因为传过来的base64码前面有"data:image/jpeg;base64,"要把这部分去掉才可以显示
        decodeData = base64.b64decode(msg["imgBase64"][22:])
        # 将图片写入本地
        fout = open("tmp.jpg", 'wb')
        fout.write(decodeData)
        fout.close()
        recognizeImg.imgPreTreatment("./tmp.jpg")
        flowerName = recognizeImg.flowerRecognization("./tmp.jpg")
        self.write_message(json.dumps({
            'flowerName':str(flowerName)
        }))

    # 判断请求源 对于符合条件的请求源允许连接
    def check_origin(self, origin):
        return True


