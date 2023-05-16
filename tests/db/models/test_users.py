import pytest
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_user_auth(db_session: AsyncSession, generate_user, fake):
    password = fake.password(length=15, special_chars=True, digits=True, upper_case=True, lower_case=True)
    user = await generate_user(password=password)
    assert user.compare_password(password), "set password is recognizable as valid"


@pytest.mark.asyncio
async def test_user_change_password(db_session: AsyncSession, generate_user, fake):
    password = fake.password(length=15, special_chars=True, digits=True, upper_case=True, lower_case=True)

    user = await generate_user(password=password)

    new_password = fake.password(length=15, special_chars=True, digits=True, upper_case=True, lower_case=True)
    user.password = new_password

    assert not user.compare_password(password), "old password is not recognizable as valid"
    assert user.compare_password(new_password), "new password is recognizable as valid"

    await db_session.commit()
    assert user.compare_password(new_password), "new password is recognizable as valid after commit"
