__all__ = ["DBDishIngredient"]

from sqlalchemy import Column, ForeignKey, String, Float
from sqlalchemy.dialects.postgresql import UUID

from .base import DBModel


class DBDishIngredient(DBModel):
    __tablename__ = 'dish_ingredients'

    dish_id = Column(UUID(as_uuid=True), ForeignKey("dishes.id"))
    name = Column(String(256), nullable=False)
    amount = Column(Float, nullable=False)
