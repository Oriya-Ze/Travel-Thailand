from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, Text
from app.db.base import Base


class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    thread_id: Mapped[int] = mapped_column(ForeignKey("threads.id"))
    parent_post_id: Mapped[int | None] = mapped_column(ForeignKey("posts.id"), nullable=True)
    body: Mapped[str] = mapped_column(Text())
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_accepted: Mapped[bool] = mapped_column(default=False)
