import uuid
from datetime import date
from typing import List

from db.models import DBDishDay
from db.repos.base import Repo


class DishDayRepo(Repo):
    __model__ = DBDishDay

    async def get_by_dates(self, date_from: date, date_to: date, user_code: uuid.UUID) -> List[DBDishDay]:
        stmt = (
            self.query
            .where(DBDishDay.day >= date_from)
            .where(DBDishDay.day <= date_to)
            .where(DBDishDay.user_code == user_code)
        )
        return await self.fetch_many(stmt)
