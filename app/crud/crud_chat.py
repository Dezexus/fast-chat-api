import logging
from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.crud.base import CRUDBase
from app.models.chat import Chat
from app.models.message import Message
from app.schemas.chat import ChatCreate
from app.schemas.message import MessageCreate

logger = logging.getLogger(__name__)


class CRUDChat(CRUDBase[Chat, ChatCreate]):
    """CRUD операции для чатов."""

    async def create_message(
        self, db: AsyncSession, *, chat_id: int, obj_in: MessageCreate
    ) -> Message:
        """Создает сообщение в чате."""
        logger.debug(f"Inserting new message into DB for chat_id={chat_id}")
        db_obj = Message(chat_id=chat_id, text=obj_in.text)
        db.add(db_obj)
        await db.commit()
        return db_obj

    async def get_with_messages(
        self, db: AsyncSession, chat_id: int, limit: int = 20
    ) -> Any:
        """Возвращает чат с последними сообщениями."""
        # Получаем сам чат
        chat = await self.get(db, chat_id)
        if not chat:
            return None

        logger.debug(f"Querying messages for chat_id={chat_id}, limit={limit}")

        # Получаем сообщения
        stmt = (
            select(Message)
            .filter(Message.chat_id == chat_id)
            .order_by(desc(Message.created_at))
            .limit(limit)
        )
        result = await db.execute(stmt)
        messages = result.scalars().all()

        # Сортируем хронологически для выдачи (старые сверху)
        sorted_messages = sorted(messages, key=lambda x: x.created_at)

        return {
            "id": chat.id,
            "title": chat.title,
            "created_at": chat.created_at,
            "messages": sorted_messages,
        }


chat = CRUDChat(Chat)
