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
    pass


class UserChatSessionTable(Base):
    __tablename__ = "user_chat_session_table"
    # __table_args__ = {"sqlite_autoincrement": True}

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)
    chat_session_id: Mapped[int] = mapped_column(
        ForeignKey("chat_session.id"), primary_key=True
    )
    create_date: Mapped[DateTime] = mapped_column(DateTime(), default=datetime.now)
