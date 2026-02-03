from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import Base


class Chat(Base):
    """Модель чата."""

    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    messages = relationship(
        "Message", back_populates="chat", cascade="all, delete-orphan"
    )
