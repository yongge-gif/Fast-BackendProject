from pydantic_settings import BaseSettings


# Settings 类 每个配置自动类型检查。
class Settings(BaseSettings):

    DATABASE_URL: str

    SECRET_KEY: str

    ALGORITHM: str

    REDIS_HOST: str

    REDIS_PORT: int

    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # 指定读取.env
    class Config:

        env_file = ".env"


# 全局配置对象
settings = Settings()
