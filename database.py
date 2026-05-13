from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+pymysql://root:123456@127.0.0.1:3306/fastapi_db"

# 创建引擎
engine = create_engine(DATABASE_URL)

# 创建会话 生成数据库操作对象
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,  # 自动提交事务关闭
    autoflush=False  # 自动同步关闭
)

# ORM基类
Base = declarative_base()


# 数据库依赖
def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
