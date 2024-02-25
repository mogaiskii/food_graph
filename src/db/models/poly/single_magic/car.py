from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from db.models import DBModel
from .car_detail import DBCarDetail


class DBCar(DBModel):
    __tablename__ = 'cars'
    __table_args__ = {"schema": "single_magic"}

    name = Column(String(256), nullable=False)

    details = relationship(DBCarDetail, lazy="joined")
