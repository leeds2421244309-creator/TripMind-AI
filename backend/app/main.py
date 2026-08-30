from fastapi import FastAPI
from sqlalchemy import text

from app.db.database import engine


from app.api.auth import auth

from app.api import ai

from app.api import chat, map,travel

app = FastAPI(
    title="TripMind AI",
    version="1.0.0",
    
)

# app.include_router(
#     travel_plan.router
# )#一次接收一个 Router。

app.include_router(
    auth.router
)#把登录功能安装到服务器。

app.include_router(
    ai.router
)#把 AI 功能安装到服务器。

app.include_router(
    chat.router
)#把聊天功能安装到服务器。

app.include_router(
    map.router
)

app.include_router(
    travel.router
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
