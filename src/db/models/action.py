__all__ = ["DBAction"]

from sqlalchemy import String, Column

from .base import DBModel


class DBAction(DBModel):
    __tablename__ = 'actions'

    name = Column(String(256), nullable=False)
