import uuid
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, Form
from sqlalchemy.orm import Session
from utils.auth import get_current_user
from database import get_db
from schemas.user_schema import LoginRequest, MessageResponse, UserListResponse, UpdateUserRequest
from services.user_service import (login_service, register_service, get_all_users_service, update_user_service,
                                   delete_user_service)
from utils.jwt_util import create_token
from utils.logger import logger
from typing import Optional

router = APIRouter()


@router.post("/register", response_model=MessageResponse)  # 注册接口
async def register(
        username: str = Form(...),
        password: str = Form(...),
        email: str = Form(...),
        avatar: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    # 生成唯一文件名
    suffix = avatar.filename.split(".")[-1]

    # 上传类型限制
    if not avatar.content_type.startswith("image/"):  # 上传限制
        return {"msg": "只能上传图片"}

    filename = f"{uuid.uuid4()}.{suffix}"

    file_path = f"uploads/{filename}"

    # 保存头像
    with open(file_path, "wb") as f:
        content = await avatar.read()

        f.write(content)

    result = register_service(username, password, email, filename, db)

    if not result:
        raise HTTPException(
            status_code=400,
            detail="用户已存在"
        )

    return {
        "code": 200,
        "msg": "注册成功",
        "data": {
            "avatar_url": f"http://127.0.0.1:8000/uploads/{filename}"  # 返回头像访问地址
        }
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


@router.get("/users", response_model=UserListResponse)  # 查询所有用户
def get_all_users(
        page: int = Query(1, ge=1),  # 大于等于1
        size: int = Query(5, le=50),  # 不传参默认5条, 最大50条

        username: Optional[str] = Query(
            None,
            min_length=1,
            max_length=15
        ),  # Optional[str]表示可以为str或空

        email: Optional[str] = Query(
            None,
            max_length=30
        ),

        order_by: str = "id",

        sort: str = "desc",

        # 登录验证
        _user=Depends(get_current_user),  # _user 表示故意不用它”

        db: Session = Depends(get_db)
):
    users = get_all_users_service(page, size, username, email, order_by, sort, db)

    return users


@router.get("/error")
def test_error():
    1 / 0


@router.post("/upload")  # 上传文件
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


# 更新接口
@router.put("/users/{user_id}")
def update_user(
        user_id: int,
        data: UpdateUserRequest,
        db: Session = Depends(get_db)
):
    result = update_user_service(
        user_id,
        data,
        db
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="用户不存在, 修改失败"
        )

    if result == "USERNAME_EXISTS":
        raise HTTPException(
            status_code=400,
            detail="用户名已存在, 修改失败"
        )

    return {
        "code": 200,
        "msg": "修改成功"
    }


# 删除接口
@router.delete("/users/{user_id}")
def delete_user(
        user_id: int,
        db: Session = Depends(get_db)
):
    result = delete_user_service(
        user_id,
        db
    )

    if result == False:
        raise HTTPException(
            status_code=404,
            detail="用户不存在, 删除失败"
        )

    return {
        "code": 200,
        "msg": "删除成功"
    }
