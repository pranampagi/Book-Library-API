"""FastAPI application entrypoint and route definitions."""

import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud, external, schemas
from app.core.config import settings
from app.core.logging_config import setup_logging
from app.db.mongo import get_mongo_db
from app.db.sqlite import Base, engine, get_db, get_db_session
from app.models import User
from app.security import (
    create_access_token,
    get_current_user,
    require_admin,
    verify_password,
)


setup_logging(settings.log_level)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Initialize database schema and bootstrap admin account at startup."""
    Base.metadata.create_all(bind=engine)
    db = get_db_session()
    try:
        admin = crud.get_user_by_username(db, settings.bootstrap_admin_username)
        if not admin:
            crud.create_user(
                db,
                settings.bootstrap_admin_username,
                settings.bootstrap_admin_password,
                role="admin",
            )
            logger.info("Bootstrap admin user created")
    finally:
        db.close()
    yield


app = FastAPI(title=settings.app_name, version="1.0.0", lifespan=lifespan)

cors_origins = [
    origin.strip()
    for origin in settings.cors_allowed_origins.split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Return a simple service status payload with useful links."""
    return {
        "message": "Book Library API is running",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health_check():
    """Report API health and MongoDB reachability."""
    mongo_status = "ok"
    try:
        get_mongo_db().command("ping")
    except Exception as exc:
        logger.warning("MongoDB health check failed: %s", exc)
        mongo_status = "unavailable"
    return {"status": "ok", "mongo": mongo_status}


@app.post("/auth/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user account."""
    existing = crud.get_user_by_username(db, user_in.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    return crud.create_user(db, user_in.username, user_in.password)


@app.post("/auth/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """Authenticate a user and return an access token."""
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    token = create_access_token(subject=user.username)
    return schemas.Token(access_token=token)


@app.get("/users/me", response_model=schemas.UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    """Return profile details for the authenticated user."""
    return current_user


@app.get("/books", response_model=list[schemas.BookOut])
def get_books(
    mine_only: bool = Query(default=False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List books visible to the authenticated user."""
    owner_id = current_user.id if mine_only or current_user.role != "admin" else None
    return crud.list_books(db, owner_id=owner_id)


@app.post("/books", response_model=schemas.BookOut, status_code=status.HTTP_201_CREATED)
def create_book(
    book_in: schemas.BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new book entry for the authenticated user."""
    try:
        book = crud.create_book(db, book_in, current_user.id)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409, detail="A book with this ISBN already exists for this user"
        )

    # Optional metadata persistence in MongoDB for analytics/audit.
    try:
        mongo_db = get_mongo_db()
        mongo_db.book_events.insert_one(
            {"event": "book_created", "book_id": book.id, "owner_id": current_user.id}
        )
    except Exception as exc:
        logger.warning("Mongo book event insert failed: %s", exc)
    return book


@app.get("/books/external/search", response_model=list[schemas.ExternalBookResult])
async def external_search(
    q: str = Query(..., min_length=2),
    provider: str = Query(default="google", pattern="^(google|openlibrary)$"),
    current_user: User = Depends(get_current_user),
):
    """Search external providers for book metadata."""
    _ = current_user
    if provider == "google":
        return await external.search_google_books(q)
    return await external.search_open_library(q)


@app.get("/books/{book_id}", response_model=schemas.BookOut)
def get_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Return one book if the user is authorized to access it."""
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if current_user.role != "admin" and book.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return book


@app.put("/books/{book_id}", response_model=schemas.BookOut)
def update_book(
    book_id: int,
    book_in: schemas.BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update one book if the user is authorized to modify it."""
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if current_user.role != "admin" and book.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    return crud.update_book(db, book, book_in)


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete one book if the user is authorized to remove it."""
    book = crud.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if current_user.role != "admin" and book.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    crud.delete_book(db, book)
    return None


@app.get("/admin/users", response_model=list[schemas.UserOut])
def list_users(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    """List all registered users (admin only)."""
    return db.query(User).order_by(User.id.desc()).all()
