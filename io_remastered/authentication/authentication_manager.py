import secrets
from uuid import uuid4
from dataclasses import dataclass
from datetime import datetime
from flask import g, session
from io_remastered import models
from io_remastered.extra_modules import RedisCacheDatabase


@dataclass
class AuthDbItem:
    created_at: str
    id: str


class AuthenticationManager:
    def __init__(self, auth_db: RedisCacheDatabase):
        self.__default_auth_token_ttl = 600

        self.__auth_db = auth_db

    def setup(self, default_auth_token_ttl: None | int = 600):
        if default_auth_token_ttl is not None:
            self.__default_auth_token_ttl = default_auth_token_ttl

    def get_auth_db_key_pattern(self, token: str | None = None, user_id: int | None = None):
        return f"user:{'*' if user_id is None else user_id}:{'*' if token is None else token}:"

    def login(self, user_id: int):
        token = secrets.token_hex(128)

        auth_db_key = self.get_auth_db_key_pattern(
            user_id=user_id, token=token)
        value = AuthDbItem(
            created_at=datetime.now().isoformat(), id=uuid4().hex)

        self.__auth_db.set_value(
            key=auth_db_key, value=value.__dict__, ttl=self.__default_auth_token_ttl)

        session["auth_token"] = token

    def refresh(self, token: str, user_id: int):
        auth_db_key = self.get_auth_db_key_pattern(
            user_id=user_id, token=token)
        self.__auth_db.update_ttl(
            key=auth_db_key, ttl=self.__default_auth_token_ttl)

    def logout(self):
        token = session.get("auth_token")

        if token is not None:
            self.__auth_db.delete_key(
                pattern=self.get_auth_db_key_pattern(token=token))
            session.pop("auth_token")

    def token_exists(self, token: str):
        key = self.__auth_db.get_value(
            pattern=self.get_auth_db_key_pattern(token=token))

        return True if key is not None else False

    @property
    def current_user(self) -> models.User:
        return g.get("current_user", None)

    def user_for_token(self, token: str | None) -> models.User | None:
        if not token:
            return None

        auth_key = self.__auth_db.get_key_for_pattern(
            pattern=self.get_auth_db_key_pattern(token=token))

        if not auth_key:
            return None

        user_id = int(auth_key.split(":")[1])

        user = models.User.query(
            models.User.select().filter_by(id=user_id)).first()

        return user

    def get_auth_token_for_current_session(self):
        return session.get("auth_token")

    def get_active_tokens_for_user(self, user_id: int):
        tokens = self.__auth_db.get_all_keys_for_pattern(
            pattern=self.get_auth_db_key_pattern(user_id=user_id))

        return tokens

    def get_user_sessions(self, user_id):
        keys = self.__auth_db.get_all_keys_for_pattern(
            pattern=self.get_auth_db_key_pattern(user_id=user_id))

        sessions = []

        for key in keys:
            data = self.__auth_db.get_value(key=key)
            ttl = self.__auth_db.get_ttl(key)

            if data:
                sessions.append({
                    "key": key,
                    "ttl": ttl,
                    "value": AuthDbItem(**data)
                })

        return sessions
