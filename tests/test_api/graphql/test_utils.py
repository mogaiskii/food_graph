import uuid
from datetime import date

from api.graphql.schemas import GQDishIngredient, GQDishDay
from api.graphql.utils import map_db_to_gq
from db.models import DBDishIngredient, DBDishDay, DBDish


def test_map_db_to_gq__simple():
    db_model = DBDishIngredient(dish_id=uuid.uuid4(), name="test", amount=1.2)
    result = map_db_to_gq(db_model, GQDishIngredient)
    assert result
    assert result.name == db_model.name
    assert result.amount == db_model.amount
    assert result.dish_id == db_model.dish_id


def test_map_db_to_gq__nested():
    dish_id = uuid.uuid4()
    db_ingredient = DBDishIngredient(dish_id=dish_id, name="test", amount=1.2)
    db_dish = DBDish(id=dish_id, name="dish name")
    db_dish.ingredients = [db_ingredient]
    db_dish_day = DBDishDay(user_code=str(uuid.uuid4()), day=date.today(), dish_id=dish_id)
    db_dish_day.dish = db_dish

    dish_day = map_db_to_gq(db_dish_day, GQDishDay)

    assert hasattr(dish_day, 'dish')
    dish = dish_day.dish

    assert hasattr(dish, 'ingredients')
    ingredients = dish.ingredients

    assert len(ingredients)
    ingredient = ingredients[0]

    assert ingredient.name == db_ingredient.name
