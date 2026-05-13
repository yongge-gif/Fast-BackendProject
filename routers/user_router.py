import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from database import get_db
from schemas.user_schema import UserResponse, LoginRequest, RegisterRequest, MessageResponse
from services.user_service import login_service, register_service, get_all_users_service
from utils.auth import get_current_user
from utils.jwt_util import create_token
from utils.logger import logger

router = APIRouter()


@router.post("/register", response_model=MessageResponse)  # 注册接口
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    result = register_service(data, db)

    if not result:
        raise HTTPException(
            status_code=400,
            detail="用户已存在"
        )

    return {
        "code": 200,
        "msg": "注册成功"
    }


@router.post("/login")  # 登录接口
def login(data: LoginRequest, db: Session = Depends(get_db)):
    logger.info("用户开始登录")

    user = login_service(data, db)

    if not user:
        logger.warning(f"用户 {data.username} 登录失败")

        raise HTTPException(
            status_code=401,
            detail="账号或密码错误"
        )

    token = create_token({
        "username": user.username,
    })

    logger.info(f"用户 {data.username} 登录成功")

    return {
        "code": 200,
        "msg": "登录成功",
        "data": {"token": token}
    }


@router.get("/users", response_model=List[UserResponse])  # 查询所有用户
def get_all_users(
        user = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    users = get_all_users_service(db)

    return users


@router.get("/error")
def test_error():

    1 / 0


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):  # 上传文件对象

    suffix = file.filename.split(".")[-1]  # 获取文件后缀名

    # if not file.content_type.startswith("image/"):  # 上传限制
    #     return {"msg": "只能上传图片"}

    filename = f"{uuid.uuid4()}.{suffix}"  # 生成唯一文件名，避免文件名覆盖

    file_path = f"uploads/{filename}"

    with open(file_path, "wb") as f:  # wb 表示 二进制写入

        content = await file.read()  # 异步读取文件内容。

        f.write(content)

    return {
        "msg": "上传成功",
        "filename": filename,
        "url": f"http://127.0.0.1:8000/uploads/{filename}"  # 返回文件访问地址
    }