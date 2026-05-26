from celery_app import celery
import time


# 创建任务
@celery.task
def send_email(email: str):

    print(f"开始发送邮件: {email}")

    time.sleep(5)  # 模拟耗时任务。

    print("邮件发送成功")

    return "发送成功"