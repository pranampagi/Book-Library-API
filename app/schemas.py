from typing import Optional

from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=128)


class UserOut(BaseModel):
    id: int
    username: str
    role: str

    model_config = {"from_attributes": True}


class BookBase(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    author: str = Field(min_length=1, max_length=255)
    isbn: Optional[str] = Field(default=None, max_length=32)
    published_year: Optional[int] = Field(default=None, ge=0, le=3000)
    genre: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = None


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    author: Optional[str] = Field(default=None, min_length=1, max_length=255)
    isbn: Optional[str] = Field(default=None, max_length=32)
    published_year: Optional[int] = Field(default=None, ge=0, le=3000)
    genre: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = None


class BookOut(BookBase):
    id: int
    owner_id: int

    model_config = {"from_attributes": True}


class ExternalBookResult(BaseModel):
    title: str
    authors: list[str]
    isbn: Optional[str] = None
    source: str
