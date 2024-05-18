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
    from models.comment import Comment
    
class CommentFile(Base):
    __tablename__ = "comment_file"
    # __table_args__ = {"sqlite_autoincrement": True}

    comment: Mapped["Comment"] = relationship(back_populates="attached_files")
    comment_id: Mapped[int] = mapped_column(ForeignKey("comment.id"), primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), primary_key=True)
    file_uuid_name: Mapped[str] = mapped_column(String(), primary_key=True)
    file_original_name: Mapped[str] = mapped_column(String())
    file_path: Mapped[str] = mapped_column(String())
    create_date: Mapped[DateTime] = mapped_column(DateTime(), default=datetime.now)
