from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import mapped_column
from io_remastered.db import Base


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(128), unique=False, nullable=False)
