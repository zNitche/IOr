from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column
from io_remastered.db import Base


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(20), unique=True, nullable=False)
    password = mapped_column(String(), unique=False, nullable=False)
