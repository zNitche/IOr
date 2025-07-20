import secrets
from flask import g, session
from io_remastered import models
from io_remastered.extra_modules import RedisCacheDatabase


class AuthenticationManager:
    def __init__(self, auth_db: RedisCacheDatabase):
        self.__auth_db = auth_db

    def login(self, user_id: int):
        token = secrets.token_hex(128)
        self.__auth_db.set_value(token, user_id, ttl=600)

        session["auth_token"] = token

    def refresh(self, token: str, time=600):
        self.__auth_db.update_ttl(token, ttl=time)

    def logout(self):
        token = session.get("auth_token")

        if token is not None:
            self.__auth_db.delete_key(token)
            session.pop("auth_token")

    def token_exists(self, token: str):
        user_id = self.__auth_db.get_value(token)

        return True if user_id is not None else False

    @property
    def current_user(self) -> models.User:
        user = g.get("current_user", None)

        if not user:
            raise Exception("current user is none")
        
        return user

    def user_for_token(self, token: str | None) -> models.User | None:
        if not token:
            return None

        user_id = self.__auth_db.get_value(token)

        if user_id is None:
            return None

        return models.User.query.filter_by(id=user_id).first()

    def get_auth_token_for_current_session(self):
        return session.get("auth_token")
