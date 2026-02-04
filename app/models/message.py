import datetime

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from . import Chat
from .base import Base


class Message(Base):
    """Модель сообщения"""

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    chat_id: Mapped[int] = mapped_column(
        ForeignKey("chats.id", ondelete="CASCADE"), nullable=False
    )

    text: Mapped[str] = mapped_column(String(5000), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    chat: Mapped["Chat"] = relationship(back_populates="messages")
