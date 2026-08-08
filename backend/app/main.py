from fastapi import FastAPI
from sqlalchemy import text

from app.db.database import engine

app = FastAPI(
    title="TripMind AI",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to TripMind AI"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/health/database")
def database_health():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "database": "connected"
        }

    except Exception as e:
        return {
            "database": "error",
            "detail": str(e)
        }
