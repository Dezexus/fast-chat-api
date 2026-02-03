from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base


class Message(Base):
    """Модель сообщения."""

    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(
        Integer, ForeignKey("chats.id", ondelete="CASCADE"), nullable=False
    )
    text = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    chat = relationship("Chat", back_populates="messages")
