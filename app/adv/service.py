from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.adv.repository import AdvRepository
from app.database import get_session


async def get_adv_repo(session: AsyncSession = Depends(get_session)) -> AdvRepository:
    """Service function to return class with Adv CRUD operations"""
    return AdvRepository(session)
