from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = "123456"

ALGORITHM = "HS256"


def create_token(data: dict):

    to_encode = data.copy()  # 复制一份字典, 避免修改原始数据

    expire = datetime.utcnow() + timedelta(hours=2)

    to_encode.update({
        "exp": expire
    })

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM  # 指定 JWT 的签名算法
    )

    return token
