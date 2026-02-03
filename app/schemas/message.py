from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class MessageBase(BaseModel):
    """Базовая схема сообщения."""

    text: str = Field(..., min_length=1, max_length=5000)


class MessageCreate(MessageBase):
    """Схема для создания сообщения."""

    pass


class MessageRead(MessageBase):
    """Схема для чтения данных сообщения."""

    id: int
    chat_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
