from models.user_model import User


def login_service(data, db):
    # 使用ORM查询
    user = db.query(User).filter(
        # 条件过滤
        User.username == data.username,
        User.password == data.password,
        User.is_deleted == False
    ).first()

    return user


def register_service(username, password, email, avatar, db):
    # 先查询用户是否存在
    user = db.query(User).filter(
        User.username == username
    ).first()

    # 用户已存在
    if user:
        return False

    # ORM插入数据（注册）
    new_user = User(
        username=username,
        password=password,
        email=email,
        avatar=avatar,
        role="user"
    )

    db.add(new_user)

    db.commit()  # 确认保存

    return True


def get_all_users_service(page, size, username, email, order_by, sort, db):
    offset = (page - 1) * size  # 跳过多少条数据

    # ***“可继续加工”的动态拼接***
    query = db.query(User).filter(
        User.is_deleted == False  # 查询时过滤已软删除的数据
    )

    # 用户名过滤
    if username:
        query = query.filter(
            User.username.like(f"%{username}%")
        )

    # 邮箱过滤
    if email:
        query = query.filter(
            User.email.like(f"%{email}%")
        )

    # 排序
    # 白名单校验
    allowed_fields = [
        "id",
        "username",
        "email"
        "create_time",
        "update_time"
    ]

    if order_by not in allowed_fields:
        order_by = "id"

    order_column = getattr(User, order_by)  # 根据前端传来的字段动态排序

    if sort == "desc":

        query = query.order_by(
            order_column.desc()
        )

    else:

        query = query.order_by(
            order_column.asc()
        )

    total = query.count()

    users = query.offset(offset) \
        .limit(size) \
        .all()

    return {
        "total": total,
        "page": page,
        "size": size,
        "data": users
    }


def update_user_service(user_id, data, db):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    # 用户不存在
    if not user:
        return None

    # 用户名重复校验
    exists_user = db.query(User).filter(
        User.username == data.username,
        User.id != user_id
    ).first()

    if exists_user:
        return "USERNAME_EXISTS"

    # 修改用户名
    if data.username:
        user.username = data.username

    # 修改邮箱
    if data.email:
        user.email = data.email

    db.commit()

    return True


def delete_user_service(
        user_id,
        db
):
    user = db.query(User).filter(
        User.id == user_id,
        User.is_deleted == False
    ).first()

    if not user:
        return False


    # db.delete(user)  # 真删除
    user.is_deleted = True  # 软删除

    db.commit()

    db.commit()

    return True
