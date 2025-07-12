from flask import Flask, current_app, g, session, abort, request
from itsdangerous import URLSafeTimedSerializer
import secrets
from io_remastered.csrf_protection.exceptions import CSRFValidationException

CSRF_TOKEN_FIELD_NAME = "csrf_token"
CSRF_TOKEN_FIELD_NAME_KEY = "CSRF_TOKEN_FIELD_NAME"
CSRF_PROTECTED_METHODS_KEY = "CSRF_PROTECTED_METHODS_KEY"


class CSRF:
    def __init__(self, app: Flask):
        self.app = app

    def setup(self):
        self.app.context_processor(
            lambda: {"get_csrf_token": self.generate_token})
        self.app.logger.info("[CSRF] enabled")

        self.app.config[CSRF_TOKEN_FIELD_NAME_KEY] = CSRF_TOKEN_FIELD_NAME
        self.app.config[CSRF_PROTECTED_METHODS_KEY] = [
            "POST", "PUT", "PATCH", "DELETE"]

        @self.app.before_request
        def csrf_before_request():
            csrf_protected_methods = current_app.config.get(
                "CSRF_PROTECTED_METHODS_KEY", [])

            if request.method in csrf_protected_methods:
                status = self.__protect_request()

                if not status:
                    abort(403)

    def __get_csrf_token_for_current_request(self):
        field_name = current_app.config.get(CSRF_TOKEN_FIELD_NAME_KEY)

        if not field_name:
            return None

        form_token = request.form.get(field_name)

        if form_token:
            return form_token

        return None

    def __protect_request(self):
        is_ok = False

        try:
            current_request_token = self.__get_csrf_token_for_current_request()
            self.validate_token(signed_token=current_request_token)

            is_ok = True

        except CSRFValidationException as e:
            current_app.logger.exception(e)

        return is_ok

    @staticmethod
    def generate_token():
        app_secret = str(current_app.secret_key)
        token_session_field_name = current_app.config.get(
            CSRF_TOKEN_FIELD_NAME_KEY, CSRF_TOKEN_FIELD_NAME)

        signer = URLSafeTimedSerializer(
            secret_key=app_secret, salt="io_remastered")

        new_token = secrets.token_hex(nbytes=32)
        setattr(session, token_session_field_name, new_token)

        return signer.dumps(new_token)

    @staticmethod
    def validate_token(signed_token: str | None):
        token_ttl = 600  # 10 mins
        app_secret = str(current_app.secret_key)

        session_csrf_token = session.get(CSRF_TOKEN_FIELD_NAME)

        if not session_csrf_token or not signed_token:
            raise CSRFValidationException("CSRF token is missing")

        signer = URLSafeTimedSerializer(
            secret_key=app_secret, salt="io_remastered")

        try:
            token = signer.loads(s=signed_token, max_age=token_ttl)

        except Exception as e:
            raise CSRFValidationException("CSRF token loading error") from e

        is_match = secrets.compare_digest(token, session_csrf_token)

        if not is_match:
            raise CSRFValidationException("CSRF tokens don't match")
