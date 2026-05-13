from sqlalchemy import Column, String, Integer

from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50))
    password = Column(String(100))
    email = Column(String(100))
    avatar = Column(String(100))
