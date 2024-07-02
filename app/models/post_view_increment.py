# from datetime import datetime
# from typing import List, Optional, TYPE_CHECKING

# from sqlalchemy import (
#     Integer,
#     String,
#     Boolean,
#     Date,
#     DateTime,
#     ForeignKey,
#     Table,
#     Column,
#     BigInteger,
# )
# from sqlalchemy.orm import Mapped, mapped_column, relationship

# from database.database import Base

# if TYPE_CHECKING:
#     from models.board import Post


# class PostViewIncrement(Base):
#     __tablename__ = "post_view_increment"
#     __table_args__ = {"sqlite_autoincrement": True}
#     id: Mapped[int] = mapped_column(primary_key=True)
#     post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
#     post: Mapped["Post"] = relationship(back_populates="post_view_increments")
    
#     timestamp: Mapped[DateTime] = mapped_column(DateTime(), default=datetime.now)
