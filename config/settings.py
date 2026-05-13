from dotenv import load_dotenv

import os

load_dotenv()  # 把 .env 文件里的内容加载到环境变量中


DATABASE_URL = os.getenv("DATABASE_URL")  # os.getenv() 意思：读取环境变量

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM")