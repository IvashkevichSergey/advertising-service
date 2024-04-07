from pydantic import BaseModel, Field


class CommentCreate(BaseModel):
    """Model to CREATE object"""
    body: str = Field(min_length=1, max_length=500)


class CommentBase(CommentCreate):
    """Base model to view comment info"""
    id: int
    author_id: int
    adv_id: int
