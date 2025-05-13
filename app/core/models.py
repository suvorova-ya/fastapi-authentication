from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class UserBase(Base):
    """ Модель User в БД """
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(64), unique=True, nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(64), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(256), nullable=False)
    disabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"

