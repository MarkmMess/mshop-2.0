from datetime import timedelta, datetime, timezone

import bcrypt

from jose import jwt, JWTError

from core.config import settings


def encode_jwt(
    token: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.token_expire_minutes,
    expire_timedelta: timedelta | None = None,
):
    to_encode = token.copy()
    now = datetime.now(timezone.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encode = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encode


def decode_jwt(
    token: str,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    try:
        decoded = jwt.decode(token, public_key, algorithms=[algorithm])
        return decoded
    except JWTError:
        raise


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode("utf-8")


def validate_password(password: str, hashed_pass) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_pass.encode("utf-8"))
