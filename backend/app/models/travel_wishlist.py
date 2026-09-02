from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    String,
    Text,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TravelWishlist(Base):
    __tablename__ = "travel_wishlists"

    # ========= 主键 =========
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    # ========= 所属旅行 =========
    travel_id: Mapped[int] = mapped_column(
        ForeignKey("travels.id"),
        nullable=False,
    )

    travel = relationship(
        "Travel",
        back_populates="wishlist",
    )

    # ========= 基础信息 =========
    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    address: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ========= 经纬度 =========
    latitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    longitude: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    # ========= 分类 =========
    category: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    # ========= 备注 =========
    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ========= 是否必去 =========
    is_must_visit: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
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
