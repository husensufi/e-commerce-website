# ── Stage: Runtime ────────────────────────────────────────────────────────────
FROM python:3.11-slim

# System deps needed by psycopg (libpq) and bcrypt (gcc)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first (cached layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Alembic config + migrations
COPY alembic.ini .
COPY alembic/ ./alembic/

# Copy application source
COPY src/ ./src/

# Make sure Python can find all local modules
ENV PYTHONPATH=/app/src

EXPOSE 8000

# 1. Run Alembic migrations (will be skipped silently if DB not ready — lifespan handles fallback)
# 2. Start the FastAPI app with hot-reload (--reload works with volume mount)
CMD ["sh", "-c", "alembic upgrade head && cd /app/src && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]
