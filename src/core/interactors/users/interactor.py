from typing import Optional, Tuple

import jwt
from jwt import DecodeError
from sqlalchemy.ext.asyncio import AsyncSession

from core.interactors.users.exceptions import WrongAuthToken, UserNotFound
from db.models import DBUser
from db.repos.exceptions import RepoNotFound
from db.repos.user import UserRepo
from settings import settings


async def create_user(session: AsyncSession, username: str, password: str, *, commit: bool = True) -> DBUser:
    user_repo = UserRepo(session)

    return await user_repo.create(username=username, password=password, commit=commit)


async def authenticate_user(session: AsyncSession, username: str, password: str) -> Optional[Tuple[DBUser, str]]:
    user_repo = UserRepo(session)

    try:
        user = await user_repo.authenticate_user(username, password)
    except RepoNotFound:
        raise UserNotFound

    token = jwt.encode({"user_id": str(user.id)}, settings.secret, algorithm="HS256")

    return user, token


async def trial_user_token(session: AsyncSession, token: str) -> DBUser:
    if token is None:
        raise WrongAuthToken

    try:
        token_data = jwt.decode(token, settings.secret, algorithms=["HS256"])
    except DecodeError:
        raise WrongAuthToken

    user_repo = UserRepo(session)
    user_id = token_data['user_id']

    try:
        user = await user_repo.get_by_id(user_id)
    except RepoNotFound:
        raise WrongAuthToken

    return user
