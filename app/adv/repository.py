from typing import Sequence
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app import Adv
from app.adv.schemas import AdvCreate, AdvUpdate


class AdvRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def create(self, adv_data: AdvCreate, author_id: int) -> Adv:
        """Create an instance of new Adv"""
        new_adv = Adv(author_id=author_id, **adv_data.model_dump(exclude_unset=True))
        self.session.add(new_adv)
        return new_adv

    async def read(self, adv_id: int) -> Adv:
        """Return an Adv instance by its id from DB"""
        # query = select(Adv).where(Adv.id == adv_id).options(selectinload(Adv.advertisements))
        query = select(Adv).where(Adv.id == adv_id)
        result = await self.session.execute(query)
        return result.scalar()

    async def read_all(self) -> Sequence[Adv]:
        """Return list of all Adv instances"""
        query = select(Adv)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self,
                     adv_data: AdvUpdate,
                     adv_instance: Adv) -> Adv:
        """Update an Adv instance"""
        if not adv_data.model_dump(exclude_unset=True):
            return adv_instance
        query = update(Adv).\
            where(Adv.id == adv_instance.id). \
            values(**adv_data.model_dump(exclude_unset=True))
        await self.session.execute(query)
        await self.session.refresh(adv_instance)
        await self.session.commit()
        return adv_instance

    async def delete(self, adv_id: int):
        """Delete an Adv instance"""
        query = delete(Adv).where(Adv.id == adv_id).returning(Adv)
        adv_instance = await self.session.execute(query)
        await self.session.commit()
        return adv_instance.scalar()
