"""Database CRUD helpers for users and books."""

from sqlalchemy.orm import Session

from app.models import Book, User
from app.schemas import BookCreate, BookUpdate
from app.security import get_password_hash


def create_user(db: Session, username: str, password: str, role: str = "user") -> User:
    """Create and persist a new user."""
    user = User(username=username, hashed_password=get_password_hash(password), role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_username(db: Session, username: str) -> User | None:
    """Fetch a user by username."""
    return db.query(User).filter(User.username == username).first()


def create_book(db: Session, book_in: BookCreate, owner_id: int) -> Book:
    """Create and persist a new book for a specific owner."""
    book = Book(**book_in.model_dump(), owner_id=owner_id)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def list_books(db: Session, owner_id: int | None = None) -> list[Book]:
    """List books, optionally filtered by owner."""
    query = db.query(Book)
    if owner_id is not None:
        query = query.filter(Book.owner_id == owner_id)
    return query.order_by(Book.id.desc()).all()


def get_book(db: Session, book_id: int) -> Book | None:
    """Fetch one book by its identifier."""
    return db.query(Book).filter(Book.id == book_id).first()


def update_book(db: Session, book: Book, book_in: BookUpdate) -> Book:
    """Apply partial updates to a book and persist changes."""
    updates = book_in.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(book, key, value)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book: Book) -> None:
    """Delete a book from the database."""
    db.delete(book)
    db.commit()
