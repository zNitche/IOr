import datetime
import uuid
from sqlalchemy import Integer, String, DATETIME, ForeignKey
from sqlalchemy.orm import mapped_column, relationship
from io_remastered.db import Base


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)

    username = mapped_column(String(20), unique=True, nullable=False)
    password = mapped_column(String(), unique=False, nullable=False)

    created_at = mapped_column(
        DATETIME, nullable=False, default=lambda: datetime.datetime.now(datetime.timezone.utc))

    # max storage size in GB
    max_storage_size = mapped_column(
        Integer, unique=False, nullable=False, default=0)

    files = relationship("File", backref="owner",
                         cascade="all, delete-orphan", lazy=False)


class File(Base):
    __tablename__ = "files"

    id = mapped_column(Integer, primary_key=True)
    uuid = mapped_column(String(32), unique=True,
                         nullable=False, default=lambda: uuid.uuid4().hex)

    owner_id = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
