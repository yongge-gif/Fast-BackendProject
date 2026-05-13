from pydantic import BaseModel


# 请求模型

class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    password: str


# 响应模型

class MessageResponse(BaseModel):
    msg: str


class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True  # 读取ORM属性




