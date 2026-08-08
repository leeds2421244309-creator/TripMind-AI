from datetime import datetime

from sqlalchemy import BigInteger, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False
    )

    user_message: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    ai_response: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )