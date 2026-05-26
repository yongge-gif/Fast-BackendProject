import random


# 创建验证码生成工具
def generate_code():

    return str(
        random.randint(100000, 999999)  # 生成随机6位数验证码
    )
