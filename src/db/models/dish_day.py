from sqlalchemy import Column, Date, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .dish import DBDish
from .base import DBModel


class DBDishDay(DBModel):
    __tablename__ = "dish_days"

    day = Column(Date, nullable=False, index=True)
    user_code = Column(UUID(as_uuid=True), nullable=False, index=True)
    dish_id = Column(UUID(as_uuid=True), ForeignKey("dishes.id"))

    dish = relationship(DBDish, uselist=False, lazy="joined")
