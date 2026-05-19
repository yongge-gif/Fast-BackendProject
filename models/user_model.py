from sqlalchemy import Column, String, Integer, Boolean
from database import Base
from sqlalchemy import DateTime
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50))
    password = Column(String(100))
    email = Column(String(100))
    avatar = Column(String(100))

    # 新增用户自动记录创建时间
    create_time = Column(
        DateTime,
        default=datetime.utcnow  # 创建时自动赋值。
    )

    # 修改用户自动更新 update_time
    update_time = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow  # 更新时自动刷新时间。
    )

    # 软删除字段
    is_deleted = Column(
        Boolean,
        default=False,  # False: 未删除
        nullable=False  # 不许出现Null
    )

    # 权限字段
    role = Column(
        String(20),
        default="user"
    )

    # 状态字段
    status = Column(
        Integer,
        default=1  # 正常用户
    )
