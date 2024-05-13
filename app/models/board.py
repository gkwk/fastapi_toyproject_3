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
    from models.user_board_table import UserPermissionTable


class Board(Base):
    __tablename__ = "board"
    __table_args__ = {"sqlite_autoincrement": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True)
    users: Mapped[List["User"]] = relationship(
        # class는 table명을 사용한다. class 아닌 table을 사용하면 table 변수를 사용한다.
        secondary="user_board_table",
        back_populates="boards",
    )  # N to M
    information: Mapped[str] = mapped_column(String(512))
    is_visible: Mapped[Boolean] = mapped_column(Boolean(), default=False)
    is_available: Mapped[Boolean] = mapped_column(Boolean(), default=False)
    permission_verified_user_id_range: Mapped[int] = mapped_column(default=0)