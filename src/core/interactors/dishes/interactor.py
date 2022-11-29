from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import DBDishDay, DBDishIngredient, DBDish
from db.repos.dish import DishRepo
from db.repos.dish_day import DishDayRepo
from db.repos.dish_ingredient import DishIngredientRepo

if TYPE_CHECKING:
    from api.graphql.schemas import GQAddDishDay, GQAddDishIngredient, GQUpdateDish, GQUpdateDishIngredient


async def create_day_with_dish(
        session: AsyncSession, dish_day_with_dish: GQAddDishDay, *, commit: bool = True
) -> DBDishDay:
    dish_day_repo = DishDayRepo(session)
    dish_repo = DishRepo(session)

    dish = await dish_repo.create(name=dish_day_with_dish.dish.name)
    dish_day = await dish_day_repo.create(
        day=dish_day_with_dish.day, user_code=dish_day_with_dish.user_code, dish_id=dish.id
    )
    dish_day.dish = dish

    if commit:
        await session.commit()
        await session.refresh(dish_day)

    return dish_day


async def delete_day_dish(session: AsyncSession, day_dish_id: uuid.UUID, *, commit: bool = True) -> None:
    dish_day_repo = DishDayRepo(session)
    dish_repo = DishRepo(session)
    dish_day: DBDishDay = await dish_day_repo.get_by_id(day_dish_id)
    await dish_day_repo.delete(day_dish_id)
    await dish_repo.delete(dish_day.dish_id)

    if commit:
        await session.commit()


async def delete_dish_ingredient(session: AsyncSession, dish_ingredient_id: uuid.UUID, *, commit: bool = True) -> None:
    dish_ingredient_repo = DishIngredientRepo(session)
    await dish_ingredient_repo.delete(dish_ingredient_id, commit=commit)


async def add_dish_ingredient(
        session: AsyncSession, dish_ingredient: GQAddDishIngredient, *, commit: bool = True
) -> DBDishIngredient:
    dish_ingredient_repo = DishIngredientRepo(session)
    return await dish_ingredient_repo.create(
        name=dish_ingredient.name,
        amount=dish_ingredient.amount,
        dish_id=dish_ingredient.dish_id,
        commit=commit
    )


async def update_dish(session: AsyncSession, dish: GQUpdateDish, *, commit: bool = True) -> DBDish:
    dish_repo = DishRepo(session)

    item: DBDish = await dish_repo.get_by_id(dish.id)
    item.name = dish.name
    item.url = dish.url
    item.description = dish.description

    session.add(item)
    if commit:
        await session.commit()

    return item


async def update_dish_ingredient(
        session: AsyncSession, dish_ingredient: GQUpdateDishIngredient, *, commit: bool = True
) -> DBDishIngredient:
    dish_ingredient_repo = DishIngredientRepo(session)

    item: DBDishIngredient = await dish_ingredient_repo.get_by_id(dish_ingredient.id)
    item.name = dish_ingredient.name
    item.amount = dish_ingredient.amount

    session.add(item)
    if commit:
        await session.commit()

    return item
