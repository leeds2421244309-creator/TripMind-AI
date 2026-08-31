from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.enums.booking_type import BookingType
from app.enums.payment_status import PaymentStatus


class TravelBooking(Base):
    __tablename__ = "travel_bookings"

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
        back_populates="bookings"
    )

    # ========= 酒店 / 餐厅 / 机票 / 高铁 =========
    booking_type: Mapped[BookingType] = mapped_column(
        Enum(BookingType),
        nullable=False,
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

    phone: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    # ========= 时间 =========
    start_time: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    end_time: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    # ========= 金额 =========
    price: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    payment_status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus),
        default=PaymentStatus.UNDECIDED,
        nullable=False,
    )

    # ========= 图片 =========
    image_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ========= OCR 原文（AI识别出的所有文字）=========
    ocr_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ========= AI解析结果(JSON字符串) =========
    ai_summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # ========= 用户备注 =========
    notes: Mapped[str | None] = mapped_column(
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