import tornado.web
from tornado.websocket import WebSocketHandler
from tornado.web import RequestHandler
import os
import json
import uuid
import datetime


# 视图类
class BaseHandler(RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.set_secure_cookie("user", self.get_argument("userName"))
        self.render(
            "index.html",
            username=self.get_argument("userName"),
            userId=self.get_argument("passWord"))


class AllromHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render("allrom.html")


class StaticFileHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render("login.html")


class HomeHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.render("home.html")


class LoginHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render('login.html')

    #  def post(self, *args, **kwargs):
    #  self.set_secure_cookie("user", self.get_argument("userName"))
    #  self.set_secure_cookie("passWord", self.get_argument("passWord"))
    #  self.redirect("/index")


class LogoutHandler(BaseHandler):
    def get(self):
        if (self.get_argument("logout", None)):
            self.clear_cookie("user")
            self.redirect("/")


#  ====================================================================


# 在新的websocket连接之后执行open函数
class ChatHandler(WebSocketHandler, BaseHandler):
    users = set()  # 用于存储在线用户id
    cache = []  # 聊天记录

    #  这个方法向客户端发送message消息，message可以使字符串或者字典(自动转为json字符串)如果binary参数为false,则message会以utf-8的编码发送,如果为true,可以发送二进制模式字节码
    def open(self):
        self.write_message(
            json.dumps({
                'type': 'sys',
                'username': 'SYSTEM',
                'message': u'Welcome to the Room',
            }))
        ChatHandler.push_cache(self)

    #  更新cache
    @classmethod
    def update_cache(cls, msg):
        cls.cache.append(msg)

    # 缓存的消息进行推送
    @classmethod
    def push_cache(cls, sock):
        for i in range(len(cls.cache)):
            sock.write_message(cls.cache[i])

    #  对在线的人进行推送
    @classmethod
    def send_updates(cls, msgtype, uname, msg):
        for sock in ChatHandler.users:
            sock.write_message(
                json.dumps({
                    'type': msgtype,
                    'username': uname,
                    'message': msg,
                }))

    # 当websocket连接关闭后调用，客户端主动的关闭
    def on_close(self):
        ChatHandler.users.remove(self)
        ChatHandler.send_updates('sys', 'SYSTEM',
                                 'User ' + self.username + ' has left!')

    def reg(self, username, uid):
        self.username = username
        self.userId = uid
        ChatHandler.send_updates('sys', 'SYSTEM',
                                 'User ' + self.username + ' has joined!')
        if self not in ChatHandler.users:
            ChatHandler.users.add(self)

    #  当客户端发送消息过来时调用
    def on_message(self, message):
        msg = json.loads(message)
        ChatHandler.update_cache(message)
        if msg["type"] == "reg":
            self.reg(msg["username"], msg["userId"])
        elif msg["type"] == "msg":
            if self not in ChatHandler.users:
                self.reg(msg["username"], self.userId)
            for sock in ChatHandler.users:
                sock.write_message(message)
        else:
            print("Message Error.")

    # 判断请求源 对于符合条件的请求源允许连接
    def check_origin(self, origin):
        return True

    # 服务器关闭websocket
    #  def on_close(self):
    #  self.users.remove(self)
    #  for u in self.users:
    #  u.write_message(
    #  u"[%s]-[%s]-离开聊天室" %
    #  (self.request.remote_ip,
    #  datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    #  def open(self):
    #  self.users.append(self)  # 建立连接后添加用户到容器中
    #  for u in self.users:  # 向已在线用户发送消息
    #  u.write_message(u"[%s]-[%s]-进入聊天室" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    #  def on_message(self, message):
    #  for u in self.users:  # 向在线用户广播消息
    #  u.write_message(u"[%s]-[%s]-说：%s" % (self.request.remote_ip, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), message))
