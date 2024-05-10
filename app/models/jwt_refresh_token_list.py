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


class JWTRefreshTokenList(Base):
    __tablename__ = "jwt_refresh_token_list"
    # __table_args__ = {"sqlite_autoincrement": True}

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    token_uuid = mapped_column(String(36))
    token_unix_timestamp = mapped_column(BigInteger())
    # refresh_token: Mapped[str] = mapped_column(String())
    # expired_date: Mapped[DateTime] = mapped_column(DateTime())