from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.users.repository import UserRepository


async def get_user_repo(session: AsyncSession = Depends(get_session)) -> UserRepository:
    """Service function to return class with User CRUD operations"""
    return UserRepository(session)
