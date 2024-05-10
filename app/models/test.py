from database.database import Base

from datetime import datetime
from typing import List, Optional

from sqlalchemy import (
    Integer,
    String,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Table,
    Column,
    BigInteger,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from models.user import User


class Test(Base):
    __tablename__ = "test"
    __table_args__ = {"sqlite_autoincrement": True}

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(64), unique=True)
    email: Mapped[str] = mapped_column(String(256), unique=True)
    password: Mapped[str] = mapped_column(String())
    password_salt: Mapped[str] = mapped_column(String())
    join_date: Mapped[DateTime] = mapped_column(DateTime(), default=datetime.now)
    update_date: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(), onupdate=datetime.now
    )
    user: Mapped["User"] = relationship(back_populates="test")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
