from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)


class TokenInfo(BaseModel):
    access_token: str
    token_type: str


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str
    hashed_password: str
    email: EmailStr
    active: bool = True


class CreateUser(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8, max_length=20)
    email: EmailStr = Field(min_length=5, max_length=50)

    @field_validator("password", mode="after")
    @classmethod
    def password_strength(cls, password: str) -> str:
        if not any(i.isdigit() for i in password):
            raise ValueError("Password must contain at least 1 digits")
        if not any(i.isupper() for i in password):
            raise ValueError("Password must contain at least 1 upper case letter")
        if not any(i.islower() for i in password):
            raise ValueError("Password must contain at least 1 lower case letter")
        return password


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    active: bool = True

    model_config = ConfigDict(from_attributes=True)


class UserValidation(UserSchema):
    model_config = ConfigDict(strict=True)
    id: int


class UserUpdate(BaseModel):
    model_config = ConfigDict(strict=True)
    username: Optional[str] = Field(min_length=3, max_length=20, title="Username")
    email: Optional[EmailStr]


class UserUpdatePartial(BaseModel):
    pass
