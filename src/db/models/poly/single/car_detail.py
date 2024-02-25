from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from db.models import DBModel


class DBCarDetail(DBModel):
    __tablename__ = 'car_details'
    __table_args__ = {"schema": "single"}

    name = Column(String(256), nullable=False)
    type = Column(String(256), nullable=False)  # wheel, door
    door_type = Column(String(256), nullable=True)  # only door
    wheel_size = Column(Integer, nullable=True)  # only wheel
    car_id = Column(UUID(as_uuid=True), ForeignKey("single.cars.id"), nullable=True)
