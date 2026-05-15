from models.user_model import User


def login_service(data, db):

    # 使用ORM查询
    user = db.query(User).filter(
        # 条件过滤
        User.username == data.username,
        User.password == data.password
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
        avatar=avatar
    )

    db.add(new_user)

    db.commit()  # 确认保存

    return True


def get_all_users_service(page, size, username, email, db):

    offset = (page - 1)* size  # 跳过多少条数据

    query = db.query(User)  # ***“可继续加工”的动态拼接***

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

    total = query.count()

    users = query.offset(offset) \
        .limit(size) \
        .all()

    return {
        "total": total,
        "page": page,
        "size": size,
        "users": users
    }
