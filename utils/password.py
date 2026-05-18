from passlib.context import CryptContext  # passlib 的密码管理器

# 加密工具
pwd_context = CryptContext(
    schemes=["bcrypt"],  # 使用bcrypt算法
    deprecated="auto"  # 算法淘汰策略 意思是：如果未来旧算法不安全了，passlib 会自动识别旧密码并建议升级
)


# 密码加密函数
def hash_password(password: str):

    return pwd_context.hash(password)


# 密码校验函数
def verify_password(
    plain_password,
    hashed_password
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )