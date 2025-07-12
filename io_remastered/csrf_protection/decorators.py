from functools import wraps
from flask import abort
from io_remastered.csrf_protection import CSRF


def csrf_protected(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        status = CSRF.check_csrf_protected_request()

        if not status:
            abort(403)

        return f(*args, **kwargs)
    return decorated_function
