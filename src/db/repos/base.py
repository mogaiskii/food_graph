import uuid
from typing import List

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

from db.models import DBModel
from db.repos.exceptions import RepoNotFound, RepoManyForOne


class Repo:
    __model__ = DBModel

    def __init__(self, session: AsyncSession):
        self.session = session

    def build_item(self, **item_kwargs) -> DBModel:
        return self.__model__(**item_kwargs)

    async def create(self, *, flush: bool = True, commit: bool = False, **item_kwargs) -> DBModel:
        item = self.build_item(**item_kwargs)
        self.session.add(item)
        if flush:
            await self.session.flush([item])
        if commit:
            await self.session.commit()
        return item

    async def delete(self, id: uuid.UUID, *, commit: bool = False):
        statement = delete(self.__model__).where(self.__model__.id == id)
        await self.session.execute(statement)
        if commit:
            await self.session.commit()

    @property
    def query(self) -> Select:
        return select(self.__model__)

    async def fetch_one(self, statement: Select) -> DBModel:
        statement = statement.limit(2)
        result = await self.session.execute(statement)
        items = result.unique().scalars().all()
        if len(items) == 0:
            raise RepoNotFound
        if len(items) == 2:
            raise RepoManyForOne
        return items[0]

    async def fetch_many(self, statement: Select) -> List[DBModel]:
        result = await self.session.execute(statement)
        items = result.unique().scalars().all()
        return items

    async def get_by_id(self, id: uuid.UUID):
        stmt = self.query.where(self.__model__.id == id)
        return await self.fetch_one(stmt)
