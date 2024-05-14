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
    from models.ai import AI


class AIlog(Base):
    __tablename__ = "ai_log"
    __table_args__ = {"sqlite_autoincrement": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="ai_logs")
    ai_id: Mapped[int] = mapped_column(ForeignKey("ai.id"))
    ai: Mapped["AI"] = relationship(back_populates="ai_logs")

    description: Mapped[str] = mapped_column(String(256))
    result: Mapped[str] = mapped_column(String(256))
    create_date: Mapped[DateTime] = mapped_column(DateTime(), default=datetime.now)
    update_date: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(), onupdate=datetime.now
    )
    finish_date: Mapped[Optional[DateTime]] = mapped_column(DateTime(), default=None)
    is_finished: Mapped[Boolean] = mapped_column(Boolean(), default=False)
    celery_task_id: Mapped[str] = mapped_column(String(64))
