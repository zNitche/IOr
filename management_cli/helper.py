import os
import shutil
from typing import Any
from werkzeug.security import generate_password_hash
from config.app_config import AppConfig
from io_remastered import models
from io_remastered.db import Database


class Helper:
    def __init__(self):
        self.db = Database()
        self.db.setup(db_uri=AppConfig.DATABASE_URI)

        self.db.create_all()

    def get_users(self) -> list[models.User]:
        users = list(models.User.query(models.User.select()).unique().all())

        return users

    def get_user(self, user_name: str) -> models.User | None:
        user = models.User.query(
            models.User.select().filter_by(username=user_name)).first()

        return user

    def get_file(self, file_uuid: str) -> models.File | None:
        file = models.File.query(
            models.File.select().filter_by(uuid=file_uuid)).first()

        return file

    def __hash_password(self, plain_password: str):
        return generate_password_hash(plain_password, salt_length=32)

    def add_user(self, user_name: str, password: str, storage_size: int):
        users_names = [user.username for user in self.get_users()]

        if user_name in users_names:
            raise Exception("user already exists")

        encrypted_password = self.__hash_password(password)
        user = models.User(
            username=user_name, password=encrypted_password, max_storage_size=storage_size)

        self.db.add(user)

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
        user = self.get_user(user_name)

        if user is None:
            raise Exception("user doesn't exists")

        self.db.remove(user)

        self.__remove_user_storage_directory(user.id)

    def reset_user_password(self, user_name: str, password: str):
        user = self.get_user(user_name)

        if not user:
            raise Exception("user doesn't exists")

        encrypted_password = self.__hash_password(password)
        user.password = encrypted_password

        self.db.commit()

    def change_user_max_storage_size(self, user_name: str, storage_size: int):
        user = self.get_user(user_name)

        if not user:
            raise Exception("user doesn't exists")

        user.max_storage_size = storage_size
        self.db.commit()

    def remove_file(self, user_id: str, file_uuid: str):
        file = self.get_file(file_uuid)

        if not file:
            raise Exception("file doesn't exists")

        self.db.remove(file)

        file_path = os.path.join(
            AppConfig.STORAGE_ROOT_PATH, str(user_id), file_uuid)

        if os.path.exists(file_path):
            os.remove(file_path)

    def cleanup_db_object(self, object: Any):
        struct = {}
        dict = object.__dict__

        for key in dict:
            if not key.startswith("_"):
                struct[key] = dict.get(key)

        return struct
