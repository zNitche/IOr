from functools import wraps
from flask import abort, request


# max_content_length in MB
def limit_content_length(max_content_length: int | None):
    def inner_wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if max_content_length is not None:
                max_content_length_in_bytes = max_content_length * 1000 * 1000

                if request.content_length and (request.content_length > max_content_length_in_bytes):
                    abort(403)

            return f(*args, **kwargs)
        return decorated_function
    return inner_wrapper
