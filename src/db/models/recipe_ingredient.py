__all__ = ["DBRecipeIngredient"]

from sqlalchemy import Column, ForeignKey, String, Float
from sqlalchemy.dialects.postgresql import UUID

from .base import DBModel


class DBRecipeIngredient(DBModel):
    __tablename__ = 'recipe_ingredients'

    recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.id"))
    name = Column(String(256), nullable=False)
    amount = Column(Float, nullable=False)
