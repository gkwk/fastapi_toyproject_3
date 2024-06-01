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
    from models.board import Board
    from models.post import Post
    from models.user_board_table import UserPermissionTable
    from models.ailog import AIlog
    from models.comment import Comment
    from models.chat_session import ChatSession
    from models.chat import Chat
    


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"sqlite_autoincrement": True}

    id: Mapped[int] = mapped_column(primary_key=True)

    boards: Mapped[List["Board"]] = relationship(
        secondary="user_board_table", back_populates="users"
    )  # N to M
    posts: Mapped[List["Post"]] = relationship(back_populates="user")  # 1 to N
    comments: Mapped[List["Comment"]] = relationship(back_populates="user")  # 1 to N
    
    ai_logs: Mapped[List["AIlog"]] = relationship(
        back_populates="user", cascade="all, delete"
    )  # 1 to N
    
    chat_sessions_create: Mapped[List["ChatSession"]] = relationship(
        back_populates="user_create"
    )  # 1 to N
    chat_sessions_connect: Mapped[List["ChatSession"]] = relationship(
        secondary="user_chat_session_table", back_populates="users_connect"
    )  # N to M
    chats: Mapped[List["Chat"]] = relationship(back_populates="user")  # 1 to N

    name: Mapped[str] = mapped_column(String(64), unique=True)
    email: Mapped[str] = mapped_column(String(256), unique=True)
    password: Mapped[str] = mapped_column(String())
    password_salt: Mapped[str] = mapped_column(String())
    role: Mapped[str] = mapped_column(String())
    join_date: Mapped[DateTime] = mapped_column(DateTime(), default=datetime.now)
    update_date: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(), onupdate=datetime.now
    )
    is_banned: Mapped[bool] = mapped_column(Boolean(), default=False)
