from celery_app import celery
import time


# 创建异步邮件任务
@celery.task
def send_email(email: str, code: str):

    print(f"向邮箱 {email} 发送验证码 {code}")

    time.sleep(5)  # 模拟耗时任务。

    print("邮件发送成功")

    return "发送成功"
