from pydantic import BaseModel, ConfigDict
from typing import List, Optional


# 请求模型

class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    password: str


# 响应模型

class MessageResponse(BaseModel):
    code: int
    msg: str
    data: Optional[dict] = None


class UserResponse(BaseModel):
    id: int
    username: str

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
