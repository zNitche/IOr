from functools import wraps
from flask import abort, request
from io_remastered.io_csrf import CSRF


def csrf_protected(skipped_methods=["GET"]):
    def inner_wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.method not in skipped_methods:
                valid = CSRF.check_csrf_protected_request()

                if not valid:
                    abort(403)

            return f(*args, **kwargs)
        return decorated_function
    return inner_wrapper
