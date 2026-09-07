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
