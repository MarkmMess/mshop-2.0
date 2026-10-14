import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.auth.security import encode_jwt
from src.models import Product, User, Category, Profile
from ..conftest import session, create_user, user_data


@pytest.fixture
def product_data():
    return {
        'name': 'product',
        'description': 'product description',
        'price': 100,
        'quantity': 1,
        'category_name': 'category',
    }

@pytest_asyncio.fixture
async def create_product(
        product_data: dict,
        session: AsyncSession,
        create_user: User,
        create_category
):
    product = Product(**product_data, user_id=create_user.id)
    session.add(product)
    await session.commit()
    await session.refresh(product)
    yield product


@pytest_asyncio.fixture
async def create_category(
        session: AsyncSession,
):
    category = Category(name='category')
    session.add(category)
    await session.commit()
    await session.refresh(category)
    yield category


@pytest_asyncio.fixture
async def create_profile(
        session: AsyncSession,
):
    profile = Profile(first_name='John', last_name='Doe', user_id=1)
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    yield profile


@pytest_asyncio.fixture
async def get_user_jwt(
        user_data: dict,
):
    jwt_token = {
        "sub": '1',
        "username": user_data['username'],
    }
    token = encode_jwt(jwt_token)
    yield token