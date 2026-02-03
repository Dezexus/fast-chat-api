from typing import List
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, ConfigDict
from .message import MessageRead


class ChatBase(BaseModel):
    """Базовая схема чата."""

    title: str = Field(..., min_length=1, max_length=200)

    @field_validator("title", mode="before")
    @classmethod
    def trim_title(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip()
        return v


class ChatCreate(ChatBase):
    """Схема для создания чата."""

    pass


class ChatRead(ChatBase):
    """Схема для чтения данных чата."""

    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class ChatWithMessages(ChatRead):
    """Схема чата с сообщениями."""

    messages: List[MessageRead] = []
