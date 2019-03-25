import os
BASE_DIRS = os.path.dirname(__file__)

# 参数
options = {"port": 8000}

# 配置
settings = {
    "static_path": os.path.join(BASE_DIRS, "static"),
    "template_path": os.path.join(BASE_DIRS, "templates"),
    "debug": True,
    "cookie_secret": "R7Qf5K9OQW6ibStACf2PwXuIeNZB3UvyiX4TU97aUBk=",
    "login_url": "/login",
}
