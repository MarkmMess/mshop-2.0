import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator

BELARUS_MOBILE_REGEX = re.compile(r"(\+375|80)(25|29|33|44)\d{7}")


def validate_mobile_number(mobile: str) -> str:
    if not isinstance(mobile, str):
        raise ValueError("mobile number must be a string")
    stripped = mobile.strip()
    if not BELARUS_MOBILE_REGEX.fullmatch(stripped):
        raise ValueError("mobile number must be in the format +375XXXXXXXXX or 80XXXXXXXXX")
    return stripped


class CreateProfile(BaseModel):
    first_name: str = Field(min_length=3, max_length=30)
    last_name: Optional[str | None] = Field(None, min_length=3, max_length=30)
    bio: Optional[str | None] = Field(None, max_length=255)
    mobile: str

    @field_validator("mobile", mode="before")
    @classmethod
    def validate_mobile(cls, mobile: str) -> str:
        return validate_mobile_number(mobile)


class ProfileRead(BaseModel):
    first_name: str
    last_name: Optional[str | None]
    bio: Optional[str | None]
    mobile: Optional[str | None]
    user_id: int


class UpdateProfile(CreateProfile):
    first_name: Optional[str | None] = Field(default=None, min_length=3, max_length=30)
    mobile: Optional[str] = Field(default=None)

    @field_validator("mobile", mode="before")
    @classmethod
    def validate_mobile_update(cls, mobile: Optional[str]) -> Optional[str]:
        if mobile is None:
            return None
        stripped = mobile.strip() if isinstance(mobile, str) else mobile
        if not stripped:
            return None
        return validate_mobile_number(stripped)
