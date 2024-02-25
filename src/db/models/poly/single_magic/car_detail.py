from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from db.models import DBModel


class DBCarDetail(DBModel):
    __tablename__ = 'car_details'
    __table_args__ = {"schema": "single_magic"}

    name = Column(String(256), nullable=False)
    type = Column(String(256), nullable=False)  # wheel, door
    car_id = Column(UUID(as_uuid=True), ForeignKey("single_magic.cars.id"), nullable=True)
    __mapper_args__ = {
        "polymorphic_on": type,
        "polymorphic_identity": "car_details",
    }


class DBCarWheel(DBCarDetail):
    wheel_size = Column(Integer, nullable=True)  # only wheel
    __mapper_args__ = {
        "polymorphic_identity": "car_wheels",
    }


class DBCarDoor(DBCarDetail):
    door_type = Column(String(256), nullable=True)  # only door
    __mapper_args__ = {
        "polymorphic_identity": "car_doors",
    }

