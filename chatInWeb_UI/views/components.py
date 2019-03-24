#!/usr/bin/python
# 包含消息类，成员类，聊天室类
import time


# 消息类
# 成员变量:消息内容(str)，消息时间(time.time()时间戳),可以不传这个参数)，消息发送者(成员ID)(str)
class Message:
    def __init__(self, uid, message='', mtime=time.time()):
        self.userId = uid
        self.mes = message
        self.date = mtime


# 成员类
# 成员变量:成员昵称(str)，成员id（str),成员所有聊天室和在其中说过的话（dict{romId(str)[mess](message类型})
class User:
    def __init__(self, uid, unick='None', roms={}):
        self.userId = uid
        self.userNick = unick
        self.uroms = dict(roms.items())

    # 加入新的聊天室
    def addRom(self, romId):
        self.uroms[romId] = []

    # 退出聊天室
    def delRom(self, romId):
        del self.uroms[romId]

    # 用户发言,mess为str
    def addMess(self, romId, mess):
        self.uroms[romId].append(Message(self.userId, mess))


# 聊天室类,成员变量有romId(str),聊天室成员(userId)集合类型,所有聊天记录(list[mess])按照时间排序
class Rom:
    allroms = dict()  # 保存所有聊天室

    def __init__(self, romId='', usersId=set(), allMess=[]):
        self.romId = romId
        self.allMess = allMess
        self.allusers = usersId  # 所有在线的userID
        self.deluser = set()  # 被删除的userId 
        Rom.allroms.append(self)

    def addUser(self,userId):
        self.allusers.add(userId)

    def addMess(self,mess):
        self.allMess.append(mess)

    def delUser(self,userId):
        self.deluser.remove(userId)
        self.allusers.add(userId)

    # uId为当前人员的
    def getNowMess(self,uId):


