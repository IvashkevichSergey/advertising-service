import enum
from sqlalchemy import BigInteger, Enum, Boolean, String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.comments.models import Comment
from app.database import Base
from app.users.models import User


class Group(str, enum.Enum):
    SELLING_ADV = "SELL"
    BUYING_ADV = "BUY"
    SERVICE_ADV = "SERVICE"


class Adv(Base):
    __tablename__ = "advertisement"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(50))
    body: Mapped[str] = mapped_column(String(2500), nullable=True)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    group: Mapped[str] = mapped_column(Enum(Group, name="group"), default=Group.SELLING_ADV)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    author: Mapped[User] = relationship("User", lazy="selectin", back_populates="advertisements")
    comments: Mapped[Comment] = relationship("Comment", back_populates="adv")

    def __repr__(self) -> str:
        return f"Adv(id={self.id}, title={self.title}, author={self.author.username})"
