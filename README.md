# Book Library API

A production-style Book Library API built with FastAPI, SQLAlchemy (SQLite), MongoDB, JWT authentication, and Docker.

## Features

- User registration and JWT login.
- Role-based authorization (`user`, `admin`).
- CRUD operations for books.
- External search integration with Google Books / Open Library.
- SQLite for core relational data and MongoDB for event logging.
- Docker and Docker Compose support.

## Tech Stack

- Python
- FastAPI
- SQLAlchemy + SQLite
- MongoDB (PyMongo)
- Docker

## API Endpoints

### Auth

- `POST /auth/register` - Register a user.
- `POST /auth/token` - Login and get access token.
- `GET /users/me` - Get current user profile.

### Books

- `GET /books` - List books (admin: all books, user: own books).
- `POST /books` - Add a new book.
- `GET /books/{book_id}` - Get one book.
- `PUT /books/{book_id}` - Update a book.
- `DELETE /books/{book_id}` - Delete a book.
- `GET /books/external/search?q=harry+potter&provider=google` - Search external providers.

### Admin

- `GET /admin/users` - List all users (admin only).

## Quickstart (Local)

1. Create and activate a virtual env:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create env file:

   ```bash
   cp .env.example .env
   ```

4. Run API:

   ```bash
   uvicorn app.main:app --reload
   ```

5. Open docs:

   - Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Root endpoint: [http://localhost:8000/](http://localhost:8000/)

## Docker

```bash
cp .env.example .env
docker compose up --build
```

- API: [http://localhost:8000](http://localhost:8000)
- MongoDB: `localhost:27017`

## Testing

```bash
pytest -q
```

## Default Admin User

An admin user is auto-created on startup:

- Username: `admin`
- Password: `admin123`

Change this pattern for production.

## Authentication Flow

1. Register with `/auth/register` (or use default admin).
2. Login via `/auth/token` using form data (`username`, `password`).
3. Copy `access_token` and authorize with `Bearer <token>`.

## Notes

- SQLite is used for primary CRUD records.
- MongoDB is used for book event logs (`book_events` collection).
- For production deployment, use secure secrets and managed database services.
