import datetime
import uuid
import json
from sqlalchemy import Integer, String, DATETIME, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from io_remastered.db import Base


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)

    username = mapped_column(String(20), unique=True, nullable=False)
    password = mapped_column(String, unique=False, nullable=False)

    created_at = mapped_column(
        DATETIME, nullable=False, default=lambda: datetime.datetime.now(datetime.timezone.utc))

    # max storage size in GB
    max_storage_size = mapped_column(
        Integer, unique=False, nullable=False, default=0)

    files = relationship("File", backref="owner",
                         cascade="all, delete-orphan", lazy=False)

    def __str__(self):
        struct = {
            "username": self.username,
            "created_at": str(self.created_at),
            "max_storage_size": self.max_storage_size,
            "files_count": len(self.files)
        }

        return json.dumps(struct)

    def get_max_storage_size_in_bytes(self):
        return self.max_storage_size * 1_000_000_000


class File(Base):
    __tablename__ = "files"

    id = mapped_column(Integer, primary_key=True)
    uuid = mapped_column(String(32), unique=True,
                         nullable=False, default=lambda: uuid.uuid4().hex)

    name = mapped_column(String(64), unique=False, nullable=False)
    extension = mapped_column(String(10), unique=False, nullable=False)

    size = mapped_column(Integer, unique=False, nullable=False, default=0)
    sha256_sum = mapped_column(String(64), unique=False, nullable=False)

    upload_date = mapped_column(
        DATETIME, nullable=False, default=lambda: datetime.datetime.now(datetime.timezone.utc))

    owner_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
