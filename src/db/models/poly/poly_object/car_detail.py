from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declared_attr

from db.models import DBModel


class DBCarDetailBase(DBModel):
    __table_args__ = {"schema": "poly_object"}
    __abstract__ = True

    name = Column(String(256), nullable=False)
    type = Column(String(256), nullable=False)  # wheel, door
    # car_detail_id = Column(UUID(as_uuid=True), ForeignKey("poly_object.car_details.id"), nullable=True)
    @declared_attr
    def car_detail_id(cls):
        return Column(UUID(as_uuid=True), ForeignKey("poly_object.car_details.id"), nullable=True)


class DBCarWheel(DBCarDetailBase):
    __tablename__ = 'car_wheels'
    __table_args__ = {"schema": "poly_object"}
    wheel_size = Column(Integer, nullable=True)  # only wheel


class DBCarDoor(DBCarDetailBase):
    __tablename__ = 'car_doors'
    __table_args__ = {"schema": "poly_object"}
    door_type = Column(String(256), nullable=True)  # only door


class DBCarDetail(DBModel):
    __table_args__ = {"schema": "poly_object"}
    __tablename__ = 'car_details'
    # car_id = Column(UUID(as_uuid=True), ForeignKey("poly_object.cars.id"), nullable=True)
    @declared_attr
    def car_id(cls):
        return Column(UUID(as_uuid=True), ForeignKey("poly_object.cars.id"), nullable=True)

    wheels = relationship(DBCarWheel, lazy="joined")
    doors = relationship(DBCarDoor, lazy="joined")
