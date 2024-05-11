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


class JWTAccessTokenBlackList(Base):
    __tablename__ = "jwt_access_token_blacklist"
    # __table_args__ = {"sqlite_autoincrement": True}

    user_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    access_token_uuid: Mapped[str] = mapped_column(String(36), primary_key=True)
    access_token_unix_timestamp: Mapped[DateTime] = mapped_column(BigInteger(), primary_key=True, autoincrement=False)
