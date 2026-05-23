import redis

redis_client = redis.Redis(
    host="127.0.0.1",
    port=6379,
    db=0,
    decode_responses=True  # 让 Redis 返回字符串。
)

# 测试 Redis 连接
# redis_client.set("test", "hello")
#
# print(redis_client.get("test"))
