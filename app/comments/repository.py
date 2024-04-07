from typing import Sequence
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.adv.models import Group, Adv
from app.comments.models import Comment
from app.comments.schemas import CommentCreate


class CommentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    def create(self, comment_data: CommentCreate, author_id: int, adv_id: int) -> Comment:
        """Create an instance of new Comment
        Parameters
        ----------
        comment_data :
            Data of pydantic class CommentCreate to create new Comment
        author_id :
            ID of author of new Comment
        adv_id :
            ID of Adv of new Comment

        Returns
        -------
        Comment :
            A new instance of the Comment class
        """
        new_comment = Comment(
            author_id=author_id,
            adv_id=adv_id,
            **comment_data.model_dump(exclude_unset=True)
        )
        self.session.add(new_comment)
        return new_comment

    async def read(self, comment_id: int) -> Comment:
        """Return a Comment instance by its ID from DB
        Parameters
        ----------
        comment_id :
            ID of a Comment instance

        Returns
        -------
        Comment :
            An instance of the Comment class from database
        """
        query = select(Comment).where(Comment.id == comment_id)
        result = await self.session.execute(query)
        return result.scalar()

    async def read_all(self, adv_id: int) -> Sequence[Comment]:
        """Return list of all Comment instances for the Adv
        Returns
        -------
        Comment :
            All instances of the Comment class from database
        """
        query = select(Comment).where(Comment.adv_id == adv_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update(self,
                     comment_data: CommentCreate,
                     comment_instance: Comment) -> Comment:
        """Update a Comment instance
        Parameters
        ----------
        comment_data :
            Data of pydantic class CommentCreate to update the Comment
        comment_instance :
            An instance of Comment to change

        Returns
        -------
        Comment :
            A changed instance of the Comment class
        """
        if not comment_data.model_dump(exclude_unset=True):
            return comment_instance
        query = update(Comment). \
            where(Comment.id == comment_instance.id). \
            values(**comment_data.model_dump(exclude_unset=True))
        await self.session.execute(query)
        await self.session.refresh(comment_instance)
        await self.session.commit()
        return comment_instance

    async def delete(self, comment_id: int) -> Comment:
        """Delete a Comment instance
        Parameters
        ----------
        comment_id :
            ID of the Comment instance

        Returns
        -------
        Comment :
            Deleted instance of the Comment class
        """
        query = delete(Comment).where(Comment.id == comment_id).returning(Comment)
        comment_instance = await self.session.execute(query)
        await self.session.commit()
        return comment_instance.scalar()

    async def delete_group(self, adv_group: Group) -> int:
        """Delete all Comment instances from specific Adv Group
        Parameters
        ----------
        adv_group :
            Name of an Adv's Group

        Returns
        -------
        int :
            Number of deleted instances of the Comment class
        """
        subquery = select(Adv.id).where(Adv.group == adv_group)
        query = delete(Comment). \
            where(Comment.adv_id.in_(subquery)). \
            returning(Comment)
        comment_instances = await self.session.execute(query)
        await self.session.commit()
        return len(comment_instances.scalars().all())
