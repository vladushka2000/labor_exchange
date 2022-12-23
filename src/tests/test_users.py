import pytest
from pydantic import ValidationError

from faker import Faker
from fixtures.users import UserFactory
from queries import user as user_query
from schemas import UserInSchema


@pytest.mark.asyncio
async def test_get_all_users(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    all_users = await user_query.get_all(sa_session)
    assert all_users
    assert len(all_users) == 1
    assert all_users[0] == user


@pytest.mark.asyncio
async def test_get_user_by_id(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    await sa_session.flush()

    current_user = await user_query.get_by_id(sa_session, user.id)
    assert current_user is not None
    assert current_user.id == user.id


@pytest.mark.asyncio
async def test_get_user_by_email(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    current_user = await user_query.get_by_email(sa_session, user.email)
    assert current_user is not None
    assert current_user.id == user.id


@pytest.mark.asyncio
async def test_create_user(sa_session):
    fake_data = Faker()

    user = UserInSchema(
        name=fake_data.pystr(min_chars=100, max_chars=200),
        email=fake_data.ascii_safe_email(),
        password="eshkere!",
        password2="eshkere!",
        is_company=False
    )

    new_user = await user_query.create(sa_session, user_schema=user)
    assert new_user is not None
    assert new_user.name == user.name
    assert new_user.hashed_password != user.password


@pytest.mark.asyncio
async def test_create_user(sa_session):
    fake_data = Faker()

    user = UserInSchema(
        name=fake_data.pystr(min_chars=100, max_chars=200),
        email=fake_data.ascii_safe_email(),
        password="eshkere!",
        password2="eshkere!",
        is_company=False
    )

    new_user = await user_query.create(sa_session, user_schema=user)
    assert new_user is not None
    assert new_user.name == user.name
    assert new_user.hashed_password != user.password


@pytest.mark.asyncio
async def test_create_user_with_invalid_data(sa_session):
    user = UserFactory.build(is_company=True)
    sa_session.add(user)
    await sa_session.flush()

    fake_data = Faker()

    with pytest.raises(ValidationError):
        UserInSchema(
            name="a",
            email=fake_data.ascii_safe_email(),
            password="eshkere!",
            password2="eshkere!",
            is_company=False
        )
        UserInSchema(
            name=fake_data.pystr(min_chars=100, max_chars=200),
            email="a",
            password="eshkere!",
            password2="eshkere!",
            is_company=False
        )
        UserInSchema(
            name=fake_data.pystr(min_chars=100, max_chars=200),
            email=fake_data.ascii_safe_email(),
            password="e",
            password2="e",
            is_company=False
        )


@pytest.mark.asyncio
async def test_create_user_password_mismatch(sa_session):
    fake_data = Faker()

    with pytest.raises(ValidationError):
        user = UserInSchema(
            name=fake_data.pystr(min_chars=100, max_chars=200),
            email=fake_data.ascii_safe_email(),
            password="eshkere!",
            password2="eshkero!",
            is_company=False
        )
        await user_query.create(sa_session, user_schema=user)


@pytest.mark.asyncio
async def test_update_user(sa_session):
    user = UserFactory.build()
    sa_session.add(user)
    sa_session.flush()

    user.name = "updated_name"
    updated_user = await user_query.update(sa_session, user=user)
    assert user.id == updated_user.id
    assert updated_user.name == "updated_name"
