from httpx import AsyncClient

from .fixtures import *
from models import Product, Profile


@pytest.mark.asyncio
async def test_create_product(
    client: AsyncClient,
    get_jwt_token: str,
    product_data: dict[str, str | int],
    create_profile: Profile,
) -> None:

    response = await client.post(
        "/products/new",
        json=product_data,
        cookies={"access_token": get_jwt_token},
    )
    assert response.status_code == 201
    assert response.json()["name"] == product_data["name"]


@pytest.mark.asyncio
async def test_error_create_product(
    client: AsyncClient,
    get_jwt_token: str,
    product_data: dict[str, str | int],
) -> None:

    response = await client.post(
        "/products/new",
        json=product_data,
        cookies={"access_token": get_jwt_token},
    )
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_products(
    client: AsyncClient,
    create_product: Product,
    create_profile: Profile,
) -> None:
    response = await client.get(
        "products/products?page=1&size=50",
    )
    assert response.status_code == 200
    assert response.json()["items"] != []
    item = response.json()["items"][0]
    assert item["first_name"] == create_profile.first_name
    assert item["mobile"] == create_profile.mobile


@pytest.mark.asyncio
async def test_get_product(
    client: AsyncClient,
    create_product: Product,
    product_data: dict[str, str | int],
) -> None:
    response = await client.get(
        "products/1",
    )
    assert response.status_code == 200
    assert response.json()["name"] == "product"


@pytest.mark.asyncio
async def test_get_user_products(
    client: AsyncClient,
    create_product: Product,
) -> None:
    response = await client.get(
        "products/users/1",
    )
    assert response.status_code == 200
    assert response.json() != []


@pytest.mark.asyncio
async def test_update_full_product(
    client: AsyncClient,
    create_product: Product,
    get_user_jwt: str,
    product_data: dict[str, str | int],
) -> None:
    product_data["name"] = "newname"
    response = await client.put(
        "products/1",
        json=product_data,
        cookies={"access_token": get_user_jwt},
    )
    assert response.status_code == 200

    assert response.json()["name"] == "newname"


@pytest.mark.asyncio
async def test_update_product_invalid_quantity(
    client: AsyncClient,
    create_product: Product,
    get_user_jwt: str,
    product_data: dict[str, str | int],
) -> None:
    product_data["quantity"] = 0
    response = await client.put(
        "products/1",
        json=product_data,
        cookies={"access_token": get_user_jwt},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_product(
    client: AsyncClient,
    create_product: Product,
    get_jwt_token: str,
) -> None:
    response = await client.delete(
        "products/1",
        cookies={"access_token": get_jwt_token},
    )
    assert response.status_code == 204
