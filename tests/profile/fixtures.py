import pytest
from models.profile import Profile


@pytest.fixture
def profile_data():
    return {
        'first_name': 'John',
        'last_name': 'Doe',
        'bio': 'some bio',
        'mobile': '+37555555555',
    }


@pytest.fixture
async def create_profile_with_user(profile_data, session, create_user):
    profile = Profile(**profile_data, user_id=create_user.id)
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    yield profile


@pytest.fixture
async def create_profile(profile_data, session):
    profile = Profile(**profile_data, user_id=1)
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    yield profile



