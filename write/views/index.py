from tornado.web import RequestHandler
import json


# 视图类
class IndexHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.write("Hello World")


class WriteHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.write("haniel is a good man")
        self.write("haniel is a nice man")
        self.write("haniel is a handsome man")
        # 刷新缓冲区,关闭当此请求通道
        # 在finish下边不要再write
        self.finish()


#  手动转成Json字符串
#  返回response类型为text/html,可以手动设置响应头
class JsonHandler(RequestHandler):
    def get(self, *args, **kwargs):
        per = {"name": "json1", "age": 20, "height": 175, "weight": 61}
        jsonStr = json.dumps(per)
        #  手动设置响应头
        self.set_header("Content-Type", "application/json;charset=UTF-8")
        self.set_header("haniel", "good")
        self.write(jsonStr)


# 推荐使用，直接返回字典,write自动转为json
# 返回response类型为json类型
class Json2Handler(RequestHandler):
    def get(self, *args, **kwargs):
        per = {"name": "json2", "age": 20, "height": 175, "weight": 61}
        self.write(per)


#  使用设置默认响应头，不用在函数里面写,就像JsonHandler一样
class HeaderHandler(RequestHandler):
    def set_default_headers(self):
        self.set_headers("Content-Type", "text/html; charset=UTF-8")
        self.set_header("hanielf", "nice")

    def get(self, *args, **kwargs):
        pass


class StatusCodeHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.set_status(404, "test")


class RedirectHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.write("重定向")


class ErrorHandler(RequestHandler):
    def write_error(self, status_code, **kwargs):
        if status_code == 500:
            self.write("服务器内部错误", bytes, dict)
        elif status_code == 404:
            self.write("资源不存在", bytes, dict)
        else:
            self.write("我也不知道啥错误", bytes, dict)

    def get(self, *args, **kwargs):
        flag = self.get_query_argument("flag")
        if flag == 0:
            self.send_error(500)
        self.write("you are right")
