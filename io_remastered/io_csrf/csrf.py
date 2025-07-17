from flask import Flask, current_app, session, request, g
from itsdangerous import URLSafeTimedSerializer
import secrets
from io_remastered.io_csrf.exceptions import CSRFValidationException

CSRF_TOKEN_SALT = "io_remastered"
CSRF_TOKEN_FIELD_NAME = "csrf_token"
CSRF_TOKEN_FIELD_NAME_KEY = "CSRF_TOKEN_FIELD_NAME"
CSRF_TOKEN_HTTP_HEADER_NAME = "X-CSRF-TOKEN"


class CSRF:
    def __init__(self):
        pass

    @staticmethod
    def initialize(app: Flask):
        app.context_processor(
            lambda: {"get_csrf_token": CSRF.generate_token})

        app.config[CSRF_TOKEN_FIELD_NAME_KEY] = CSRF_TOKEN_FIELD_NAME

        app.logger.info("[CSRF] initialized")

    @staticmethod
    def generate_token():
        current_token = g.get(CSRF_TOKEN_FIELD_NAME)

        if current_token:
            return current_token

        app_secret = str(current_app.secret_key)
        token_session_field_name = current_app.config.get(
            CSRF_TOKEN_FIELD_NAME_KEY, CSRF_TOKEN_FIELD_NAME)

        signer = URLSafeTimedSerializer(
            secret_key=app_secret, salt=CSRF_TOKEN_SALT)

        new_token = secrets.token_hex(nbytes=32)
        signed_token = signer.dumps(new_token)

        session[token_session_field_name] = new_token
        setattr(g, CSRF_TOKEN_FIELD_NAME, signed_token)

        return signed_token

    @staticmethod
    def validate_token(signed_token: str | None):
        token_ttl = 600  # 10 mins
        app_secret = str(current_app.secret_key)

        session_csrf_token = session.get(CSRF_TOKEN_FIELD_NAME)

        if not session_csrf_token or not signed_token:
            part = "session" if not session_csrf_token else "request"
            raise CSRFValidationException(f"missing CSRF token in {part}")

        signer = URLSafeTimedSerializer(
            secret_key=app_secret, salt=CSRF_TOKEN_SALT)

        try:
            token = signer.loads(s=signed_token, max_age=token_ttl)

        except Exception as e:
            raise CSRFValidationException("CSRF token loading error") from e

        is_match = secrets.compare_digest(token, session_csrf_token)

        if not is_match:
            raise CSRFValidationException("CSRF tokens don't match")

    @staticmethod
    def get_csrf_token_for_current_request():
        field_name = current_app.config.get(CSRF_TOKEN_FIELD_NAME_KEY)

        if not field_name:
            return None

        form_token = request.form.get(field_name)

        if form_token:
            return form_token

        header_token = request.headers.get(CSRF_TOKEN_HTTP_HEADER_NAME)

        if header_token:
            return header_token

        return None

    @staticmethod
    def check_csrf_protected_request():
        is_valid = False

        try:
            current_request_token = CSRF.get_csrf_token_for_current_request()
            CSRF.validate_token(signed_token=current_request_token)

            is_valid = True

        except CSRFValidationException as e:
            current_app.logger.exception(e)

        return is_valid
