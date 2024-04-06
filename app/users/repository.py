from typing import Sequence
from passlib.context import CryptContext
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from app import User
from app.users.schemas import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"])


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def create(self, user_data: UserCreate) -> User:
        """Create a new User"""
        user_password = pwd_context.hash(user_data.password)
        new_user = User(username=user_data.username, password=user_password)
        self.session.add(new_user)
        return new_user

    async def read(self, username: str) -> User:
        """Return a User by username from DB"""
        query = select(User).where(User.username == username).options(selectinload(User.advertisements))
        result = await self.session.execute(query)
        return result.scalar()

    async def read_all(self) -> Sequence[User]:
        """Return list of all Users"""
        query = select(User).options(selectinload(User.advertisements))
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self,
                     user_data: UserUpdate,
                     user_instance: User) -> User:
        """Update a User info"""
        if not user_data.model_dump(exclude_unset=True):
            return user_instance
        query = update(User). \
            where(User.id == user_instance.id). \
            values(**user_data.model_dump(exclude_unset=True))
        await self.session.execute(query)
        await self.session.refresh(user_instance)
        await self.session.commit()
        return user_instance

    async def delete(self, username: str):
        """Delete a User"""
        query = delete(User).where(User.username == username).returning(User)
        user = await self.session.execute(query)
        await self.session.commit()
        return user.scalar()
