import asyncio
import sys

import pytest
from faker import Faker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import DBBase, DBUser
from settings import settings


@pytest.fixture(scope="session")
def fake():
    return Faker()


@pytest.fixture(scope="session")
def event_loop():
    """
    Creates an instance of the default event loop for the test session.
    """
    if sys.platform.startswith("win") and sys.version_info[:2] >= (3, 8):
        # Avoid "RuntimeError: Event loop is closed" on Windows when tearing down tests
        # https://github.com/encode/httpx/issues/914
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def _database_url():
    return settings.get_db_url()


@pytest.fixture(scope="session")
def init_database():
    return DBBase.metadata.create_all


@pytest.fixture
def generate_user(db_session: AsyncSession, fake):
    async def _user(username=None, password=None) -> DBUser:
        if username is None:
            username = fake.user_name()
        if password is None:
            password = fake.password(length=15, special_chars=True, digits=True, upper_case=True, lower_case=True)

        user = DBUser(username=username)
        user.password = password
        db_session.add(user)
        await db_session.flush(objects=[user])
        await db_session.commit()

        return user
    return _user
