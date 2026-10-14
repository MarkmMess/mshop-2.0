# MShop 2.0

A marketplace-style backend with FastAPI, SQLAlchemy, PostgreSQL, JWT auth, and a lightweight frontend served from the app itself.

---

## Requirements

- Docker Desktop or Docker Engine
- Docker Compose
- Python 3.13+ recommended
- Poetry
- OpenSSL

---

## Run with Docker

This is the simplest way to start the full app.

### 1. Copy environment variables

```bash
cp .env.example .env
```

If the repository does not include `.env.example`, create a `.env` file with:

```env
APP_DB__URL=postgresql+asyncpg://postgres:postgres@db:5432/mshop
APP_DB__ECHO=0
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

### 2. Create certificates for JWT

```bash
mkdir -p src/certs
openssl genrsa -out src/certs/jwt-private.pem 2048
openssl rsa -in src/certs/jwt-private.pem -outform PEM -pubout -out src/certs/jwt-public.pem
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

### 3. JWT certificates missing

```bash
mkdir -p src/certs
openssl genrsa -out src/certs/jwt-private.pem 2048
openssl rsa -in src/certs/jwt-private.pem -outform PEM -pubout -out src/certs/jwt-public.pem
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
- JWT (RS256)
- Poetry
- Docker Compose
- Uvicorn