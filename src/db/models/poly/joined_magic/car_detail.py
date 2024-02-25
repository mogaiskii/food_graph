from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.models import DBModel


class DBCarDetail(DBModel):
    __tablename__ = 'car_details'
    __table_args__ = {"schema": "joint_magic"}

    name = Column(String(256), nullable=False)
    type = Column(String(256), nullable=False)  # wheel, door
    car_id = Column(UUID(as_uuid=True), ForeignKey("joint_magic.cars.id"), nullable=True)
    __mapper_args__ = {
        "polymorphic_identity": "car_details",
        "polymorphic_on": type,
    }


class DBCarWheel(DBCarDetail):
    __tablename__ = 'car_wheels'
    __table_args__ = {"schema": "joint_magic"}
    wheel_size = Column(Integer, nullable=True)  # only wheel
    __mapper_args__ = {
        "polymorphic_identity": "car_wheels",
    }


class DBCarDoor(DBCarDetail):
    __tablename__ = 'car_doors'
    __table_args__ = {"schema": "joint_magic"}
    door_type = Column(String(256), nullable=True)  # only door
    __mapper_args__ = {
        "polymorphic_identity": "car_doors",
    }


