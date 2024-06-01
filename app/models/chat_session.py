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
    from models.chat import Chat


class ChatSession(Base):
    __tablename__ = "chat_session"
    __table_args__ = {"sqlite_autoincrement": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    user_create_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user_create: Mapped["User"] = relationship(back_populates="chat_sessions_create")
    users_connect: Mapped[List["User"]] = relationship(
        secondary="user_chat_session_table", back_populates="chat_sessions_connect"
    )
    chats: Mapped[List["Chat"]] = relationship(
        back_populates="chat_session", cascade="all, delete"
    )

    name: Mapped[str] = mapped_column(String(64))
    information: Mapped[str] = mapped_column(String(256))
    create_date: Mapped[DateTime] = mapped_column(DateTime(), default=datetime.now)
    update_date: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(), onupdate=datetime.now
    )
    is_visible: Mapped[Boolean] = mapped_column(Boolean(), default=True)
    is_closed: Mapped[Boolean] = mapped_column(Boolean(), default=False)
