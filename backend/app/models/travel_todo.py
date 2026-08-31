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
from app.enums.todo_source import TodoSource
from app.enums.todo_status import TodoStatus
from app.enums.todo_type import TodoType


class TravelTodo(Base):
    __tablename__ = "travel_todos"

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
        back_populates="todos",
    )

    # ========= Todo内容 =========
    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # # ========= 分类 =========
    # todo_type: Mapped[TodoType] = mapped_column(
    #     Enum(TodoType),
    #     nullable=False,
    # )

    
    #天数
    day_number: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    # ========= 状态 =========
    status: Mapped[TodoStatus] = mapped_column(
        Enum(TodoStatus),
        default=TodoStatus.TODO,
        nullable=False,
    )

    # ========= 来源 =========
    source: Mapped[TodoSource] = mapped_column(
        Enum(TodoSource),
        default=TodoSource.USER,
        nullable=False,
    )

    # ========= 提醒时间 =========
    deadline: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    # ========= 排序 =========
    sort_order: Mapped[int] = mapped_column(
        Integer,
        default=0,
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