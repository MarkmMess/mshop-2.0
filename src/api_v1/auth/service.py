from typing import Annotated

from fastapi import APIRouter, Depends, Form, Path
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from models import db_helper
from . import crud
from .errors import not_found, unauth, inactive
from .schemas import UserRead, UserValidation
import api_v1.auth.security as auth_security

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login/new/")


router = APIRouter(prefix="/jwt", tags=["jwt"])


async def validate_auth_user(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    username: str = Form(...),
    password: str = Form(...),
) -> UserValidation:
    user = await crud.get_user_for_validation(session, username)
    if not user:
        raise not_found
    if not auth_security.validate_password(password, user.hashed_password):
        raise unauth
    return user


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        payload = auth_security.decode_jwt(
            token,
        )
    except JWTError:
        raise unauth
    return payload


async def get_current_auth_user(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    payload: dict = Depends(get_current_token_payload),
) -> UserRead:
    user_id: int | None = int(payload.get("sub"))
    if not user_id:
        raise unauth
    if user := await crud.get_user(session, user_id):
        return user
    raise not_found


def get_current_active_auth_user(
    user: UserRead = Depends(get_current_auth_user),
):
    if user.active:
        return user
    raise inactive
