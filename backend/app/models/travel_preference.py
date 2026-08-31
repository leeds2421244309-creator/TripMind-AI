from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Integer,
    Text,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TravelPreference(Base):
    __tablename__ = "travel_preferences"

    # ========= 主键 =========
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    # ========= 所属旅行（一对一） =========
    travel_id: Mapped[int] = mapped_column(
        ForeignKey("travels.id"),
        nullable=False,
        unique=True,
    )

    travel = relationship(
        "Travel",
        back_populates="preference",
    )

    # ========= 🏨 酒店偏好 =========
    hotel_budget_per_night: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    hotel_prompt: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ========= 🍜 美食偏好 =========
    food_budget_per_meal: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    food_prompt: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ========= ✈️ 城市间交通 =========
    transport_prompt: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ========= 🚇 市内交通 =========
    local_transport_prompt: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )