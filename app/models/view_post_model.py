from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from app.database.database import Base
from sqlalchemy.orm import relationship


class ViewPost(Base):
    __tablename__ = "view_posts"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(
        Integer, ForeignKey("blogs.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    ip_address = Column(String(100), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now(), index=True)

    user = relationship("User", back_populates="view_posts")
    post = relationship("Blog", back_populates="view_posts")

    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="unique_user_post_view"),
    )
