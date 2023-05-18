import uuid
from datetime import date
from typing import List, Optional

from sqlalchemy.orm import load_only

from db.models import DBDishDay
from db.repos.base import Repo
from utils.gq_db_mapper import GQDBMapper


class DishDayRepo(Repo):
    __model__ = DBDishDay

    async def get_by_dates(
            self, date_from: date, date_to: date, user_code: uuid.UUID, mapper: Optional[GQDBMapper] = None
    ) -> List[DBDishDay]:
        stmt = (
            self.query
            .where(DBDishDay.day >= date_from)
            .where(DBDishDay.day <= date_to)
            .where(DBDishDay.user_code == user_code)
        )
        stmt = mapper.patch_statement(stmt)
        return await self.fetch_many(stmt)
