from celery import Celery

# 创建 Celery 配置
celery = Celery(
    "fastapi_project",
    broker="redis://127.0.0.1:6379/0",  # 消息队列
    backend="redis://127.0.0.1:6379/0",  # 任务结果储存
    include=["tasks.email_task"]  # 启动Worker时 自动导入任务模块
)
