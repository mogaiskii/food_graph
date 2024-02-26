from db.models.poly.joined_magic import DBCarWheel as JoinedWheel, DBCarDoor as JoinedDoor, DBCarDetail as JoinedDetail
from db.models.poly.single_magic import DBCarWheel as SingleWheel, DBCarDoor as SingleDoor, DBCarDetail as SingleDetail
from db.repos.base import Repo


class JoinedCarDetailRepo(Repo):
    __model__ = JoinedDetail


class SingleCarDetailRepo(Repo):
    __model__ = SingleDetail


class JoinedCarWheelRepo(Repo):
    __model__ = JoinedWheel


class SingleCarWheelRepo(Repo):
    __model__ = SingleWheel


class JoinedDoorRepo(Repo):
    __model__ = JoinedDoor


class SingleDoorRepo(Repo):
    __model__ = SingleDoor
