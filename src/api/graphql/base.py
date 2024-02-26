__all__ = ['Query', 'schema', 'graphql_app']

import asyncio
import datetime
import uuid
from typing import List, AsyncGenerator

import strawberry
from strawberry import Schema
from strawberry.extensions import Extension
from strawberry.fastapi import GraphQLRouter
from strawberry.subscriptions import GRAPHQL_TRANSPORT_WS_PROTOCOL, GRAPHQL_WS_PROTOCOL
from strawberry.types import Info

from app import SessionMaker
from core.interactors.actions.interactor import get_updates, create_action
from core.interactors.dishes.interactor import (
    create_day_with_dish, delete_day_dish, delete_dish_ingredient,
    add_dish_ingredient, update_dish, update_dish_ingredient,
)
from core.interactors.users.exceptions import UserNotFound
from core.interactors.users.interactor import authenticate_user, create_user
from db.models import DBDishDay, DBCar, DBCarDetail
from db.repos.car import SingleCarRepo, JoinedCarRepo
from db.repos.car_details import JoinedCarDetailRepo, SingleCarDetailRepo
from db.repos.dish_day import DishDayRepo
from utils.gq_db_mapper import GQDBMapper
from .permissions import IsAuthenticated
from .schemas import GQDishDay, GQAddDishDay, GQUpdateDish, GQAddDishIngredient, GQUpdateDishIngredient, \
    GQDishIngredient, GQDish, LoginResult, LoginError, LoginSuccess, GQUser, GQCreateUser, GQAction, Car, CarDetail, \
    CarWheel, CarDoor
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
        mapper = GQDBMapper(info, DBDishDay)
        items = await DishDayRepo(info.context["db"]).get_by_dates(date_from, date_to, user_code, mapper)
        return items
        # return [map_db_to_gq(item, GQDishDay) for item in items]

    @strawberry.field
    async def joined_cars(self, info: Info) -> List[Car]:
        mapper = GQDBMapper(info, DBCar)
        items = await JoinedCarRepo(info.context["db"]).get_all(mapper=mapper)
        return items

    @strawberry.field
    async def single_cars(self, info: Info) -> List[Car]:
        mapper = GQDBMapper(info, DBCar)
        items = await SingleCarRepo(info.context["db"]).get_all(mapper=mapper)
        return items

    @strawberry.field
    async def joined_details(self, info: Info) -> List[CarDetail]:
        mapper = GQDBMapper(info, DBCarDetail)
        items = await JoinedCarDetailRepo(info.context["db"]).get_all(mapper=mapper)
        return items

    @strawberry.field
    async def single_details(self, info: Info) -> List[CarDetail]:
        mapper = GQDBMapper(info, DBCarDetail)
        items = await SingleCarDetailRepo(info.context["db"]).get_all(mapper=mapper)
        return items


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

    @strawberry.mutation
    async def create_action(self, info: Info, name: str) -> GQAction:
        return await create_action(info.context['db'], name)


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def count(self, target: int = 100) -> int:
        for i in range(target):
            yield i
            await asyncio.sleep(0.5)

    @strawberry.subscription
    async def live_actions(self, info: Info) -> AsyncGenerator[List[GQAction], None]:
        min_date = datetime.datetime.now()
        session = None
        try:
            session = SessionMaker()
            while True:
                print(min_date)
                updates = await get_updates(session, min_date)  # TODO: why did the context[db] disappeared?
                if updates:
                    min_date = datetime.datetime.now()
                    yield updates
                await asyncio.sleep(1)
        finally:
            if session:
                await session.close()


schema = Schema(Query, mutation=Mutation, subscription=Subscription, extensions=[SQLAlchemySession],
                types=[CarWheel, CarDoor])
graphql_app = GraphQLRouter(
    schema,
    subscription_protocols=[
        GRAPHQL_TRANSPORT_WS_PROTOCOL,
        GRAPHQL_WS_PROTOCOL,
    ],
)
