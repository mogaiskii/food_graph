__all__ = ["DBDish"]

from sqlalchemy import String, Column, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from . import DBUser
from .recipe import DBRecipe
from .dish_ingredient import DBDishIngredient
from .base import DBModel


class DBDish(DBModel):
    __tablename__ = 'dishes'

    name = Column(String(256), nullable=False)
    description = Column(Text, nullable=True)
    url = Column(String(2048), nullable=True)
    recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.id"), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    ingredients = relationship(DBDishIngredient, lazy="joined")
    recipe = relationship(DBRecipe, uselist=False)
    user = relationship(DBUser, uselist=False)
