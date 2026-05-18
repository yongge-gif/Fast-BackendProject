from fastapi import HTTPException, Depends

from utils.auth import get_current_user


def admin_required(
    current_user=Depends(get_current_user)  # 先验证token
):

    if current_user.get("role") != "admin":

        raise HTTPException(
            status_code=403,
            detail="没有权限"
        )

    return current_user
