from sqlalchemy.orm import Session

from app.models import Book, User
from app.schemas import BookCreate, BookUpdate
from app.security import get_password_hash


def create_user(db: Session, username: str, password: str, role: str = "user") -> User:
    user = User(username=username, hashed_password=get_password_hash(password), role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def create_book(db: Session, book_in: BookCreate, owner_id: int) -> Book:
    book = Book(**book_in.model_dump(), owner_id=owner_id)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def list_books(db: Session, owner_id: int | None = None) -> list[Book]:
    query = db.query(Book)
    if owner_id is not None:
        query = query.filter(Book.owner_id == owner_id)
    return query.order_by(Book.id.desc()).all()


def get_book(db: Session, book_id: int) -> Book | None:
    return db.query(Book).filter(Book.id == book_id).first()


def update_book(db: Session, book: Book, book_in: BookUpdate) -> Book:
    updates = book_in.model_dump(exclude_unset=True)
    for key, value in updates.items():
        setattr(book, key, value)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book: Book) -> None:
    db.delete(book)
    db.commit()
