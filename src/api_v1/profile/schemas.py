from typing import Optional

from pydantic import Field, BaseModel, field_validator


class CreateProfile(BaseModel):
    first_name: str = Field(min_length=3, max_length=30)
    last_name: Optional[str | None] = Field(None, min_length=3, max_length=30)
    bio: Optional[str | None] = Field(None, max_length=255)
    mobile: Optional[str | None] = Field(None, min_length=11, max_length=15)

    @field_validator("mobile", mode="after")
    @classmethod
    def validate_mobile(cls, mobile: str) -> str:
        if not mobile.startswith("+375") and not mobile.startswith("80"):
            raise ValueError(f"mobile number must start with +375 or 80")
        return mobile


class ProfileRead(BaseModel):
    first_name: str
    last_name: Optional[str | None]
    bio: Optional[str | None]
    mobile: Optional[str | None]
    user_id: int


class UpdateProfile(CreateProfile):
    first_name: Optional[str | None] = Field(min_length=3, max_length=30)
