import pytest
import pytest_asyncio
from collections.abc import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession
from models.profile import Profile
from models import User


@pytest.fixture
def profile_data() -> dict[str, str]:
    return {
        'first_name': 'John',
        'last_name': 'Doe',
        'bio': 'some bio',
        'mobile': '+375291234567',
    }


@pytest_asyncio.fixture
async def create_profile_with_user(
    profile_data: dict[str, str],
    session: AsyncSession,
    create_user: User,
) -> AsyncIterator[Profile]:
    profile = Profile(**profile_data, user_id=create_user.id)
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    yield profile


@pytest_asyncio.fixture
async def create_profile(
    profile_data: dict[str, str],
    session: AsyncSession,
) -> AsyncIterator[Profile]:
    profile = Profile(**profile_data, user_id=1)
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    yield profile



