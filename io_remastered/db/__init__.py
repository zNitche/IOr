from sqlalchemy.orm import declarative_base

Base = declarative_base()

from io_remastered.db.database import Database
from io_remastered.db.pagination import Pagination
