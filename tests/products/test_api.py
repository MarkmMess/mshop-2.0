from httpx import AsyncClient

from .fixtures import *


@pytest.mark.asyncio
async def test_create_product(
        client: AsyncClient,
        get_jwt_token,
        product_data,
):

    response = await client.post(
        "/products/new",
        json=product_data,
        headers={"Authorization": f"Bearer {get_jwt_token}"},
        )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_get_products(
        client: AsyncClient,
        create_product,
):
    response = await client.get(
        "products/products?page=1&size=50",
    )
    assert response.status_code == 200
    assert response.json()['items'] != []


@pytest.mark.asyncio
async def test_get_product(
        client: AsyncClient,
        create_product,
        product_data,
):
    response = await client.get(
        "products/1",
    )
    assert response.status_code == 200
    assert response.json()['name'] == 'product'


@pytest.mark.asyncio
async def test_get_user_products(
        client: AsyncClient,
        create_product,
):
    response = await client.get(
        "products/users/1",
    )
    assert response.status_code == 200
    assert response.json() != []
