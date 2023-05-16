__all__ = ['Query', 'schema', 'graphql_app']

import datetime
import uuid
from typing import List

import strawberry
from strawberry import Schema
from strawberry.extensions import Extension
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info

from app import SessionMaker
from core.interactors.dishes.interactor import (
    create_day_with_dish, delete_day_dish, delete_dish_ingredient,
    add_dish_ingredient, update_dish, update_dish_ingredient,
)
from core.interactors.users.exceptions import UserNotFound
from core.interactors.users.interactor import authenticate_user, create_user
from db.repos.dish_day import DishDayRepo
from .permissions import IsAuthenticated
from .schemas import GQDishDay, GQAddDishDay, GQUpdateDish, GQAddDishIngredient, GQUpdateDishIngredient, \
    GQDishIngredient, GQDish, LoginResult, LoginError, LoginSuccess, GQUser, GQCreateUser
from .utils import map_db_to_gq


class SQLAlchemySession(Extension):
    def on_request_start(self):
        self.execution_context.context["db"] = SessionMaker()

    async def on_request_end(self):
        await self.execution_context.context["db"].close()


@strawberry.type
class Query:
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def plan(
            self, info: Info, date_from: datetime.date, date_to: datetime.date, user_code: uuid.UUID
    ) -> List[GQDishDay]:
        items = await DishDayRepo(info.context["db"]).get_by_dates(date_from, date_to, user_code)
        return items
        # return [map_db_to_gq(item, GQDishDay) for item in items]


@strawberry.type
class Mutation:
    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def add_day_dish(self, info: Info, day_dish: GQAddDishDay) -> GQDishDay:
        item = await create_day_with_dish(info.context["db"], day_dish)
        return map_db_to_gq(item, GQDishDay)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def add_dish_ingredient(
            self, info: Info, dish_ingredient: GQAddDishIngredient
    ) -> GQDishIngredient:
        item = await add_dish_ingredient(info.context["db"], dish_ingredient)
        return map_db_to_gq(item, GQDishIngredient)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def update_dish(self, info: Info, dish: GQUpdateDish) -> GQDish:
        item = await update_dish(info.context["db"], dish)
        return map_db_to_gq(item, GQDish)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def update_dish_ingredient(
            self, info: Info, dish_ingredient: GQUpdateDishIngredient
    ) -> GQDishIngredient:
        item = await update_dish_ingredient(info.context["db"], dish_ingredient)
        return map_db_to_gq(item, GQDishIngredient)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def remove_day_dish(self, info: Info, id: uuid.UUID) -> None:
        await delete_day_dish(info.context["db"], id)

    @strawberry.mutation(permission_classes=[IsAuthenticated])
    async def remove_dish_ingredient(self, info: Info, id: uuid.UUID) -> None:
        await delete_dish_ingredient(info.context["db"], id)

    @strawberry.mutation
    async def create_user(self, info: Info, user: GQCreateUser) -> GQUser:
        item = await create_user(info.context["db"], user.username, user.password)
        return map_db_to_gq(item, GQUser)

    @strawberry.field
    async def login(self, info: Info, username: str, password: str) -> LoginResult:
        try:
            user, token = await authenticate_user(info.context["db"], username, password)
        except UserNotFound:
            return LoginError(message="Login failed")

        return LoginSuccess(user=map_db_to_gq(user, GQUser), token=token)


schema = Schema(Query, mutation=Mutation, extensions=[SQLAlchemySession])
graphql_app = GraphQLRouter(schema)
