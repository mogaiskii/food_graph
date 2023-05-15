from db.models import DBUser
from db.repos.base import Repo
from db.repos.exceptions import RepoNotFound


class UserRepo(Repo):
    __model__ = DBUser

    async def get_by_username(self, username: str) -> DBUser:
        stmt = self.query.where(DBUser.username == username)
        return await self.fetch_one(stmt)

    async def authenticate_user(self, username: str, password: str) -> DBUser:
        user = await self.get_by_username(username)

        if not user.compare_password(password):
            raise RepoNotFound

        return user

    async def create(
            self, *, username: str, password: str, flush: bool = True, commit: bool = False, **kwargs
    ) -> DBUser:
        user = DBUser(username=username)
        user.password = password
        return await self.save(user, flush=flush, commit=commit)
