import uuid
from datetime import date
from typing import Optional, List

import strawberry


class GQBase:
    pass


# @strawberry.type
# class GQRecipeIngredient(GQBase):



@strawberry.type
class GQDishIngredient(GQBase):
    id: uuid.UUID
    dish_id: uuid.UUID
    name: str
    amount: float


@strawberry.type
class GQDish(GQBase):
    id: uuid.UUID
    name: str
    ingredients: List[GQDishIngredient]
    description: Optional[str] = None
    url: Optional[str] = None


@strawberry.type
class GQDishDay(GQBase):
    id: uuid.UUID
    day: date
    user_code: uuid.UUID
    dish_id: uuid.UUID
    dish: GQDish


@strawberry.input
class GQAddDishInDay(GQBase):
    name: str


@strawberry.input
class GQAddDishDay(GQBase):
    day: date
    user_code: uuid.UUID
    dish: GQAddDishInDay


@strawberry.input
class GQUpdateDish(GQBase):
    id: uuid.UUID
    name: str
    description: Optional[str] = None
    url: Optional[str] = None


@strawberry.input
class GQAddDishIngredient(GQBase):
    name: str
    amount: float
    dish_id: uuid.UUID


@strawberry.input
class GQUpdateDishIngredient(GQBase):
    id: uuid.UUID
    name: str
    amount: float


@strawberry.type
class GQUser(GQBase):
    username: str


@strawberry.input
class GQCreateUser(GQBase):
    username: str
    password: str


@strawberry.type
class LoginSuccess(GQBase):
    user: GQUser
    token: str


@strawberry.type
class LoginError(GQBase):
    message: str


LoginResult = strawberry.union("LoginResult", (LoginSuccess, LoginError))


@strawberry.type
class GQAction(GQBase):
    name: str
