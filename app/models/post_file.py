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
    from models.user import User
    from models.post import Post

class PostFile(Base):
    __tablename__ = "post_file"
    # __table_args__ = {"sqlite_autoincrement": True}

    post: Mapped["Post"] = relationship(back_populates="attached_files")
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), primary_key=True)
    board_id: Mapped[int] = mapped_column(ForeignKey("board.id"), primary_key=True)
    file_uuid_name: Mapped[str] = mapped_column(String(), primary_key=True)
    file_original_name: Mapped[str] = mapped_column(String())
    file_path: Mapped[str] = mapped_column(String())
    create_date: Mapped[DateTime] = mapped_column(DateTime(), default=datetime.now)