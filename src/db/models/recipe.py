__all__ = ["DBRecipe"]

from sqlalchemy import String, Column, Text
from sqlalchemy.orm import relationship

from .recipe_ingredient import DBRecipeIngredient
from .base import DBModel


class DBRecipe(DBModel):
    __tablename__ = 'recipes'

    name = Column(String(256), nullable=False)
    description = Column(Text, nullable=True)
    url = Column(String(2048), nullable=True)

    ingredients = relationship(DBRecipeIngredient, lazy="joined")
