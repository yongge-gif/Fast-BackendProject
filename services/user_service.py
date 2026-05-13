from models.user_model import User


def login_service(data, db):

    # 使用ORM查询
    user = db.query(User).filter(
        # 条件过滤
        User.username == data.username,
        User.password == data.password
    ).first()

    return user


def register_service(data, db):

    # 先查询用户是否存在
    user = db.query(User).filter(
        User.username == data.username
    ).first()

    # 用户已存在
    if user:
        return False



    # ORM插入数据（注册）
    new_user = User(
        username=data.username,
        password=data.password
    )

    db.add(new_user)

    db.commit()  # 确认保存

    return True


def get_all_users_service(page, size, db):

    offset = (page - 1)* size  # 跳过多少条数据

    total = db.query(User).count()

    users = db.query(User)\
        .offset(offset)\
        .limit(size)\
        .all()

    return {
        "total": total,
        "page": page,
        "size": size,
        "users": users
    }
