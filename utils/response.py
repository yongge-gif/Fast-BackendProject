def success_response(
    data=None,
    msg="success"
):

    return {
        "code": 200,
        "msg": msg,
        "data": data
    }


def error_response(
    msg="error",
    code=400,
    data=None
):

    return {
        "code": code,
        "msg": msg,
        "data": data
    }
