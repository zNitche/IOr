from flask import Request


def is_js_request(request: Request):
    return request.headers.get("X-Is-JS-Request", False)
