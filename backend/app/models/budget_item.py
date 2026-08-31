from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from sqlalchemy import Enum
from app.enums.payment_status import PaymentStatus

class BudgetItem(Base):
    __tablename__ = "budget_items"

    # ===== 主键 =====
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
    )

    # ===== 所属旅行 =====
    travel_id: Mapped[int] = mapped_column(
        ForeignKey("travels.id"),
        nullable=False,
    )

    travel: Mapped["Travel"] = relationship(
        "Travel",
        back_populates="budget_items"
    )

    # ===== 默认预算 / 用户新增 =====
    budget_type: Mapped[str] = mapped_column(
        String(20),
        default="custom",      # default / custom
        nullable=False,
    )

    # ===== 分类 =====
    category: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    # ===== 项目名称 =====
    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # ===== 单价（每天 / 每晚 / 单次）=====
    unit_cost: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    # ===== 数量（天数 / 晚数 / 次数）=====
    quantity: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    # ===== 自动计算金额 =====
    estimated_cost: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    # ===== 支付状态 =====
    # payment_status: Mapped[str] = mapped_column(
    #     String(20),
    #     default="pending",   # pending / paid / undecided / cancelled
    #     nullable=False,
    # )
    # payment_status:
    # paid 已支付
    # pending 待支付
    # undecided 未决定
    # cancelled 已取消
    payment_status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus),
        default=PaymentStatus.PENDING,
        nullable=False,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )