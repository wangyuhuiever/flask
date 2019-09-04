# -*- coding: utf-8 -*-
from functools import wraps
from flask import g
from .errors import forbidden


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorator_function(*args, **kwargs):
            if not g.current_user.can(permission):
                return forbidden('无权限进行当前操作')
            return f(*args, **kwargs)
        return decorator_function
    return decorator
