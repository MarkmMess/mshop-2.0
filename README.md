# MShop 2.0

A marketplace-style backend with FastAPI, SQLAlchemy, PostgreSQL, JWT auth, and a lightweight frontend served from the app itself.

---

## Requirements

- Docker Desktop or Docker Engine
- Docker Compose
- Python 3.13+ recommended
- Poetry
- OpenSSL (or Python, to generate the JWT secret)

---

## Run with Docker

This is the simplest way to start the full app.

### 1. Copy environment variables

```bash
cp .env.example .env
```

Generate a JWT secret and put it into `.env`:

```bash
openssl rand -base64 32
```

### 2. Start the app and PostgreSQL

```bash
docker compose up -d --build
```

### 3. Open the app

- Frontend: http://localhost:8000/
- API docs: http://localhost:8000/docs

### 4. Stop it

```bash
docker compose down
```

---

## Local development

### 1. Install dependencies

```bash
pip install poetry
poetry install
```

### 2. Create a secret for JWT

### 2. Create a secret for JWT

Generate a random secret:

```bash
openssl rand -base64 32
```

Copy `.env.example` to `.env` and paste the result into it:

```bash
cp .env.example .env
```

```env
APP_AUTH_JWT__SECRET=<generated string>
```

### 3. Start the database only

```bash
docker compose up -d db
```

### 4. Run the app

From project root:

```bash
poetry run uvicorn src.main:main_app --host 0.0.0.0 --port 8000 --reload
```

Or use the app entrypoint:

```bash
python src/main.py
```

---

## Run tests

The test suite uses the dedicated PostgreSQL container in [docker-compose.test.yml](docker-compose.test.yml).

Start the test database first:

```bash
docker compose -f docker-compose.test.yml up -d
```

Then run the tests:

```bash
pytest
```

### Run one file

```bash
pytest tests/auth/test_api.py
```

### Run one test

```bash
pytest tests/auth/test_api.py -k create_user
```

### Stop the test database

```bash
docker compose -f docker-compose.test.yml down
```

---

## Common fixes

### 1. `ModuleNotFoundError` or missing packages

```bash
poetry install
```

### 2. `Connection refused` to PostgreSQL

Start the database:

```bash
docker compose up -d db
```

Then verify:

```bash
docker compose ps
```

### 3. JWT secret is missing

If the app fails on startup with a settings validation error, `.env` has no JWT secret. Generate one and add it:

```bash
openssl rand -base64 32
```

```env
APP_AUTH_JWT__SECRET=<generated string>
```

### 4. App starts but frontend looks outdated in Safari

This is a cache problem. The app now sends no-store headers and versioned asset URLs. Hard-refresh once:

- Safari: Command + Option + R
- Or open Dev Tools and empty caches

### 5. `uvicorn` cannot find `src.main`

Run from the project root, not inside the `src` folder:

```bash
poetry run uvicorn src.main:main_app --host 0.0.0.0 --port 8000 --reload
```

### 6. Migrations not applied

```bash
poetry run alembic upgrade head
```

---

## Project structure

- `src/main.py` — FastAPI app entrypoint
- `src/api_v1/` — routers and logic for auth, products, profile, categories, stats
- `src/models/` — SQLAlchemy models
- `src/static/` — frontend HTML/CSS/JS served by FastAPI
- `tests/` — API and app tests

---

## Tech stack

- FastAPI
- Async SQLAlchemy
- PostgreSQL
- Alembic
- JWT (HS256)
- Poetry
- Docker Compose
- Uvicorn