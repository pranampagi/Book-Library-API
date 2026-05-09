"""Integrations with external book metadata providers."""

import httpx

from app.core.config import settings
from app.schemas import ExternalBookResult


async def search_google_books(query: str, limit: int = 5) -> list[ExternalBookResult]:
    """Search Google Books and normalize results to internal schema."""
    params = {"q": query, "maxResults": limit}
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(settings.google_books_base_url, params=params)
        response.raise_for_status()
        payload = response.json()

    books: list[ExternalBookResult] = []
    for item in payload.get("items", []):
        volume = item.get("volumeInfo", {})
        identifiers = volume.get("industryIdentifiers", [])
        isbn = None
        for ident in identifiers:
            if ident.get("type", "").startswith("ISBN"):
                isbn = ident.get("identifier")
                break
        books.append(
            ExternalBookResult(
                title=volume.get("title", "Unknown"),
                authors=volume.get("authors", []),
                isbn=isbn,
                source="google_books",
            )
        )
    return books


async def search_open_library(query: str, limit: int = 5) -> list[ExternalBookResult]:
    """Search Open Library and normalize results to internal schema."""
    params = {"q": query, "limit": limit}
    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(settings.open_library_base_url, params=params)
        response.raise_for_status()
        payload = response.json()

    books: list[ExternalBookResult] = []
    for doc in payload.get("docs", []):
        isbn_values = doc.get("isbn", [])
        books.append(
            ExternalBookResult(
                title=doc.get("title", "Unknown"),
                authors=doc.get("author_name", []),
                isbn=isbn_values[0] if isbn_values else None,
                source="open_library",
            )
        )
    return books
