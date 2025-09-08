import secrets
from datetime import datetime
from flask import g, session
from io_remastered import models
from io_remastered.extra_modules import RedisCacheDatabase


class AuthenticationManager:
    def __init__(self, auth_db: RedisCacheDatabase):
        self.__default_auth_token_ttl = 600

        self.__auth_db = auth_db

    def setup(self, default_auth_token_ttl: None | int = 600):
        if default_auth_token_ttl is not None:
            self.__default_auth_token_ttl = default_auth_token_ttl

    def get_auth_db_key(self, user_id: int | str, token: str):
        return f"user:{user_id}:{token}:"

    def get_auth_db_token_key_pattern(self, token: str):
        return f"user:*:{token}:"

    def login(self, user_id: int):
        token = secrets.token_hex(128)
        now = datetime.now().isoformat()

        auth_db_key = self.get_auth_db_key(user_id=user_id, token=token)

        self.__auth_db.set_value(
            key=auth_db_key, value=now, ttl=self.__default_auth_token_ttl)

        session["auth_token"] = token

    def refresh(self, token: str, user_id: int):
        auth_db_key = self.get_auth_db_key(user_id=user_id, token=token)
        self.__auth_db.update_ttl(
            key=auth_db_key, ttl=self.__default_auth_token_ttl)

    def logout(self):
        token = session.get("auth_token")

        if token is not None:
            self.__auth_db.delete_key(
                pattern=self.get_auth_db_token_key_pattern(token))
            session.pop("auth_token")

    def token_exists(self, token: str):
        key = self.__auth_db.get_value(
            pattern=self.get_auth_db_token_key_pattern(token))

        return True if key is not None else False

    @property
    def current_user(self) -> models.User:
        return g.get("current_user", None)

    def user_for_token(self, token: str | None) -> models.User | None:
        if not token:
            return None

        auth_key = self.__auth_db.get_key_for_pattern(
            pattern=self.get_auth_db_token_key_pattern(token))

        if not auth_key:
            return None

        user_id = int(auth_key.replace(f":{token}:", "").replace("user:", ""))

        user = models.User.query(
            models.User.select().filter_by(id=user_id)).first()

        return user

    def get_auth_token_for_current_session(self):
        return session.get("auth_token")

    def get_active_tokens_for_user(self, user_id: int):
        tokens = self.__auth_db.get_all_keys_for_pattern(
            pattern=f"user:{user_id}:*:")

        return tokens
