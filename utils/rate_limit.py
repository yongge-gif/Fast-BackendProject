from fastapi import Request, HTTPException
from utils.redis_client import redis_client


# 创建限流依赖
def rate_limit(
    max_requests: int = 5,  # 次数窗口 5 次
    window: int = 60  # 时间窗口 60 秒
):
    # 限流装饰器
    def decorator(request: Request):

        client_ip = request.client.host  # 获取客户端IP。

        key = f"rate_limit:{client_ip}"

        # Redis统计请求次数
        current = redis_client.get(key)

        # 第一次请求
        if current is None:

            redis_client.setex(
                key,
                window,
                1
            )

            return

        # 超过限制直接拒绝
        if int(current) >= max_requests:

            raise HTTPException(
                status_code=429,
                detail="请求过于频繁"
            )

        # 未超限继续增加
        redis_client.incr(key)

    return decorator
