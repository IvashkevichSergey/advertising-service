import enum

from sqlalchemy import BigInteger, Enum, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Roles(str, enum.Enum):
    USER_ROLE = "USER"
    ADMIN_ROLE = "ADMIN"
    MODERATOR_ROLE = "MODERATOR"


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(25), unique=True)
    password: Mapped[str] = mapped_column(String(250))
    fullname: Mapped[str] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(String(50), nullable=True)
    role: Mapped[str] = mapped_column(Enum(Roles, name="role"), default=Roles.USER_ROLE)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    advertisements: Mapped[list["Adv"]] = relationship("Adv",
                                                       back_populates="author",
                                                       passive_deletes=True)
    comments: Mapped[list["Comment"]] = relationship("Comment",
                                                     back_populates="author",
                                                     passive_deletes=True)

    def __repr__(self) -> str:
        return f"User(id={self.id}, username={self.username}, role={self.role})"
