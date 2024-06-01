from datetime import datetime
from typing import List, Optional, TYPE_CHECKING

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

from database.database import Base

if TYPE_CHECKING:
    from models.user import User
    from models.chat_session import ChatSession


class Chat(Base):
    __tablename__ = "chat"
    __table_args__ = {"sqlite_autoincrement": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="chats")
    chat_session_id: Mapped[int] = mapped_column(ForeignKey("chat_session.id"))
    chat_session: Mapped["ChatSession"] = relationship(back_populates="chats")

    content: Mapped[str] = mapped_column(String(256))
    create_date: Mapped[DateTime] = mapped_column(DateTime(), default=datetime.now)
    update_date: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(), onupdate=datetime.now
    )
    is_visible: Mapped[Boolean] = mapped_column(Boolean(), default=True)

