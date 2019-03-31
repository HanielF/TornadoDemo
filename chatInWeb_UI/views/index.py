import tornado.web
from tornado.websocket import WebSocketHandler
from tornado.web import RequestHandler
import os
import json
import uuid
import datetime
import time


# 视图类
class BaseHandler(RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class IndexHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.render("index.html", username=self.get_argument("userName"))


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
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.get_argument("username")
        self.set_secure_cookie("user", username)
        pwd = self.get_argument("passWord")
        self.set_secure_cookie("passWord", pwd)
        self.redirect("/index")


class LogoutHandler(BaseHandler):
    def get(self):
        if (self.get_argument("logout", None)):
            self.clear_cookie("user")
            self.redirect("/")


#  ====================================================================


# 在新的websocket连接之后执行open函数
class ChatHandler(WebSocketHandler, BaseHandler):
    users = set()  # 用于存储在线用户
    cache = {
        'ChatRoom1msgBody': [],
    }  # 聊天记录
    usersTime = {}

    #  这个方法向客户端发送message消息，message可以使字符串或者字典(自动转为json字符串)如果binary参数为false,则message会以utf-8的编码发送,如果为true,可以发送二进制模式字节码
    def open(self):
        self.write_message(
            json.dumps({
                'type': 'sys',
                'username': 'SYSTEM',
                'roomBody': u'ChatRoom1msgBody',
                'message': u'Welcome to the Room',
            }))

    # 更新cache
    @classmethod
    def update_cache(cls, mess):
        msg = json.loads(mess)
        room = msg["roomBody"]
        cls.cache[room].append(mess)

    # 缓存的消息进行推送
    @classmethod
    def push_cache(cls, sock, roomBody):
        i = 0
        length = len(ChatHandler.cache[roomBody])
        for t in ChatHandler.usersTime[sock.username]:
            while i < length:
                tmpMsg = json.loads(ChatHandler.cache[roomBody][i])
                if tmpMsg["mtime"] >= t[1]:
                    break
                if tmpMsg["mtime"] >= t[0] and tmpMsg["mtime"] < t[1]:
                    tmpMsg["mtime"] = time.strftime(
                        "[%H:%M:%S]", time.localtime(tmpMsg["mtime"]))
                    sock.write_message(json.dumps(tmpMsg))
                i = i + 1

    #  对在线的人进行推送
    @classmethod
    def send_updates(cls, msgtype, uname, rooms, msg):
        for sock in ChatHandler.users:
            for room in rooms:
                if room in sock.rooms:
                    sock.write_message(
                        json.dumps({
                            'type': msgtype,
                            'username': uname,
                            'roomBody': room,
                            'message': msg,
                        }))

    # 当websocket连接关闭后调用，客户端主动的关闭
    def on_close(self):
        self.onlineTime.append(int(time.time()))
        ChatHandler.usersTime[self.username].append(
            self.onlineTime)  # 将用户的在线时间加入用户的在线时间表
        ChatHandler.users.remove(self)
        ChatHandler.send_updates('sys', 'SYSTEM', self.rooms,
                                 self.username + ' has left!')
        print(ChatHandler.usersTime)

    def reg(self, username, roomBody):
        self.username = username
        self.onlineTime = []
        self.onlineTime.append(int(time.time()))
        if username not in ChatHandler.usersTime.keys():
            ChatHandler.usersTime[username] = []

        self.rooms = set()
        self.rooms.add(roomBody)

        # 如果不存在这个聊天室则添加
        if roomBody not in ChatHandler.cache.keys():
            ChatHandler.cache[roomBody] = []
        #  self.uid = ''.join(str(uuid.uuid4()).split('-'))
        ChatHandler.send_updates('sys', 'SYSTEM', self.rooms,
                                 self.username + ' has joined!')
        if self not in ChatHandler.users:
            ChatHandler.users.add(self)
        ChatHandler.push_cache(self, 'ChatRoom1msgBody')

    #  当客户端发送消息过来时调用
    def on_message(self, message):
        msg = json.loads(message)
        msg["mtime"] = int(time.time())
        tmpMsg = json.dumps(msg)
        print(msg)
        if msg["type"] == "reg":
            self.reg(msg["username"], msg["roomBody"])
        elif msg["type"] == "msg":
            if self not in ChatHandler.users:
                self.reg(msg["username"], msg["roomBody"])
            for sock in ChatHandler.users:
                revTimeMsg = json.loads(tmpMsg)
                revTimeMsg["mtime"] = time.strftime(
                    "[%H:%M:%S]", time.localtime(msg["mtime"]))
                sock.write_message(json.dumps(revTimeMsg))
        elif msg["type"] == "addroom":
            self.rooms.add(msg["roomBody"])
            if msg["roomBody"] not in ChatHandler.cache.keys():
                ChatHandler.cache[msg["roomBody"]] = []
            self.write_message(
                json.dumps({
                    'type': 'sys',
                    'username': 'SYSTEM',
                    'roomBody': msg["roomBody"],
                    'message': u'Welcome to the Room',
                }))
            ChatHandler.push_cache(self, msg["roomBody"])
            ChatHandler.send_updates('sys', 'SYSTEM', [
                msg["roomBody"],
            ], self.username + ' has joined!')
        else:
            print("Message Error.")
        ChatHandler.update_cache(tmpMsg)

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
