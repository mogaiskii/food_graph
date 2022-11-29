from db.models import DBDish
from db.repos.base import Repo


class DishRepo(Repo):
    __model__ = DBDish
