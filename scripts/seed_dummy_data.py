"""
Insert dummy users and books into the configured SQLite database.

Uses the same hashing and models as the FastAPI app.

Run from the project root (with virtualenv activated):

    python -m scripts.seed_dummy_data

Skipped rows when re-running: existing usernames; books already present for
that owner (matched by title + ISBN).
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.crud import create_book, create_user, get_user_by_username
from app.db.sqlite import Base, engine, get_db_session
from app.models import Book
from app.schemas import BookCreate

# Demo passwords (min length 6 per API schema); change for anything beyond local dev.
DUMMY_USERS: list[dict[str, str]] = [
    {"username": "alice", "password": "alice123", "role": "user"},
    {"username": "bob", "password": "bob12345", "role": "user"},
    {"username": "carol", "password": "carol123", "role": "user"},
]

# Each entry: owner username + book fields (ISBN unique per owner due to DB constraint).
DUMMY_BOOKS: list[dict[str, object]] = [
    {
        "owner": "alice",
        "title": "Clean Code",
        "author": "Robert C. Martin",
        "isbn": "9780132350884",
        "published_year": 2008,
        "genre": "Software",
        "description": "Handbook of agile software craftsmanship.",
    },
    {
        "owner": "alice",
        "title": "The Pragmatic Programmer",
        "author": "David Thomas & Andrew Hunt",
        "isbn": "9780135957059",
        "published_year": 2019,
        "genre": "Software",
        "description": "Classic guidance for modern software developers.",
    },
    {
        "owner": "bob",
        "title": "Design Patterns",
        "author": "Gang of Four",
        "isbn": "9780201633612",
        "published_year": 1994,
        "genre": "Software",
        "description": "Elements of reusable object-oriented software.",
    },
    {
        "owner": "bob",
        "title": "Atomic Habits",
        "author": "James Clear",
        "isbn": "9780735211292",
        "published_year": 2018,
        "genre": "Self-help",
        "description": "Tiny changes, remarkable results.",
    },
    {
        "owner": "carol",
        "title": "Project Hail Mary",
        "author": "Andy Weir",
        "isbn": "9780593135204",
        "published_year": 2021,
        "genre": "Science fiction",
        "description": "A lone astronaut races to save Earth.",
    },
    {
        "owner": "carol",
        "title": "The Midnight Library",
        "author": "Matt Haig",
        "isbn": "9780525559481",
        "published_year": 2020,
        "genre": "Fiction",
        "description": "Between life and death lies a library.",
    },
]


def _book_exists(db, owner_id: int, title: str, isbn: str | None) -> bool:
    q = db.query(Book).filter(Book.owner_id == owner_id, Book.title == title)
    if isbn:
        q = q.filter(Book.isbn == isbn)
    return q.first() is not None


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = get_db_session()
    users_created = 0
    books_created = 0
    try:
        for spec in DUMMY_USERS:
            if get_user_by_username(db, spec["username"]):
                continue
            create_user(db, spec["username"], spec["password"], role=spec["role"])
            users_created += 1

        for row in DUMMY_BOOKS:
            owner_name = str(row["owner"])
            user = get_user_by_username(db, owner_name)
            if not user:
                print(f"Skip book (unknown user): {row.get('title')} -> {owner_name}")
                continue
            isbn = row.get("isbn")
            title = str(row["title"])
            if _book_exists(db, user.id, title, str(isbn) if isbn else None):
                continue
            payload = BookCreate(
                title=title,
                author=str(row["author"]),
                isbn=str(isbn) if isbn else None,
                published_year=int(row["published_year"]) if row.get("published_year") is not None else None,
                genre=str(row["genre"]) if row.get("genre") else None,
                description=str(row["description"]) if row.get("description") else None,
            )
            create_book(db, payload, user.id)
            books_created += 1

        print(f"Seed complete: {users_created} user(s) added, {books_created} book(s) added.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
