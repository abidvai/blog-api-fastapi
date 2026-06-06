from sqlalchemy import Column, DateTime, Integer, String, func
from app.database.database import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    profile_picture_url = Column(String(255), nullable=True)
    bio = Column(String(500), nullable=True)
    last_login = Column(DateTime, nullable=False, server_default=func.now())
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    password_updated_at = Column(
        DateTime, nullable=True, onupdate=func.now(), server_default=func.now()
    )
    blogs = relationship("Blog", back_populates="user", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")
    comments = relationship(
        "Comment", back_populates="user", cascade="all, delete-orphan"
    )
    view_posts = relationship(
        "ViewPost", back_populates="user", cascade="all, delete-orphan"
    )
