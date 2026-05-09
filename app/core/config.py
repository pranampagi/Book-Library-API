"""Application settings loaded from environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Centralized configuration model for API runtime and integrations."""

    app_name: str = "Book Library API"
    log_level: str = "INFO"
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    bootstrap_admin_username: str = "admin"
    bootstrap_admin_password: str = "admin123"

    sqlite_database_url: str = "sqlite:///./library.db"
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_database: str = "book_library"

    google_books_base_url: str = "https://www.googleapis.com/books/v1/volumes"
    open_library_base_url: str = "https://openlibrary.org/search.json"
    cors_allowed_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
