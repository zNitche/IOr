from sqlalchemy import Integer, String, DATETIME
from sqlalchemy.orm import mapped_column
import datetime
from io_remastered.db import Base


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)

    username = mapped_column(String(20), unique=True, nullable=False)
    password = mapped_column(String(), unique=False, nullable=False)

    created_at = mapped_column(
        DATETIME, nullable=False, default=lambda: datetime.datetime.now(datetime.timezone.utc))

    # max storage size in GB 
    max_storage_size = mapped_column(Integer, unique=False, nullable=False, default=0)
