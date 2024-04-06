from pydantic import BaseModel, Field, ConfigDict

from app import User


class AdvBase(BaseModel):
    title: str
    body: str | None = Field(default=None)
    author_id: int

