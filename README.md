# MShop 2.0

A marketplace-style backend with FastAPI, SQLAlchemy, PostgreSQL, JWT auth, and a lightweight frontend served from the app itself.

Works on Windows, macOS, and Linux.

---

## Requirements

- Docker Desktop (Windows / macOS) or Docker Engine (Linux)
- Docker Compose (included in Docker Desktop)
- Python 3.13+ (only needed for local development and for generating the JWT secret)
- Poetry (only needed for local development)

> **Note:** OpenSSL is **not** required. The JWT secret is generated with Python.

### Which Python command do I use?

| OS | Command |
|---|---|
| Windows | `py` (or `python`) |
| macOS / Linux | `python3` (or `python`) |

The examples below use `python`. Replace it with the command that works on your system.

---

## Step 0. Create the `.env` file (all OSes)

Pick the command for your shell:

**Windows (PowerShell):**
```powershell
Copy-Item .env.example .env
```

**Windows (cmd):**
```bat
copy .env.example .env
```

**macOS / Linux / Git Bash:**
```bash
cp .env.example .env
```

Or just copy the file manually in your file manager and rename the copy to `.env`.

## Step 1. Generate a JWT secret (all OSes)

Run this one-liner (same on every OS):

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the printed string and put it into `.env`:

```env
APP_AUTH_JWT__SECRET=<generated string>
```

Alternatives (optional):

- macOS / Linux / Git Bash: `openssl rand -base64 32`
- Windows PowerShell (no OpenSSL needed):
  ```powershell
  [Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))
  ```

---

## Run with Docker

The simplest way to start the full app. Complete **Step 0** and **Step 1** first.

### 1. Start the app and PostgreSQL

```bash
docker compose up -d --build
```

> Older Docker installs may need `docker-compose` (with a hyphen) instead of `docker compose`.

### 2. Open the app

- Frontend: http://localhost:8000/
- API docs: http://localhost:8000/docs

### 3. Stop it

```bash
docker compose down
```

---

## Local development

Complete **Step 0** and **Step 1** first.

### 1. Install dependencies

```bash
python -m pip install poetry
python -m poetry install
```

> Using `python -m poetry` works even if the `poetry` command is not in your PATH (common on Windows).

### 2. Start the database only

```bash
docker compose up -d db
```

### 3. Apply migrations

```bash
python -m poetry run alembic upgrade head
```

### 4. Run the app

From the project root:

```bash
python -m poetry run uvicorn src.main:main_app --host 0.0.0.0 --port 8000 --reload
```

Or use the app entrypoint:

```bash
python -m poetry run python src/main.py
```

---

## Run tests

The test suite uses the dedicated PostgreSQL container from [docker-compose.test.yml](docker-compose.test.yml).

Start the test database:

```bash
docker compose -f docker-compose.test.yml up -d
```

Run the tests:

```bash
python -m poetry run pytest
```

### Run one file

```bash
python -m poetry run pytest tests/auth/test_api.py
```

### Run one test

```bash
python -m poetry run pytest tests/auth/test_api.py -k create_user
```

### Stop the test database

```bash
docker compose -f docker-compose.test.yml down
```

---

## Common fixes

### 1. `cp` / `openssl` is not recognized (Windows)

These are Unix tools. Use the cross-platform commands from **Step 0** and **Step 1** instead (`Copy-Item` / `copy` and the Python one-liner).

### 2. `python` / `poetry` is not recognized

- Windows: try `py` instead of `python`, and use `py -m poetry ...`.
- macOS / Linux: try `python3`.
- Make sure Python was installed with "Add Python to PATH" checked (Windows).

### 3. `ModuleNotFoundError` or missing packages

```bash
python -m poetry install
```

### 4. `Connection refused` to PostgreSQL

Start the database and verify it is running:

```bash
docker compose up -d db
docker compose ps
```

On Windows / macOS make sure Docker Desktop is running.

### 5. JWT secret is missing

If the app fails on startup with a settings validation error, `.env` has no JWT secret. Generate one (see Step 1) and add it:

```env
APP_AUTH_JWT__SECRET=<generated string>
```

Make sure the file is named exactly `.env` (not `.env.txt`). On Windows, enable "File name extensions" in Explorer to check.

### 6. Frontend looks outdated

This is a browser cache problem. Hard-refresh once:

- Windows / Linux: `Ctrl + Shift + R`
- macOS Chrome / Firefox: `Cmd + Shift + R`
- macOS Safari: `Cmd + Option + R`

### 7. `uvicorn` cannot find `src.main`

Run from the project root, not from inside `src`:

```bash
python -m poetry run uvicorn src.main:main_app --host 0.0.0.0 --port 8000 --reload
```

### 8. Migrations not applied

```bash
python -m poetry run alembic upgrade head
```

### 9. Port 8000 or 5432 is already in use

Stop the other program using the port, or change the port mapping in `docker-compose.yml`.

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
- Pytest
- Docker Compose
- Uvicorn