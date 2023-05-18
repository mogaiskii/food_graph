import datetime

from db.models import DBAction
from db.repos.base import Repo


class ActionsRepo(Repo):
    __model__ = DBAction

    async def get_by_min_date(self, min_date: datetime.datetime) -> list[DBAction]:
        stmt = self.query.where(DBAction.created_at >= min_date)
        return await self.fetch_many(stmt)
