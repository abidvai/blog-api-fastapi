from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from app.database.database import Base
from sqlalchemy.orm import relationship


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), index=True, nullable=False)
    content = Column(Text, nullable=False)
    blog_photo = Column(String(255), nullable=True, default="")
    created_at = Column(DateTime, nullable=False, server_default=func.now(), index=True)
    updated_at = Column(
        DateTime, nullable=False, onupdate=func.now(), server_default=func.now()
    )
    is_deleted = Column(Boolean, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    user = relationship("User", back_populates="blogs")
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")
    comments = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan"
    )
    view_posts = relationship(
        "ViewPost", back_populates="post", cascade="all, delete-orphan"
    )

    @property
    def likes_count(self) -> int:
        try:
            return len(self.likes)
        except Exception:
            return 0

    @property
    def comments_count(self) -> int:
        try:
            return len(self.comments)
        except Exception:
            return 0

    @property
    def views_count(self) -> int:
        try:
            return len(self.view_posts)
        except Exception:
            return 0

