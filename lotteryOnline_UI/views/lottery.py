import tornado.web
from tornado.web import RequestHandler
import json
import numpy as np

cnts = np.zeros(3, np.int)  # 存放一二三等奖的各自人数
plist = []  # 存放一二三等奖概率
names = []  # 存放所有的人
res = []  # 除去当次中奖剩下的人,用作缓冲
info = ""
partSize = 5

first_names = []
second_names = []
third_names = []


def lotteryAgain():
    global info, plist, first_names, second_names, third_names, names, cnts, res, partSize
    if len(names) == 0 or cnts.sum(axis=0) == 0:
        info = info + "已经全部抽完"
        return
    if cnts.sum(axis=0) < partSize:
        partSize = cnts.sum(axis=0)

    # 中奖的候选人
    if len(names) <= partSize:
        candidates = np.arange(len(names))
    else:
        candidates = np.random.choice(len(names), partSize, replace=False)

    for i in range(len(candidates)):
        # 随机抽取是几等奖
        step = np.random.choice(3, 1, p=plist)[0]
        while cnts[step] == 0:
            step = np.random.choice(3, 1, p=plist)[0]

        cnts[step] = cnts[step] - 1
        if (step == 0):
            first_names.append(names[candidates[i]])
        elif (step == 1):
            second_names.append(names[candidates[i]])
        else:
            third_names.append(names[candidates[i]])

    for j in range(len(names)):
        if j not in candidates:
            res.append(names[j])
    names = res
    res = []

    #  info = "names:" + ",".join(names) + "first:" + ",".join(first_names) + "second:" + ",".join(second_names) + "third:" + ",".join(third_names)


def lotteryInit():
    global info, first_names, second_names, third_names
    info = ""
    first_names = []
    second_names = []
    third_names = []


# 抽一次，一次五个人,不足就停止
class LotteryHandler(RequestHandler):
    def get(self, *args, **kwargs):
        global info, first_names, second_names, third_names
        info = ""
        lotteryAgain()
        self.render(
            'lottery.html',
            first=first_names,
            second=second_names,
            third=third_names,
            info=info,
        )

    def post(self, *args, **kwargs):
        global plist, info, first_names, second_names, third_names, names, cnts
        lotteryInit()

        cnts[0] = self.get_argument('first')
        cnts[1] = self.get_argument('second')
        cnts[2] = self.get_argument('third')
        cnt_sum = cnts.sum(axis=0)
        plist = [cnts[0] / cnt_sum, cnts[1] / cnt_sum, cnts[2] / cnt_sum]

        if not self.get_argument('staff') is None:
            staff = self.get_argument('staff')
            names = staff.split(' ')
        elif not self.request.files["uploadFiles"][0]['body'] is None:
            filebody = str(self.request.files["uploadFiles"][0]['body'], encoding="utf-8")
            names = filebody.split(' ')
        else:
            return

        lotteryAgain()
        self.render(
            'lottery.html',
            first=first_names,
            second=second_names,
            third=third_names,
            info=info,
        )
