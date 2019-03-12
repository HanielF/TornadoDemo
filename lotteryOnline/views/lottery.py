import tornado.web
from tornado.web import RequestHandler


class LotteryHandler(RequestHandler):
    def post(self, *args, **kwargs):
        noun1 = self.get_argument('noun1')
        noun2 = self.get_argument('noun2')
        verb = self.get_argument('verb')
        noun3 = self.get_argument('noun3')
        self.render(
            'lottery.html', first=noun1, second=noun2, third=verb, forth=noun3)
