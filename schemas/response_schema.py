from pydantic import BaseModel
from typing import Any


class ResponseModel(BaseModel):

    code: int

    msg: str

    data: Any = None  # data可以是任意类型
