from datetime import datetime

from sqlalchemy import BigInteger, Date, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TravelPlan(Base):
    __tablename__ = "travel_plans"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    destination: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    start_date: Mapped[datetime] = mapped_column(
        Date,
        nullable=False
    )

    days: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    budget: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )

    people_count: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False
    )

    interests: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    transportation: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )