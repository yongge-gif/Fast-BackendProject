import os
import uuid
import json

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query, Form
from fastapi.responses import JSONResponse
from jose.exceptions import ExpiredSignatureError  # JWT令牌过期异常
from sqlalchemy.orm import Session

from database import get_db
from dependencies.permission import admin_required
from models.user_model import User
from schemas.user_schema import (LoginRequest, MessageResponse, UserListResponse, UpdateUserRequest,
                                 RefreshTokenRequest, ChangePasswordRequest)
from services.user_service import (login_service, register_service, get_all_users_service, update_user_service,
                                   delete_user_service, update_user_status_service)
from utils.auth import get_current_user, oauth2_scheme
from utils.jwt_util import create_access_token, create_refresh_token, decode_token
from utils.logger import logger
from utils.password import verify_password, hash_password
from utils.response import (success_response, error_response)
from utils.token_blacklist import token_blacklist
from utils.redis_client import redis_client
from utils.rate_limit import rate_limit

from tasks.email_task import send_email



router = APIRouter()


@router.post("/register", response_model=MessageResponse)  # 注册接口
async def register(
        username: str = Form(...),
        password: str = Form(...),
        email: str = Form(...),
        avatar: Optional[UploadFile] = File(None),  # 可以不上传，使用默认头像
        db: Session = Depends(get_db)
):
    filename = "default.png"

    if avatar:
        # 生成唯一文件名
        suffix = avatar.filename.split(".")[-1]

        # 上传类型限制
        if not avatar.content_type.startswith("image/"):  # 上传限制
            return error_response(
                msg="只能上传图片"
            )

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
def login(
        data: LoginRequest,
        db: Session = Depends(get_db),
        _: None = Depends(rate_limit(5, 60))  # 添加限流依赖
):
    logger.info("用户开始登录")

    user = login_service(data, db)

    if not user:
        logger.warning(f"用户 {data.username} 不存在")

        return JSONResponse(
            status_code=401,
            content=error_response(
                msg="账号或密码错误",
                code=401
            )
        )

    # 状态校验
    if user.status == 0:
        logger.warning(f"用户{data.username}已被封禁")

        return error_response(
            msg="账号已被禁用",
            code=403
        )


    if not verify_password(
        data.password,
        user.password
    ):
        logger.warning(f"用户{data.username} 密码验证失败")

        return JSONResponse(
            status_code=401,
            content=error_response(
                msg="账号或密码错误",
                code=401
            )
        )

    # 返回双token
    access_token = create_access_token({
        "user_id": user.id,
        "role": user.role
    })

    refresh_token = create_refresh_token({
        "user_id": user.id,
        "role": user.role
    })

    logger.info(f"用户 {data.username} 登录成功")

    return success_response(
        msg="登录成功",
        data={
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    )


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

    return success_response(
        data=users
    )


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


# 更新用户头像接口
@router.put("/users/avatar")
async def update_user_avatar(
        avatar: UploadFile = File(...),
        current_user=Depends(get_current_user),  # 通过 JWT 获取当前登录用户
        db: Session = Depends(get_db)
):

    # 查询当前用户
    user = db.query(User).filter(
        User.id == current_user["user_id"]
    ).first()

    # 删除旧头像
    if user.avatar:

        old_file = f"uploads/{user.avatar}"

        if os.path.exists(old_file):
            os.remove(old_file)

    # 保存新头像
    suffix = avatar.filename.split(".")[-1]

    filename = f"{uuid.uuid4()}.{suffix}"

    file_path = f"uploads/{filename}"

    with open(file_path, "wb") as f:

        content = await avatar.read()

        f.write(content)

    # 更新
    user.avatar = filename

    db.commit()

    # 删除旧缓存
    redis_client.delete(
        f"user:{user.id}"
    )

    # 返回
    return success_response(
        data={
            "avatar_url": f"http://127.0.0.1:8000/uploads/{filename}"
        },
        msg="头像更新成功"
    )


# 密码修改接口
@router.put("/users/password")
def change_password(
    data: ChangePasswordRequest,
    current_user=Depends(get_current_user),  # 通过 JWT 获取当前登录用户。
    db: Session = Depends(get_db)
):

    # 查询当前用户
    user = db.query(User).filter(
        User.id == current_user["user_id"]
    ).first()

    # 校验旧密码
    if not verify_password(
            data.old_password,
            user.password
    ):
        return error_response(
            msg="旧密码错误",
            code=400
        )

    # 更改新密码
    user.password = hash_password(
        data.new_password
    )

    # 新旧密码相同校验
    if data.old_password == data.new_password:
        return error_response(
            msg="新密码不能与旧密码相同"
        )

    db.commit()

    return success_response(
        msg="密码修改成功"
    )


# 用户名，邮箱更新接口
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
        db: Session = Depends(get_db),
        _current_user=Depends(admin_required)  # 权限依赖链: DELETE接口 → admin_required → get_current_user → JWT认证
        # 不用current_user变量
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


# token刷新接口
@router.post("/refresh")
def refresh_token_api(
    data: RefreshTokenRequest
):

    try:

        payload = decode_token(
            data.refresh_token
        )

        new_access_token = create_access_token(
            {
                "user_id": payload["user_id"],
                "role": payload["role"]
            }
        )

        return success_response(
            data={
                "access_token": new_access_token
            },
            msg="刷新成功"
        )

    except ExpiredSignatureError:

        return error_response(
            msg="refresh_token已过期",
            code=401
        )

    except Exception as e:
        print(e)

        return error_response(
            msg=str(e),
            code=401
        )


# 禁用接口
@router.put("/users/{user_id}/status")
def update_user_status(
    user_id: int,
    status: int,
    db: Session = Depends(get_db),
    _current_user=Depends(admin_required)  # 权限依赖 管理员能封禁
):
    result = update_user_status_service(
        user_id,
        status,
        db
    )

    if not result:
        return error_response(
            msg="用户不存在",
            code=404
        )

    return success_response(
        msg="状态修改成功"
    )


# 查询当前用户接口
@router.get("/me")
def get_current_user_info(
    current_user=Depends(get_current_user),  # id来自jwt解析，无状态身份认证
    db: Session = Depends(get_db)
):
    # 先检查缓存
    cache_user = redis_client.get(
        f"user:{current_user['user_id']}"
    )
    # 如果缓存存在
    if cache_user:
        return success_response(
            data=json.loads(cache_user),
            msg="获取成功（Redis缓存）"
        )

    # 数据库查询完整信息
    user = db.query(User).filter(
        User.id == current_user["user_id"]
    ).first()

    user_data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "avatar_url": f"http://127.0.0.1:8000/uploads/{user.avatar}",
            "role": user.role,
            "status": user.status
        }

    # 写入Redis缓存
    redis_client.setex(  # 设置缓存 + 过期时间
        f"user:{user.id}",
        300,
        json.dumps(user_data)  # dict → JSON字符串
    )

    return success_response(
        data=user_data,
        msg="获取成功"
    )


# 退出登录接口
@router.post("/logout")
def logout(
    token: str = Depends(oauth2_scheme)
):
    # token加入黑名单
    token_blacklist.add(token)

    return success_response(
        msg="退出登录成功"
    )


# 调用异步任务接口
@router.post("/send-email")
def send_email_api(email: str):

    send_email.delay(email)  # 丢进任务队列

    return success_response(
        msg="邮件发送任务已提交"
    )
