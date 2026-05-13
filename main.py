import time
from fastapi import FastAPI, Request
from routers.user_router import router
from database import engine
from models.user_model import User
from fastapi.responses import JSONResponse
from utils.logger import logger
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager  # 导入“异步上下文管理器”装饰器


# 创建生命周期管理
@asynccontextmanager
async def lifespan(app: FastAPI):

    # 启动逻辑
    logger.info("数据库连接成功")
    logger.info("日志初始化成功")

    yield  # 上下文管理

    # 关闭逻辑
    logger.info("项目安全关闭")


app = FastAPI(lifespan=lifespan)

# app = FastAPI()

app.include_router(router)  # 把其它文件里的路由“注册”到主程序中。

User.metadata.create_all(bind=engine)  # 自动创建表


@app.middleware("http")
async def db_session_middleware(
        request,
        call_next
):  # 异步定义
    start_time = time.time()  # 记录开始时间

    print("=" * 50)

    print(f"请求方式: {request.method}")
    print(f"请求路径: {request.url}")
    print(f"客户端IP: {request.client.host}")

    # 放行请求
    response = await call_next(request)  # 继续执行真正接口

    process_time = time.time() - start_time  # 计算耗时

    print(f"请求耗时: {process_time * 1000:.2f}ms")

    print("=" * 50)

    return response


@app.exception_handler(Exception)
async def global_exception_handler(
        request: Request,
        exc: Exception
):
    logger.error(f"系统异常: {exc}")

    return JSONResponse(
        status_code=500,
        content={
            "code": 500,
            "msg": "服务器内部错误"},
    )


# 挂载静态目录
app.mount(
    "/uploads",  # 表示：浏览器访问路径：http://127.0.0.1:8000/uploads/xxx.png
    StaticFiles(directory="uploads"),  # 表示：本地真实目录：项目目录/uploads
    name="uploads"
)
