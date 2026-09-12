import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.auth.security import encode_jwt
from models import Product, User, Category
from ..conftest import session, create_user, user_data


@pytest.fixture
def product_data():
    return {
        'name': 'product',
        'description': 'product description',
        'price': 100,
        'quantity': 1,
    }

@pytest_asyncio.fixture
async def create_product(
        product_data: dict,
        session: AsyncSession,
        create_user: User,
):
    product_data['user_id'] = create_user.id
    product = Product(**product_data)
    session.add(product)
    await session.commit()
    await session.refresh(product)
    yield product


@pytest_asyncio.fixture
async def create_category(
        session: AsyncSession,
):
    category = Category(name='product')
    session.add(category)
    await session.commit()
    await session.refresh(category)
    yield category


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