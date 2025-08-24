from typing import Self
from sqlalchemy import Select, func, select, ScalarResult
from sqlalchemy.orm import scoped_session, DeclarativeBase, Session


class Base(DeclarativeBase):
    @classmethod
    def get_db_session(cls) -> scoped_session[Session]:
        return None  # type: ignore

    @classmethod
    def select(cls) -> Select[tuple[Self]]:
        return select(cls)

    @classmethod
    def query(cls, select_exp: Select) -> ScalarResult[Self]:
        return cls.get_db_session().scalars(select_exp)

    @classmethod
    def count(cls, select_exp: Select) -> int | None:
        count = cls.get_db_session().scalar(
            select(func.count()).select_from(select_exp.subquery()))

        return count
