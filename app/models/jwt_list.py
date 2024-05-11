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


class JWTList(Base):
    __tablename__ = "jwt_list"
    # __table_args__ = {"sqlite_autoincrement": True}

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    refresh_token_uuid: Mapped[str] = mapped_column(String(36))
    refresh_token_unix_timestamp: Mapped[int] = mapped_column(BigInteger())
    access_token_uuid: Mapped[Optional[str]] = mapped_column(String(36))
    access_token_unix_timestamp: Mapped[Optional[int]] = mapped_column(BigInteger())

    # refresh_token: Mapped[str] = mapped_column(String())
    # expired_date: Mapped[DateTime] = mapped_column(DateTime())