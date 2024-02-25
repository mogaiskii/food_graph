from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID

from db.models import DBModel



class DBCarDetail(DBModel):
    __table_args__ = {"schema": "naive"}
    __abstract__ = True

    name = Column(String(256), nullable=False)
    type = Column(String(256), nullable=False)  # wheel, door
    car_id = Column(UUID(as_uuid=True), ForeignKey("naive.cars.id"), nullable=True)


class DBCarWheel(DBCarDetail):
    __tablename__ = 'car_wheels'
    __table_args__ = {"schema": "naive"}
    wheel_size = Column(Integer, nullable=True)  # only wheel


class DBCarDoor(DBCarDetail):
    __tablename__ = 'car_doors'
    __table_args__ = {"schema": "naive"}
    door_type = Column(String(256), nullable=True)  # only door

