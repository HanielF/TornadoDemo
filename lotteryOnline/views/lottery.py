import tornado.web
from tornado.web import RequestHandler


class LotteryHandler(RequestHandler):
    def post(self, *args, **kwargs):
        first = self.get_argument('first')
        second = self.get_argument('second')
        third = self.get_argument('third')
        staff = self.get_argument('staff')
        nameFile = self.get_argument('nameFile')

        if len(staff) != 0:
            names = staff.split('，')
        elif nameFile is not None:
            pass
        else:
            pass

        self.render(
            'lottery.html',
            first=first,
            second=second,
            third=third,
            staff=staff,
            nameFile=nameFile,
            names=names[0],
        )
