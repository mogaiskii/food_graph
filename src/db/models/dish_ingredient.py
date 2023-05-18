__all__ = ["DBDishIngredient"]

from sqlalchemy import Column, ForeignKey, String, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from . import DBRecipeIngredient
from .base import DBModel


class DBDishIngredient(DBModel):
    __tablename__ = 'dish_ingredients'

    dish_id = Column(UUID(as_uuid=True), ForeignKey("dishes.id"))
    name = Column(String(256), nullable=False)
    amount = Column(Float, nullable=False)
    recipe_ingredient_id = Column(UUID(as_uuid=True), ForeignKey("recipe_ingredients.id"), nullable=True)

    recipe_ingredient = relationship(DBRecipeIngredient, uselist=False, lazy="joined")
