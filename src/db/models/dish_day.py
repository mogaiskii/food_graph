from sqlalchemy import Column, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.db.models.base import DBModel


class DBDishDay(DBModel):
    __tablename__ = "dish_days"

    day = Column(Date, nullable=False, index=True)
    user_code = Column(UUID, nullable=False, index=True)
    dish_id = Column(UUID, ForeignKey("dishes.id"))

    dish = relationship("Dish", uselist=False)
