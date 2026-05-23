from jose import jwt, JWTError
from fastapi import Header, HTTPException, Depends

from config.settings import SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer  # 一个安全工具类，方便从请求中获取 Bearer Token
from utils.token_blacklist import token_blacklist

# 创建OAuth2, 获取 Bearer Token 的依赖对象
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)


# 创建登录依赖
def get_current_user(
        # authorization: str = Header(None, alias="Authorization")  # 手动从header中取token
        token: str = Depends(oauth2_scheme)
):
    if not token:
        raise HTTPException(
            status_code=401,
            detail="未登录或未携带token"
        )

    if token in token_blacklist:
        raise HTTPException(
            status_code=401,
            detail="token已失效"
        )

    try:

        # token = authorization.split(" ")[1]  不需要了 OAuth2PasswordBearer自动提取出了token

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
