from datetime import datetime

from sqlalchemy import BigInteger, Date, DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from datetime import date, datetime

from app.models.budget_item import BudgetItem

class Travel(Base):
    __tablename__ = "travels"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    # 用户ID
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="travels"
    )

    # ===== 基础旅行信息 =====
    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    origin: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    destination: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    goal: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    # ===== 日期 =====
    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    end_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    # ===== 人数预算 =====
    people_count: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    total_budget: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        default="CNY",
        nullable=False,
    )
    budget_mode: Mapped[bool] = mapped_column(
        default=False,
        nullable=False,
    )
    # # ===== 用户偏好 =====
    # preferences: Mapped[str | None] = mapped_column(
    #     Text,
    #     nullable=True,
    # )

    # transport_preference: Mapped[str | None] = mapped_column(
    #     String(50),
    #     nullable=True,
    # )

    # long_transport_preference: Mapped[str | None] = mapped_column(
    #     String(50),
    #     nullable=True,
    # )
    # local_transport_preference: Mapped[str | None] = mapped_column(
    #     String(50),
    #     nullable=True,
    # )

    # notes: Mapped[str | None] = mapped_column(
    #     Text,
    #     nullable=True,
    # )

    # planning / confirmed / traveling / finished
    status: Mapped[str] = mapped_column(
        String(20),
        default="planning",
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

    #预算决策结果
    budget_items: Mapped[list["BudgetItem"]] = relationship(
    "BudgetItem",
    back_populates="travel",
    cascade="all, delete-orphan",
    )
    
    #预定信息
    bookings: Mapped[list["TravelBooking"]] = relationship(
        "TravelBooking",
        back_populates="travel",
        cascade="all, delete-orphan"
    )
    #用户偏好
    preference = relationship(
        "TravelPreference",
        back_populates="travel",
        uselist=False,
        cascade="all, delete-orphan",
    )
        