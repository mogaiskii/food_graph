import pytest
from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import DBUser


@pytest.fixture
def generate_user(db_session: AsyncSession):
    async def _user(username=None, password=None) -> DBUser:
        fake = Faker()
        if username is None:
            username = fake.user_name()
        if password is None:
            password = fake.password(length=15, special_chars=True, digits=True, upper_case=True, lower_case=True)

        user = DBUser(username=username)
        user.password = password
        db_session.add(user)
        await db_session.flush()
        await db_session.commit()

        return user
    return _user


@pytest.mark.asyncio
async def test_user_authorization(db_session: AsyncSession, generate_user):
    fake = Faker()
    password = fake.password(length=15, special_chars=True, digits=True, upper_case=True, lower_case=True)
    user = await generate_user(password=password)
    assert user.compare_password(password), "set password is recognizable as valid"


@pytest.mark.asyncio
async def test_user_change_password(db_session: AsyncSession, generate_user):
    fake = Faker()
    password = fake.password(length=15, special_chars=True, digits=True, upper_case=True, lower_case=True)

    user = await generate_user(password=password)

    new_password = fake.password(length=15, special_chars=True, digits=True, upper_case=True, lower_case=True)
    user.password = new_password

    assert not user.compare_password(password), "old password is not recognizable as valid"
    assert user.compare_password(new_password), "new password is recognizable as valid"

    await db_session.commit()
    assert user.compare_password(new_password), "new password is recognizable as valid after commit"
