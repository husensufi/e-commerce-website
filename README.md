# FastAPI React E-Commerce

A full-stack e-commerce application built with **FastAPI** (Python) + **React** (Vite), backed by **PostgreSQL**.

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI 0.88, Python 3.10+ |
| Database | PostgreSQL 15 |
| ORM | SQLAlchemy 2.x (async) |
| DB Driver | Psycopg v3 (`psycopg[asyncio]`) |
| Migrations | Alembic |
| Auth | JWT (python-jose) + bcrypt (passlib) |
| Frontend | React 18, Vite, TailwindCSS |
| DB Admin | pgAdmin 4 (port 8081) |

---

## Quick Start

### 1. Prerequisites
- Docker & Docker Compose
- Python 3.10+
- Node.js 18+

### 2. Environment

Copy the example file and fill in values (defaults work out of the box with Docker):
```bash
cp .env.example .env
```

### 3. Start PostgreSQL & pgAdmin
```bash
docker-compose up -d
```

- **PostgreSQL** → `localhost:5432`
- **pgAdmin** → http://localhost:8081 (email: `admin@admin.com`, password: `admin`)

### 4. Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run Alembic migrations (creates tables)
cd ..
alembic -c backend/alembic.ini upgrade head

# Start the API server
cd backend/src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API docs → http://localhost:8000/docs

### 5. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend → http://localhost:5173

---

## API Endpoints

### Auth
| Method | Path | Description |
|---|---|---|
| POST | `/auth/signup` | Register a new user |
| POST | `/auth/login` | Login and get JWT token |

### Products
| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/products/` | List all products |
| GET | `/api/v1/products/{id}` | Get product by UUID |
| POST | `/api/v1/products/` | Create a product |
| PUT | `/api/v1/products/{id}` | Update a product |
| DELETE | `/api/v1/products/{id}` | Delete a product |

---

## Database Migrations (Alembic)

All commands run from the `backend/` directory:

```bash
# Apply all pending migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Auto-generate a new migration after model changes
alembic revision --autogenerate -m "description of change"

# View migration history
alembic history
```

---

## Project Structure

```
fastapi-react-ecommerce/
├── .env                        # Local environment variables
├── .env.example                # Template
├── docker-compose.yml          # PostgreSQL + pgAdmin
├── backend/
│   ├── alembic.ini             # Alembic configuration
│   ├── alembic/
│   │   ├── env.py              # Async migration runner
│   │   ├── script.py.mako      # Migration template
│   │   └── versions/
│   │       └── 0001_initial.py # Initial schema migration
│   ├── requirements.txt
│   └── src/
│       ├── main.py
│       ├── app.py              # FastAPI app factory + lifespan
│       ├── config/             # Env-based settings
│       ├── database/           # Async engine + get_db dependency
│       ├── models/
│       │   ├── common.py       # SQLAlchemy Base + TimestampMixin
│       │   ├── products.py     # ProductTable ORM + Pydantic schemas
│       │   └── users.py        # UserTable ORM + Pydantic schemas
│       ├── routers/
│       │   ├── products.py     # CRUD endpoints
│       │   └── users.py        # Users router (stub)
│       ├── auth/
│       │   ├── router.py       # /auth/login + /auth/signup
│       │   └── utils.py        # JWT + bcrypt helpers
│       └── middlewares/
│           └── cors.py
└── frontend/
    └── src/
        ├── services/           # API service classes
        ├── pages/              # Home, Product, Login
        └── components/         # Layout, Header, Products
```