from httpx import AsyncClient


from .fixtures import *
from ..products.fixtures import *


@pytest.mark.asyncio
async def test_create_profile(
        client: AsyncClient,
        get_jwt_token,
        profile_data: dict
):
    response = await client.post(
        url="/profile/create",
        json=profile_data,
        headers={"Authorization": f"Bearer {get_jwt_token}"}
    )
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_get_profile(
        client: AsyncClient,
        create_profile_with_user,
        get_user_jwt,
):
    response = await client.get(
        url="/profile/profile",
        headers={"Authorization": f"Bearer {get_user_jwt}"}
    )
    assert response.status_code == 200
    assert response.json()['first_name'] == create_profile_with_user.first_name


@pytest.mark.asyncio
async def test_get_user_profile(
        client: AsyncClient,
        create_profile_with_user,
):
    response = await client.get(
        url="/profile/profile/1",
    )
    assert response.status_code == 200
    assert response.json()['first_name'] == create_profile_with_user.first_name


@pytest.mark.asyncio
async def test_profile_product(
        client: AsyncClient,
        create_product,
        create_profile,
):
    response = await client.get(
        url="/profile/profile/products/1",
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_profile(
        client: AsyncClient,
        create_profile_with_user,
        profile_data: dict,
        get_user_jwt,
):
    profile_data['first_name'] = 'newName'
    response = await client.put(
        url="/profile/profile/update",
        json=profile_data,
        headers={"Authorization": f"Bearer {get_user_jwt}"}
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_profile(
        client: AsyncClient,
        create_profile_with_user,
        get_user_jwt,
):
    response = await client.delete(
        url="/profile/delete",
        headers={"Authorization": f"Bearer {get_user_jwt}"}
    )
    assert response.status_code == 204
