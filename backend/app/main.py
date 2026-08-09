from fastapi import FastAPI
from sqlalchemy import text

from app.db.database import engine

from app.api import travel_plan
from app.api.auth import auth

app = FastAPI(
    title="TripMind AI",
    version="1.0.0"
)

app.include_router(
    travel_plan.router
)

app.include_router(
    auth.router
)

@app.get("/")
def root():
    return {
        "message": "TripMind AI Backend Running"
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
