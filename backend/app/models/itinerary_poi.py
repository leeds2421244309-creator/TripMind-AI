from sqlalchemy import BigInteger, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ItineraryPoi(Base):
    __tablename__ = "itinerary_pois"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    itinerary_day_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

    poi_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

    visit_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    visit_time: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    transport: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        nullable=False
    )