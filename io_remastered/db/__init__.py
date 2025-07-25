from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

from io_remastered.db.database import Database
from io_remastered.db.pagination import Pagination
