"""Pydantic request/response models used by API endpoints."""

from typing import Optional

from pydantic import BaseModel, Field


class Token(BaseModel):
    """JWT access token response payload."""

    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    """Payload for registering a new user."""

    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=128)


class UserOut(BaseModel):
    """Public user information returned by the API."""

    id: int
    username: str
    role: str

    model_config = {"from_attributes": True}


class BookBase(BaseModel):
    """Shared fields for book payloads."""

    title: str = Field(min_length=1, max_length=255)
    author: str = Field(min_length=1, max_length=255)
    isbn: Optional[str] = Field(default=None, max_length=32)
    published_year: Optional[int] = Field(default=None, ge=0, le=3000)
    genre: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = None


class BookCreate(BookBase):
    """Payload for creating a new book entry."""


class BookUpdate(BaseModel):
    """Partial payload for updating an existing book entry."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    author: Optional[str] = Field(default=None, min_length=1, max_length=255)
    isbn: Optional[str] = Field(default=None, max_length=32)
    published_year: Optional[int] = Field(default=None, ge=0, le=3000)
    genre: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = None


class BookOut(BookBase):
    """Book response payload returned by CRUD endpoints."""

    id: int
    owner_id: int

    model_config = {"from_attributes": True}


class ExternalBookResult(BaseModel):
    """Normalized result from external book provider lookups."""

    title: str
    authors: list[str]
    isbn: Optional[str] = None
    source: str
