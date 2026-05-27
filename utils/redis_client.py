import redis
from core.config import settings

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,  # 使用 Redis 的 0 号数据库
    decode_responses=True  # 让 Redis 返回字符串。
)

# 测试 Redis 连接
# redis_client.set("test", "hello")
#
# print(redis_client.get("test"))
