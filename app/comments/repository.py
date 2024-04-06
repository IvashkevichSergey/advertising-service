from typing import Sequence

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.comments.models import Comment
from app.comments.schemas import CommentCreate


class CommentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def create(self, comment_data: CommentCreate, author_id: int, adv_id: int) -> Comment:
        """Create an instance of new Comment"""
        new_comment = Comment(author_id=author_id, adv_id=adv_id, **comment_data.model_dump(exclude_unset=True))
        self.session.add(new_comment)
        return new_comment

    async def read(self, comment_id: int) -> Comment:
        """Return a Comment instance by its ID from DB"""
        query = select(Comment).where(Comment.id == comment_id)
        result = await self.session.execute(query)
        return result.scalar()

    async def read_all(self, adv_id: int) -> Sequence[Comment]:
        """Return list of all Comment instances for the Adv"""
        query = select(Comment).where(Comment.adv_id == adv_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self,
                     comment_data: CommentCreate,
                     comment_instance: Comment) -> Comment:
        """Update a Comment instance"""
        if not comment_data.model_dump(exclude_unset=True):
            return comment_instance
        query = update(Comment). \
            where(Comment.id == comment_instance.id). \
            values(**comment_data.model_dump(exclude_unset=True))
        await self.session.execute(query)
        await self.session.refresh(comment_instance)
        await self.session.commit()
        return comment_instance

    async def delete(self, comment_id: int):
        """Delete a Comment instance"""
        query = delete(Comment).where(Comment.id == comment_id).returning(Comment)
        comment_instance = await self.session.execute(query)
        await self.session.commit()
        return comment_instance.scalar()
