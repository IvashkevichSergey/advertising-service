from pydantic import BaseModel, Field
from app.adv.models import Group


class AdvCreate(BaseModel):
    """Model to CREATE advertisement"""
    title: str = Field(min_length=3, max_length=50)
    body: str | None = Field(max_length=2500, default=None)
    group: Group = Group.SELLING_ADV


class AdvBase(BaseModel):
    """Base model to view advertisement info"""
    id: int
    title: str
    body: str | None = Field(default=None)
    author_id: int
    group: Group


class AdvUpdate(AdvCreate):
    """Base model to update advertisement info"""
    title: str = Field(min_length=3, max_length=50, default=None)
