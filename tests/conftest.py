import os
from collections.abc import AsyncIterator

os.environ["APP_DB__URL"] = (
    "postgresql+asyncpg://test_user:test_password@localhost:5433/test_shop_db"
)

import pytest
import pytest_asyncio

from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)
from sqlalchemy.pool import NullPool

from core.config import settings
from models import User, Base
from api_v1.auth.security import hash_password, encode_jwt
from main import main_app
from models import db_helper

test_engine: AsyncEngine = create_async_engine(
    str(settings.db.url),
    # echo=True,
    poolclass=NullPool,
)


TestSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    test_engine,
    expire_on_commit=False,
)


# Creating tables from alchemy models
@pytest_asyncio.fixture(scope="function", autouse=True)
async def create_tables() -> AsyncIterator[None]:

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def session() -> AsyncIterator[AsyncSession]:
    async with TestSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def client(session: AsyncSession) -> AsyncIterator[AsyncClient]:

    # Replacing app session with session test one
    async def override_session() -> AsyncIterator[AsyncSession]:
        yield session

    main_app.dependency_overrides[db_helper.scoped_session_dependency] = (
        override_session
    )

    transport = ASGITransport(app=main_app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test/api/v1",
    ) as client:
        yield client

    main_app.dependency_overrides.clear()


@pytest.fixture
def user_data() -> dict[str, str]:
    return {
        "username": "test",
        "password": "Test1234",
        "email": "mail@mail.com",
    }


@pytest_asyncio.fixture
async def create_user(
    user_data: dict[str, str],
    session: AsyncSession,
) -> AsyncIterator[User]:
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


@pytest_asyncio.fixture
async def get_jwt_token(create_user: User) -> AsyncIterator[str]:
    jwt_token = {
        "sub": str(create_user.id),
        "username": create_user.username,
    }
    token = encode_jwt(jwt_token)
    yield token


@pytest_asyncio.fixture
async def get_user_jwt(
    user_data: dict[str, str],
) -> AsyncIterator[str]:
    jwt_token = {
        "sub": "1",
        "username": user_data["username"],
    }
    token = encode_jwt(jwt_token)
    yield token
