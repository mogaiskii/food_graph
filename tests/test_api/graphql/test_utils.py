import uuid
from datetime import date
from typing import List

import pytest

from api.graphql.schemas import GQDishIngredient, GQDishDay, GQUser
from api.graphql.utils import map_db_to_gq, map_response
from db.models import DBDishIngredient, DBDishDay, DBDish, DBUser


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


@pytest.mark.asyncio
async def test_map_response():
    @map_response
    def simple() -> GQUser:
        return DBUser(username='abc')

    @map_response(GQUser)
    def explicit(username):
        return DBUser(username=username)

    @map_response
    async def simple_list() -> List[GQUser]:
        return [DBUser(username='abc')]

    @map_response(GQUser)
    def explicit_list(username):
        return [DBUser(username=username)]

    class Handler:
        @map_response
        async def class_member(self, username) -> list[GQUser]:
            return [DBUser(username=username)]

    simple_result = simple()
    assert isinstance(simple_result, GQUser)
    assert simple_result.username == 'abc'
    assert explicit('abc').username == 'abc'
    simple_list_result = await simple_list()
    assert simple_list_result[0].username == 'abc'
    assert explicit_list('abc')[0].username == 'abc'
    handler = Handler()
    member_result = await handler.class_member('abc')
    assert member_result[0].username == 'abc'
