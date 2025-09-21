from functools import wraps
from datetime import datetime
from flask import redirect, url_for, session, abort, g, request
from io_remastered import authentication_manager


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_token = session.get("auth_token")

        if not auth_token:
            abort(401)

        current_user = authentication_manager.user_for_token(auth_token)

        if not current_user:
            abort(401)

        setattr(g, "current_user", current_user)

        authentication_manager.refresh(
            token=auth_token, user_id=current_user.id)

        return f(*args, **kwargs)
    return decorated_function


def anonymous_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_token = session.get("auth_token")

        if auth_token and authentication_manager.token_exists(auth_token):
            return redirect(url_for("core.home"))

        return f(*args, **kwargs)
    return decorated_function


def password_authentication_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        origin_url = request.base_url
        referrer_url = request.referrer

        def set_password_authentication_origin():
            return authentication_manager.set_password_authentication_origin(origin_url=origin_url,
                                                                             referrer_url=referrer_url)

        password_auth_page_url = url_for("auth.password_authentication")
        last_auth = authentication_manager.get_last_password_authentication()

        if not last_auth:
            set_password_authentication_origin()
            return redirect(password_auth_page_url)

        now = datetime.now().timestamp()
        last_auth = last_auth.timestamp() + 300

        if last_auth <= now:
            set_password_authentication_origin()
            return redirect(password_auth_page_url)

        return f(*args, **kwargs)
    return decorated_function
