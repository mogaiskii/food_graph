import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from db.models import DBAction
from db.repos.actions import ActionsRepo


async def get_updates(session: AsyncSession, min_date: datetime.datetime) -> list[DBAction]:
    repo = ActionsRepo(session)
    return await repo.get_by_min_date(min_date)


async def create_action(session: AsyncSession, name: str) -> DBAction:
    repo = ActionsRepo(session)
    return await repo.create(commit=True, name=name)
