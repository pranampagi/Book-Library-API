# Book Library App (Client + Server)

A complete client-server book library application:

- **Backend Server:** FastAPI + SQLAlchemy + SQLite + MongoDB event logging
- **Frontend Client:** Vue 3 + Vite (separate app)
- **Communication:** HTTP API with JWT bearer auth

The backend and frontend run as independent services and can be started separately or together.

## Architecture

- **Client (`frontend/`)** handles UI and user interaction.
- **Server (`app/`)** handles authentication, authorization, business logic, and persistence.
- **Database Layer:** SQLite for core records, MongoDB for optional event logs.

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

## Local Development

### 1) Start the backend server

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

Backend runs on [http://127.0.0.1:8000](http://127.0.0.1:8000)

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Root endpoint: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### 2) Start the frontend client

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

Frontend runs on [http://127.0.0.1:5173](http://127.0.0.1:5173)

## Docker Compose (Full Stack)

```bash
cp .env.example .env
docker compose up --build
```

- Backend API: [http://localhost:8000](http://localhost:8000)
- Frontend client: [http://localhost:5173](http://localhost:5173)
- MongoDB: `localhost:27017`

## Frontend Environment

- `VITE_API_BASE_URL` (default: `http://127.0.0.1:8000`)

## Default Admin User

An admin user is auto-created on startup:

- Username: `admin`
- Password: set from `.env` (`BOOTSTRAP_ADMIN_PASSWORD`)

Change this pattern for production.

## Authentication Flow

1. Register with `/auth/register` (or use default admin).
2. Login via `/auth/token` using form data (`username`, `password`).
3. Copy `access_token` and authorize with `Bearer <token>`.

## Testing

### Backend tests

```bash
pytest -q
```

### Frontend build check

```bash
cd frontend
npm run build
```

## Notes

- SQLite is used for primary CRUD records.
- MongoDB is used for book event logs (`book_events` collection).
- CORS is enabled for frontend origins on port `5173`.
- For production deployment, use secure secrets and managed database services.
