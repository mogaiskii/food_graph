import uuid
from datetime import date

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import DBDish, DBDishIngredient, DBDishDay


@pytest.fixture
async def dish_day__full(db_session: AsyncSession):
    async with db_session.begin():
        dish = DBDish(name="dish name")
        db_session.add(dish)
        await db_session.flush()

        ingredient_1 = DBDishIngredient(dish_id=dish.id, name="ingredient 1", amount=1.0)
        ingredient_2 = DBDishIngredient(dish_id=dish.id, name="ingredient 2", amount=0.1)
        dish_day = DBDishDay(user_code=str(uuid.uuid4()), day=date.today(), dish_id=dish.id)
        db_session.add_all([
            ingredient_1,
            ingredient_2,
            dish_day
        ])
        await db_session.flush()
        await db_session.commit()

    return dish_day


@pytest.mark.asyncio
async def test_complex_scenario(db_session: AsyncSession, dish_day__full: DBDishDay):
    async with db_session.begin():
        stmt = select(DBDishDay).where(DBDishDay.id == dish_day__full.id)
        result = await db_session.execute(stmt)
        dish_day: DBDishDay = result.scalars().first()

        dish: DBDish = dish_day.dish

        ingredients: list[DBDishIngredient] = dish.ingredients

        assert len(ingredients) == 2
