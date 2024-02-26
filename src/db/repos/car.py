from db.models.poly.joined_magic import DBCar as JoinedCar
from db.models.poly.single_magic import DBCar as SingleCar
from db.repos.base import Repo


class JoinedCarRepo(Repo):
    __model__ = JoinedCar


class SingleCarRepo(Repo):
    __model__ = SingleCar
