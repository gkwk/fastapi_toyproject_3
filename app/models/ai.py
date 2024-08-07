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
    Enum
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base
from enums import AIType

if TYPE_CHECKING:
    from models.ailog import AIlog


class AI(Base):
    __tablename__ = "ai"
    __table_args__ = {"sqlite_autoincrement": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    ai_logs: Mapped[List["AIlog"]] = relationship(
        back_populates="ai", cascade="all, delete"
    )

    name: Mapped[str] = mapped_column(String(64), unique=True)
    description: Mapped[str] = mapped_column(String(256))
    ai_type: Mapped[AIType] = mapped_column(Enum(AIType), nullable=False)
    create_date: Mapped[DateTime] = mapped_column(DateTime(), default=datetime.now)
    update_date: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(), onupdate=datetime.now
    )
    finish_date: Mapped[Optional[DateTime]] = mapped_column(DateTime(), default=None)
    is_visible: Mapped[Boolean] = mapped_column(Boolean(), default=False)
    is_available: Mapped[Boolean] = mapped_column(Boolean(), default=False)
    celery_task_id: Mapped[str] = mapped_column(String(64))
