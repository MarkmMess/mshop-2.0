from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import db_helper
from .schemas import (
    TokenInfo,
    CreateUser,
    UserRead,
    UserValidation,
    UserUpdate,
)
from .service import (
    validate_auth_user,
    get_current_active_auth_user,
)
from . import crud
from . import security as auth_security


router = APIRouter()


@router.post("/signIn", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: CreateUser,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> UserRead:
    return await crud.create_user(session, user)


@router.post("/login/new/", response_model=TokenInfo)
async def auth_user_jwt(
    user: UserValidation = Depends(validate_auth_user),
):
    jwt_token = {
        # subject
        "sub": str(user.id),
        "username": user.username,
    }
    token = auth_security.encode_jwt(jwt_token)
    return TokenInfo(
        access_token=token,
        token_type="bearer",
    )


@router.get("/check/user/", response_model=UserRead)
def auth_user_check_info(
    user: UserRead = Depends(get_current_active_auth_user),
):
    return user


@router.get("/user/{user_id}", response_model=UserRead)
async def get_user_by_id(
    user_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await crud.get_user(session, user_id)
    return user


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
