from sqlalchemy import BigInteger, String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Comment(Base):
    """Comment database model"""
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    body: Mapped[str] = mapped_column(String(500))
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    adv_id: Mapped[int] = mapped_column(Integer, ForeignKey("advertisement.id", ondelete="CASCADE"))

    author: Mapped["User"] = relationship("User", lazy="selectin", back_populates="comments")
    adv: Mapped["Adv"] = relationship("Adv", lazy="selectin", back_populates="comments")

    def __repr__(self) -> str:
        return f"Comment("f"id={self.id}, body={self.body}, " \
               f"author={self.author.username}, adv={self.adv.id})"
