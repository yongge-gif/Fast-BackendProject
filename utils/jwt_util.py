from jose import jwt
from datetime import datetime, timedelta
from core.config import settings


# def create_token(data: dict):
#
#     to_encode = data.copy()  # 复制一份字典, 避免修改原始数据
#
#     expire = datetime.utcnow() + timedelta(hours=2)
#
#     to_encode.update({
#         "exp": expire
#     })
#
#     token = jwt.encode(
#         to_encode,
#         SECRET_KEY,
#         algorithm=ALGORITHM  # 指定 JWT 的签名算法
#     )
#
#     return token


# 访问接口
def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=30
    )

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


# 刷新登录状态
def create_refresh_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        days=7
    )

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


# 解析并验证token
def decode_token(token: str):

    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=settings.ALGORITHM
    )
