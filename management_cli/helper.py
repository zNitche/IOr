from io_remastered import models
from io_remastered.db import Database
import os
import shutil
from config.app_config import AppConfig
from werkzeug.security import generate_password_hash


class Helper:
    def __init__(self):
        self.db = Database()
        self.db.setup(db_uri=AppConfig.DATABASE_URI)

    def get_users(self):
        with self.db.session_context() as session:
            users = session.query(models.User).all()

        return users

    def __hash_password(self, plain_password: str):
        return generate_password_hash(plain_password)

    def add_user(self, user_name: str, password: str, storage_size: int):
        users_names = [user.username for user in self.get_users()]

        if user_name in users_names:
            raise Exception("user already exists")

        encrypted_password = self.__hash_password(password)
        user = models.User(
            username=user_name, password=encrypted_password, max_storage_size=storage_size)

        with self.db.session_context() as session:
            session.add(user)
            session.commit()

            self.__create_user_storage_directory(user_id=user.id)

    def __create_user_storage_directory(self, user_id: str):
        storage_path = os.path.join(
            AppConfig.STORAGE_ROOT_PATH, str(user_id))

        if not os.path.exists(storage_path):
            os.mkdir(storage_path)

    def __remove_user_storage_directory(self, user_id: str):
        storage_path = os.path.join(
            AppConfig.STORAGE_ROOT_PATH, str(user_id))

        if os.path.exists(storage_path):
            shutil.rmtree(storage_path)

    def delete_user(self, user_name: str):
        with self.db.session_context() as session:
            user = session.query(models.User).filter_by(
                username=user_name).first()

            if user is None:
                raise Exception("user doesn't exists")

            session.delete(user)
            session.commit()

            self.__remove_user_storage_directory(user.id)

    def reset_user_password(self, user_name: str, password: str):
        with self.db.session_context() as session:
            user = session.query(models.User).filter_by(
                username=user_name).first()

            if not user:
                raise Exception("user doesn't exists")

            user.password = self.__hash_password(password)
            session.commit()

    def change_user_max_storage_size(self, user_name: str, storage_size: int):
        with self.db.session_context() as session:
            user = session.query(models.User).filter_by(
                username=user_name).first()

            if not user:
                raise Exception("user doesn't exists")

            user.max_storage_size = storage_size
            session.commit()
