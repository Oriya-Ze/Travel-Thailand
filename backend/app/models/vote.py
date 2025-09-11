from sqlalchemy import ForeignKey, UniqueConstraint, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base


class PostVote(Base):
    __tablename__ = "post_votes"
    __table_args__ = (UniqueConstraint("user_id", "post_id", name="uq_vote"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    value: Mapped[int] = mapped_column(Integer, default=1) # +1 / -1
