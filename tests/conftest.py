import os

os.environ["APP_DB__URL"] = (
    "postgresql+asyncpg://test_user:test_password@localhost:5433/test_shop_db"
)
# os.environ["APP_DB__URL"] = (
#     "postgresql+asyncpg://postgres:postgres@localhost:5432/mshop"
# )

import pytest
import pytest_asyncio

from httpx import AsyncClient, ASGITransport
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.pool import NullPool

from core.config import settings
from models import User, Base
from api_v1.auth.security import hash_password
from main import main_app
from models import db_helper


test_engine = create_async_engine(
    str(settings.db.url),
    echo=True,
    poolclass=NullPool,
)


TestSessionLocal = async_sessionmaker(
    test_engine,
    expire_on_commit=False,
)


# Creating tables from alchemy models
@pytest_asyncio.fixture(scope="function", autouse=True)
async def create_tables():

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def session():
    async with TestSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def client(session: AsyncSession):

    # Replacing app session with session test one
    async def override_session():
        yield session

    main_app.dependency_overrides[
        db_helper.scoped_session_dependency
    ] = override_session


    transport = ASGITransport(app=main_app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test/api/v1",
    ) as client:
        yield client

    main_app.dependency_overrides.clear()


@pytest.fixture
def user_data():
    return {
        "username": "test",
        "password": "Test1234",
        "email": "mail@mail.com",
    }


@pytest_asyncio.fixture
async def create_user(
    user_data: dict,
    session: AsyncSession,
):
    user = User(
        username=user_data["username"],
        email=user_data["email"],
        hashed_password=hash_password(user_data["password"]),
        active=True,
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    yield user
