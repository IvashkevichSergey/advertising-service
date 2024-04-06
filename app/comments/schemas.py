from pydantic import BaseModel, Field


class CommentCreate(BaseModel):
    body: str = Field(min_length=1, max_length=500)


class CommentBase(CommentCreate):
    id: int
    author_id: int
    adv_id: int
