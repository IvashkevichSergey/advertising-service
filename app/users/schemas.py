from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.adv.schemas import AdvBase
from app.users.models import Roles


class UserCreate(BaseModel):
    """Model to CREATE user"""
    username: str = Field(min_length=3, max_length=25)
    password: str = Field(min_length=3)
    # role: Roles = Roles.ADMIN_ROLE


class UserBase(BaseModel):
    """Base model to check user info"""
    username: str
    fullname: str | None = Field(default=None)
    email: EmailStr | None = Field(default=None)
    advertisements: list[AdvBase]

    model_config = ConfigDict(arbitrary_types_allowed=True)


class UserUpdate(BaseModel):
    """Base model to update user profile info"""
    username: str = Field(min_length=3, max_length=25, default=None)
    password: str = Field(min_length=3, default=None)
    fullname: str = Field(default=None)
    email: EmailStr = Field(default=None)


class UserFullInfo(UserBase):
    """Extended model to check user info by Admin"""
    id: int
    role: Roles
    is_active: bool


class UserUpdateAdmin(BaseModel):
    """Extended model to update user restricted data by Admin"""
    username: str
    role: Roles = Field(default=None)
    is_active: bool = Field(default=None)
