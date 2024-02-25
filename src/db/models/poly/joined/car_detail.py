from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from db.models import DBModel


class DBCarWheel(DBModel):
    __tablename__ = 'car_wheels'
    __table_args__ = {"schema": "joint"}
    car_detail_id = Column(UUID(as_uuid=True), ForeignKey("joint.car_details.id"), nullable=True)
    wheel_size = Column(Integer, nullable=True)  # only wheel


class DBCarDoor(DBModel):
    __tablename__ = 'car_doors'
    __table_args__ = {"schema": "joint"}
    car_detail_id = Column(UUID(as_uuid=True), ForeignKey("joint.car_details.id"), nullable=True)
    door_type = Column(String(256), nullable=True)  # only door



class DBCarDetail(DBModel):
    __tablename__ = 'car_details'
    __table_args__ = {"schema": "joint"}

    name = Column(String(256), nullable=False)
    type = Column(String(256), nullable=False)  # wheel, door
    car_id = Column(UUID(as_uuid=True), ForeignKey("joint.cars.id"), nullable=True)

    wheel = relationship("DBCarWheel", backref="car_detail", uselist=False, lazy='joined')  # always joined! // or additional magic in gql mapper
    door = relationship("DBCarDoor", backref="car_detail", uselist=False, lazy='joined')  # always joined! // or additional magic in gql mapper

    @property
    def info(self):
        if self.type == 'wheel':
            return self.wheel
        elif self.type == 'door':
            return self.door
        else:
            return None
