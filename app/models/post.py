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
    from models.post_file import PostFile
    from models.comment import Comment
    # from models.post_view_increment import PostViewIncrement


class Post(Base):
    __tablename__ = "post"
    __table_args__ = {"sqlite_autoincrement": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="posts")
    board_id: Mapped[int] = mapped_column(ForeignKey("board.id"))
    board: Mapped["Board"] = relationship(back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship(
        back_populates="post", cascade="all, delete"
    )
    # post_view_increments: Mapped[List["PostViewIncrement"]] = relationship(
    #     back_populates="post", cascade="all, delete"
    # )

    name: Mapped[str] = mapped_column(String(64))
    content: Mapped[str] = mapped_column(String(1024))
    create_date: Mapped[DateTime] = mapped_column(DateTime(), default=datetime.now)
    update_date: Mapped[Optional[DateTime]] = mapped_column(
        DateTime(), onupdate=datetime.now
    )
    number_of_view: Mapped[int] = mapped_column(Integer(), default=0)
    number_of_comment: Mapped[int] = mapped_column(Integer(), default=0)
    # number_of_like: Mapped[int] = mapped_column(Integer(), default=0)
    is_file_attached: Mapped[Boolean] = mapped_column(Boolean(), default=False)
    attached_files: Mapped[List["PostFile"]] = relationship(
        back_populates="post", cascade="all, delete"
    )
    is_visible: Mapped[Boolean] = mapped_column(Boolean(), default=True)
