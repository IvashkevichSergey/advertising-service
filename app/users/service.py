from typing import Optional, List

from passlib.context import CryptContext
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app import Adv
from app.users.models import User
from app.users.schemas import UserCreate, UserBase, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"])


async def get_user_by_username(session: AsyncSession, username: str) -> User:
    """Return a User instance by username from DB"""
    # new_adv = Adv(title="New super new adv", author_id=2)
    # session.add(new_adv)
    # await session.commit()
    query = select(User).where(User.username == username).options(selectinload(User.advertisements))
    result = await session.execute(query)
    return result.scalar()


async def get_all_users(session: AsyncSession) -> List[User]:
    """Return list of all User instances"""
    query = select(User)
    result = await session.execute(query)
    return result.scalars().all()


def create_new_user(session: AsyncSession, user_data: UserCreate) -> User:
    """Create an instance of new User"""
    user_password = pwd_context.hash(user_data.password)
    new_user = User(username=user_data.username, password=user_password)
    session.add(new_user)
    return new_user


async def auth_user(session: AsyncSession,
                    username: str, password: str) -> Optional[User]:
    """Check if the user exists and the password is correct"""
    user = await get_user_by_username(session, username)
    if not (user and pwd_context.verify(password, user.password)):
        return None
    return user


async def update_user(session: AsyncSession,
                      user_data: UserUpdate,
                      user_instance: User):
    if not user_data.model_dump(exclude_unset=True):
        return user_instance
    query = update(User). \
        where(User.id == user_instance.id). \
        values(**user_data.model_dump(exclude_unset=True))
    await session.execute(query)
    await session.refresh(user_instance)
    await session.commit()
    return user_instance
