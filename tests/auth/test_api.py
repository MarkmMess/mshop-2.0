import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_user(
        client: AsyncClient,
        user_data: dict,
):
    response = await client.post("/auth/signIn", json=user_data)

    assert response.status_code == 201
    assert response.json()['username']  == user_data['username']


@pytest.mark.asyncio
async def test_error_create_user(
        client: AsyncClient,
        create_user: None,
        user_data: dict
):
    response = await client.post("/auth/signIn", json=user_data)
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_get_auth_token(
        client: AsyncClient,
        create_user: None,
        user_data: dict
):
    response = await client.post(
            "/auth/login/new/",
            data={
                "username": user_data['username'],
                "password": user_data['password']
            },
    )
    assert response.status_code == 200
    result = response.json()['access_token']
    global jwt
    jwt = result


@pytest.mark.asyncio
async def test_error_auth_token(
        client: AsyncClient,
        create_user,
):
    response = await client.post(
        "/login/new/",
        data={"username": "labuba", "password": "228"}
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_auth_user_check_info(
        client: AsyncClient,
        get_jwt_token,
):
    response = await client.get(
        "/auth/check/user/",
        headers={"Authorization": f"Bearer {get_jwt_token}"}
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_user(
        client: AsyncClient,
        get_jwt_token,
):
    response = await client.put("/auth/update_user/",
                               json={
                                         "username": "testik",
                                         "email": "email@mail.com"
                               },
                               headers={"Authorization": f"Bearer {get_jwt_token}"}
                                )

    assert response.status_code == 200
    assert response.json()['username'] == 'testik'


@pytest.mark.asyncio
async def test_delete_user(
        client: AsyncClient,
        get_jwt_token,
        create_user,
):
    response = await client.delete(
        "/auth/delete_user/",
        headers={"Authorization": f"Bearer {get_jwt_token}"}
    )

    assert response.status_code == 200
