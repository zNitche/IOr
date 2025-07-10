from io_remastered import models
from io_remastered.db import Database
from config.app_config import AppConfig
from werkzeug.security import generate_password_hash


class Helper:
    def __init__(self):
        self.db = Database()
        self.db.setup(db_uri=AppConfig.DATABASE_URI)

    def get_users_names(self):
        names = []

        with self.db.session_context() as session:
            users = session.query(models.User).all()

            for user in users:
                names.append(user.username)

        return names

    def hash_password(self, plain_password):
        password = generate_password_hash(plain_password)

        return password

    def add_user(self, user_name, password):
        if user_name in self.get_users_names():
            raise Exception("user already exists")

        encrypted_password = self.hash_password(password)
        user = models.User(username=user_name, password=encrypted_password)

        with self.db.session_context() as session:
            session.add(user)
            session.commit()

    def delete_user(self, user_name):
        with self.db.session_context() as session:
            user = session.query(models.User).filter_by(
                username=user_name).first()

            if user is None:
                raise Exception("user doesn't exists")

            session.delete(user)
            session.commit()

    def reset_user_password(self, user_name, password):
        with self.db.session_context() as session:
            user = session.query(models.User).filter_by(
                username=user_name).first()

            if not user:
                raise Exception("user doesn't exists")

            user.password = self.hash_password(password)
            session.commit()
