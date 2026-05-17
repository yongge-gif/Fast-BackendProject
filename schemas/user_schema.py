from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime


# 请求模型

class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    password: str


class UpdateUserRequest(BaseModel):
    # 允许部分字段修改
    username: Optional[str] = None
    email: Optional[str] = None


# 响应模型

class MessageResponse(BaseModel):
    code: int
    msg: str
    data: Optional[dict] = None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str | None
    avatar: str | None

    create_time: datetime | None
    update_time: datetime | None

    # class Config:
    #     orm_mode = True  # 读取ORM属性    Pydantic V1

    model_config = ConfigDict(             # Pydantic V2
        from_attributes=True
    )


# 分页响应模型
class UserListResponse(BaseModel):

    total: int

    page: int

    size: int

    data: List[UserResponse]

    model_config = ConfigDict(
        from_attributes=True
    )
