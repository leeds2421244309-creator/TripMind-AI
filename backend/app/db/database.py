import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.db.base import Base

load_dotenv()

# ========= 数据库配置 =========
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = (
    f"mysql+pymysql://"
    f"{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/"
    f"{DB_NAME}"
)

# ========= Engine 连接MySQL=========
engine = create_engine(
    DATABASE_URL,
    echo=True,          # 开发阶段打印 SQL
    pool_pre_ping=True  # 自动检测数据库连接是否失效
)

# ========= Session 工厂，每次请求创建一个session =========
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# ========= 所有 Model 的基类 =========
# Base = declarative_base()


# ========= FastAPI 数据库依赖 =========
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()