import tornado.web
import json
from tornado.web import RequestHandler
from tornado.httpclient import AsyncHTTPClient
import time


# 视图类
class IndexHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.write("Hello World")


class StudentsHandler(RequestHandler):
    def on_response(self, response):
        if response.error:
            self.send_error(500)
        else:
            data = json.loads(response.body)
            # 这里本身无法write,要打开通道，用asynchronous装饰器
            self.write(data)
        self.finish()

    # 不关闭通信的通道
    #  @tornado.web.asynchronous
    # 实操发现用不了这个装饰器
    def get(self, *args, **kwargs):
        url = "http://s.budejie.com/v2/topic/list/10/0-0/budejie-android-8.0.1/0-25.json?uid=&t=&market=360zhushou&client=android&appname=budejie&device=&jdk=1&ver=8.0.1&udid=&from=android"
        # 创建客户端
        client = AsyncHTTPClient()
        # on_response是回调函数,如果请求成功，就进行on_response回调函数
        client.fetch(url, self.on_response)
        #  self.write("OK")


class Students2Handler(RequestHandler):
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        url = "http://s.budejie.com/v2/topic/list/10/0-0/budejie-android-8.0.1/0-25.json?uid=&t=&market=360zhushou&client=android&appname=budejie&device=&jdk=1&ver=8.0.1&udid=&from=android"
        client = AsyncHTTPClient()
        # 耗时操作
        res = yield client.fetch(url)
        if res.error:
            self.send_error(500)
        else:
            data = json.loads(res.body)
            self.write(data)


class Students3Handler(RequestHandler):
    # 简化get函数
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        res = yield self.getData()
        self.write(res)

    # 这里也要加装饰器，这里也是耗时操作
    @tornado.gen.coroutine
    def getData(self):
        url = "http://s.budejie.com/v2/topic/list/10/0-0/budejie-android-8.0.1/0-25.json?uid=&t=&market=360zhushou&client=android&appname=budejie&device=&jdk=1&ver=8.0.1&udid=&from=android"
        client = AsyncHTTPClient()
        # 耗时操作
        res = yield client.fetch(url)
        if res.error:
            #  表示没有结果
            ret = {"ret": 0}
        else:
            ret = json.loads(res.body)
        #  相当于gen.send()函数
        raise tornado.gen.Return(ret)


class HomeHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.write("Home")
