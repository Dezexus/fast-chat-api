from typing import List, Annotated
from datetime import datetime
from pydantic import BaseModel, StringConstraints, ConfigDict
from .message import MessageRead


class ChatBase(BaseModel):
    """Базовая схема чата."""

    title: Annotated[
        str, StringConstraints(min_length=1, max_length=200, strip_whitespace=True)
    ]


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
