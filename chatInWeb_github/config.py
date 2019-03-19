import os
BASE_DIRS = os.path.dirname(__file__)

# 参数
options = {"port": 8000}

# 配置
settings = {
    "static_path": os.path.join(BASE_DIRS, "static"),
    "template_path": os.path.join(BASE_DIRS, "templates"),
    "debug": True,
}
