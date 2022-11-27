__all__ = ["DBDish"]

from sqlalchemy import String, Column, Text
from sqlalchemy.orm import relationship

from .base import DBModel


class DBDish(DBModel):
    __tablename__ = 'dishes'

    name = Column(String(256), nullable=False)
    description = Column(Text, nullable=True)
    url = Column(String(2048), nullable=True)

    ingredients = relationship("DBDishIngredient")
