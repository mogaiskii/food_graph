from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import AbstractConcreteBase

from db.models import DBModel, DBBase


class DBCarDetail(AbstractConcreteBase, DBModel):
    __abstract__ = True

    name = Column(String(256), nullable=False)
    type = Column(String(256), nullable=False)  # wheel, door
    car_id = Column(UUID(as_uuid=True), ForeignKey("concrete.cars.id"), nullable=True)


class DBCarWheel(DBCarDetail):
    __tablename__ = 'car_wheels'
    __table_args__ = {"schema": "concrete"}
    wheel_size = Column(Integer, nullable=True)  # only wheel
    __mapper_args__ = {
        "polymorphic_identity": "car_wheels",
        "concrete": True,
    }


class DBCarDoor(DBCarDetail):
    __tablename__ = 'car_doors'
    __table_args__ = {"schema": "concrete"}
    door_type = Column(String(256), nullable=True)  # only door
    __mapper_args__ = {
        "polymorphic_identity": "car_doors",
        "concrete": True,
    }

DBBase.registry.configure()
