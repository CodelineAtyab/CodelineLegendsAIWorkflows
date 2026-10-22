import os

import psycopg
from fastapi import FastAPI, HTTPException

# Inside Compose the host is the service name "db", not localhost.
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://app:app@localhost:5432/app")

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello from Docker!"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/visits")
def visits():
    """Record a visit and return the total, so data persistence can be checked."""
    try:
        with psycopg.connect(DATABASE_URL, connect_timeout=3) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS visits (id SERIAL PRIMARY KEY, visited_at TIMESTAMPTZ DEFAULT now())")
            conn.execute("INSERT INTO visits DEFAULT VALUES")
            total = conn.execute("SELECT COUNT(*) FROM visits").fetchone()[0]
    except psycopg.OperationalError as error:
        raise HTTPException(status_code=503, detail=f"Database unavailable: {error}") from error
    return {"visits": total}
