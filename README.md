# MShop 2.0

An e-commerce API built with **FastAPI** and **PostgreSQL**.

This project is designed for learning backend development, SQL, and application architecture.

---

## Quick Start (Docker)

This is the easiest way to run the project — everything is preconfigured.

### 1. Clone the repository

```bash
git clone https://github.com/your_username/mshop2.0
cd mshop2.0
```
### 2. Create environment variables file

```bash
cp .env.example .env
```

### 3. Start with Docker Compose

```bash
docker-compose up -d --build
```

### 4. Open API documentation

http://localhost:8000/docs

### 5. Stop the application

```bash
docker-compose down
```

## Local Development (without Docker)

If you prefer to run the project locally:

### 1. Install Python 3.10+

Check your version:
```bash
python --version  # Should be 3.10 or higher
```

### 2. Install Poetry and dependencies

```bash
pip install poetry
poetry install
```

### 3. Create .env file inside src directory

```bash
cp src/env.template src/.env
```
Edit src/.env:
```bash
APP_DB__URL=postgresql+asyncpg://postgres:postgres@localhost:5432/mshop
APP_DB__ECHO=1
```

### 4. Generate JWT certificates

```bash
# Make sure openssl is installed (preinstalled on macOS/Linux)
mkdir -p src/certs
openssl genrsa -out src/certs/jwt-private.pem 2048
openssl rsa -in src/certs/jwt-private.pem -outform PEM -pubout -out src/certs/jwt-public.pem
```

### 5. Start PostgreSQL (if not already running)

```bash
docker-compose up -d db
```

### 6. Apply database migrations

```bash
alembic upgrade head
```

### 7. Run the server

```bash
cd src
uvicorn main:app --reload
```

## Tech Stack

- FastAPI — modern Python web framework
- SQLAlchemy 2.0 — async ORM
- Alembic — database migrations
- PostgreSQL — relational database
- Poetry — dependency management
- Docker Compose — container orchestration
- JWT (RS256) — authentication