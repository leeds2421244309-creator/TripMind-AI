from sqlalchemy import BigInteger, DateTime, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ItineraryDay(Base):
    __tablename__ = "itinerary_days"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    travel_plan_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

    day_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    morning_plan: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    afternoon_plan: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    evening_plan: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        nullable=False
    )