import tornado.web
from tornado.web import RequestHandler
import json
import numpy as np


class LotteryHandler(RequestHandler):
    def get(self, *args, **kwargs):
        self.write("get")

    def post(self, *args, **kwargs):
        first = self.get_argument('first')
        second = self.get_argument('second')
        third = self.get_argument('third')
        staff = self.get_argument('staff')
        filebody = str(
            self.request.files["uploadFiles"][0]['body'], encoding="utf-8")
        if staff=='' && filebody==''

        # 分词
        if len(staff) != 0:
            names = staff.split(' ')
        elif filebody != '':
            names = filebody.split(' ')
        else:
            self.write("请输入抽奖人员姓名\n")

        cnt = len(names)
        first_names = []
        second_names = []
        third_names = []
        if (first != ''):
            first = int(first)
            for i in range(first):
                pos = np.random.choice(cnt)
                first_names.append(names[pos])
                del names[pos]
                cnt = cnt - 1

        if (second != ''):
            second = int(second)
            for i in range(second):
                pos = np.random.choice(cnt)
                second_names.append(names[pos])
                del names[pos]
                cnt = cnt - 1

        if (third != ''):
            third = int(third)
            for i in range(third):
                pos = np.random.choice(cnt)
                third_names.append(names[pos])
                del names[pos]
                cnt = cnt - 1

        self.render(
            'lottery.html',
            first=first_names,
            second=second_names,
            third=third_names,
        )
