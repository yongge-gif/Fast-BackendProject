# FastAPI Backend Project

基于 FastAPI + MySQL + SQLAlchemy + Redis 构建的后台管理系统后端项目。

## 项目简介

本项目是一个使用 FastAPI 开发的 RESTful API 后端项目，包含用户认证、权限控制、头像上传、Redis缓存、软删除等常见后台功能。

适合作为 FastAPI 学习项目与后端开发练习项目。

---

## 技术栈

- FastAPI
- SQLAlchemy ORM
- MySQL
- Redis
- JWT认证
- Alembic 数据库迁移
- Pydantic
- Uvicorn

---

## 已实现功能

### 用户模块

- 用户注册
- 用户登录
- JWT Token认证
- Refresh Token刷新
- 获取当前用户信息
- 修改用户信息
- 修改密码
- 用户头像上传

### 权限管理

- RBAC角色权限
- 管理员接口权限控制
- 用户封禁功能

### 数据处理

- 用户软删除
- 分页查询
- 统一响应结构
- 全局异常处理

### Redis缓存

- 用户信息缓存
- Cache Aside旁路缓存模式
- Redis缓存更新策略

---

## 项目结构

```bash
fastapi_project
├── alembic
├── config
├── dependencies
├── models
├── routers
├── schemas
├── services
├── utils
├── uploads
├── main.py
├── database.py
└── requirements.txt
```

---

## 环境配置

创建 `.env` 文件：

```env
DATABASE_URL=mysql+pymysql://root:123456@127.0.0.1:3306/fastapi_db

SECRET_KEY=123456

REDIS_HOST=127.0.0.1
REDIS_PORT=6379
```

---

## 安装依赖

```bash
pip install -r requirements.txt
```

---

## 启动项目

```bash
uvicorn main:app --reload
```

启动后访问：

```bash
http://127.0.0.1:8000/docs
```

Swagger接口文档：

- `/docs`
- `/redoc`

---

## 数据库迁移

生成迁移：

```bash
alembic revision --autogenerate -m "init"
```

执行迁移：

```bash
alembic upgrade head
```

---

## 项目亮点

- 使用 FastAPI 分层架构开发
- 使用 JWT 实现身份认证
- Redis 缓存优化接口性能
- 使用 Alembic 管理数据库迁移
- RESTful API 风格设计
- 统一异常处理与统一响应结构

---

## 开发记录

项目采用 Git 分支与阶段式开发：

- day1 ~ day32 持续迭代
- 从基础 CRUD 到 Redis 缓存优化
- 逐步完善后台权限系统

---

## 作者

杨连勇
Computer Science and Technology
