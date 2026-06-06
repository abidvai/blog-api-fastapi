from unittest.mock import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text, func
from app.database.database import Base
from sqlalchemy.orm import relationship


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now(), index=True)
    updated_at = Column(
        DateTime, nullable=False, onupdate=func.now(), server_default=func.now()
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    post_id = Column(
        Integer, ForeignKey("blogs.id", ondelete="CASCADE"), nullable=False
    )

    user = relationship("User", back_populates="comments")
    post = relationship("Blog", back_populates="comments")
