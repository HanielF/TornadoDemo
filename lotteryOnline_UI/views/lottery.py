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


# 负责抽奖的函数，杯其它函数调用
def lotteryAgain():
    global info, plist, first_names, second_names, third_names, names, cnts, res, partSize

    # 对现在的状态进行判断，是否奖品抽完或者参与的人员抽完
    if len(names) == 0 or cnts.sum(axis=0) == 0:
        info = info + "已经全部抽完"
        return
    if cnts.sum(axis=0) < partSize:
        partSize = cnts.sum(axis=0)

    # 中奖的候选人设置
    # 如果人数足够，就调用choice函数，一次随机生成这一批的候选人
    # 如果剩下的人数不足原本设置的人数，则剩下的所有人作为这次抽奖的候选人
    if len(names) <= partSize:
        candidates = np.arange(len(names))
    else:
        candidates = np.random.choice(len(names), partSize, replace=False)

    # 对每个随机抽到的人进行排队抽奖，调用choice函数和中奖概率数组
    for i in range(len(candidates)):
        # 按概率抽取这个人是几等奖
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


# 初始化全局变量,可以在返回主页时调用
def lotteryInit():
    global info, first_names, second_names, third_names, partSize
    info = ""
    partSize = 5
    first_names = []
    second_names = []
    third_names = []


# 负责抽奖的后台程序
class LotteryHandler(RequestHandler):

    # 此函数工作在点击再抽一次按钮之后，调用抽奖函数
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

    # 此函数工作在第一次提交抽奖人数和参与人员之后，调用抽奖函数
    def post(self, *args, **kwargs):
        global plist, info, first_names, second_names, third_names, names, cnts
        lotteryInit()

        # 保存奖品人数并计算每等奖的中奖概率
        cnts[0] = self.get_argument('first')
        cnts[1] = self.get_argument('second')
        cnts[2] = self.get_argument('third')
        cnt_sum = cnts.sum(axis=0)
        plist = [cnts[0] / cnt_sum, cnts[1] / cnt_sum, cnts[2] / cnt_sum]

        # 对输入的抽奖人员进行数据处理，存在全局数组中
        if not self.get_argument('staff') is '':
            staff = self.get_argument('staff')
            names = staff.split(' ')
            #  info = info + "有输入"
        else:
            filebody = str(self.request.files["uploadFiles"][0]['body'], encoding="utf-8")
            names = filebody.split(' ')
            #  info = info + "有文件"
        print(names)

        # 调用抽奖函数并将结果返回前端
        lotteryAgain()
        self.render(
            'lottery.html',
            first=first_names,
            second=second_names,
            third=third_names,
            info=info,
        )
