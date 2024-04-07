from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.adv.schemas import AdvBase
from app.users.models import Roles


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=25)
    password: str = Field(min_length=3)


class UserBase(BaseModel):
    username: str
    fullname: str | None = Field(default=None)
    email: EmailStr | None = Field(default=None)
    advertisements: list[AdvBase]

    model_config = ConfigDict(arbitrary_types_allowed=True)


class UserUpdate(BaseModel):
    username: str = Field(min_length=3, max_length=25, default=None)
    password: str = Field(min_length=3, default=None)
    fullname: str = Field(default=None)
    email: EmailStr = Field(default=None)


class UserFullInfo(UserBase):
    id: int
    role: Roles
    is_active: bool


class UserUpdateAdmin(BaseModel):
    username: str
    role: Roles = Field(default=None)
    is_active: bool = Field(default=None)
