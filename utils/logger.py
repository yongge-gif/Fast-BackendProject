import logging
from logging.handlers import RotatingFileHandler

# 创建logger
logger = logging.getLogger("fastapi")

# # 防止重复添加handler
# if not logger.handlers:

# 设置日志等级
logger.setLevel(logging.INFO)
# 日志格式
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)
# 创建控制台输出器
console_handler = logging.StreamHandler()  # 日志输出到终端/控制台
# 给“输出器”设置日志格式
console_handler.setFormatter(formatter)
# 日志写入文件
file_handler = RotatingFileHandler(
    "logs/app.log",
    maxBytes=1024 * 1024,  # 超过1MB自动切割
    backupCount=3,  # 保留3个历史日志
    encoding="utf-8"
)
file_handler.setFormatter(formatter)
# 添加handler
logger.addHandler(console_handler)
logger.addHandler(file_handler)
