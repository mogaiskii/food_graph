from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from db.models import DBModel
from .car_detail import DBCarWheel, DBCarDoor


class DBCar(DBModel):
    __tablename__ = 'cars'
    __table_args__ = {"schema": "naive"}

    name = Column(String(256), nullable=False)

    wheels = relationship(DBCarWheel, lazy="joined")
    doors = relationship(DBCarDoor, lazy="joined")
