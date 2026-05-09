"""SQLAlchemy ORM models for users and books."""

from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.sqlite import Base


class User(Base):
    """Application user with role-based access and owned books."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user", nullable=False)

    books = relationship("Book", back_populates="owner", cascade="all, delete-orphan")


class Book(Base):
    """Book catalog entry owned by a user."""

    __tablename__ = "books"
    __table_args__ = (UniqueConstraint("owner_id", "isbn", name="uq_owner_isbn"),)

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    author = Column(String, nullable=False, index=True)
    isbn = Column(String, nullable=True, index=True)
    published_year = Column(Integer, nullable=True)
    genre = Column(String, nullable=True)
    description = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    owner = relationship("User", back_populates="books")
