from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import db_helper
from .schemas import (
    CreateUser,
    UserRead,
    UserValidation,
    UserUpdate,
    UserPublicRead,
)
from .service import (
    validate_auth_user,
    get_current_active_auth_user,
    get_public_user,
    set_auth_cookie,
)
from . import crud

router = APIRouter()


@router.post("/signIn", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: CreateUser,
    response: Response,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> UserRead:
    user = await crud.create_user(session, user)
    set_auth_cookie(response, user.id, user.username)
    return await crud.create_user(session, user)


@router.post("/logout", response_model=dict)
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"detail": "ok"}


@router.post("/login", response_model=dict)
async def auth_user_jwt(
    response: Response,
    user: UserValidation = Depends(validate_auth_user),
):
    set_auth_cookie(response, user.id, user.username)
    return {"detail": "ok"}


@router.get("/check/user/", response_model=UserRead)
def auth_user_check_info(
    user: UserRead = Depends(get_current_active_auth_user),
):
    return user


@router.get("/user/{user_id}", response_model=UserPublicRead)
async def get_user_by_id(
    user_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await get_public_user(session, user_id)


@router.put("/update_user/", response_model=UserRead)
async def update_user(
    update_user_scheme: UserUpdate,
    user: UserRead = Depends(get_current_active_auth_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_user(session, user, update_user_scheme)


@router.delete("/delete_user/")
async def delete_user(
    user: UserRead = Depends(get_current_active_auth_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await crud.del_user(session, user)
