from db.models import DBDishIngredient
from db.repos.base import Repo


class DishIngredientRepo(Repo):
    __model__ = DBDishIngredient
