from jose import jwt, JWTError
from fastapi import Header, HTTPException

SECRET_KEY = "123456"
ALGORITHM = "HS256"


# 创建登录依赖
def get_current_user(
    authorization: str = Header(None, alias="Authorization")
):

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="未登录"
        )

    try:

        token = authorization.split(" ")[1]

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="token无效"
        )
