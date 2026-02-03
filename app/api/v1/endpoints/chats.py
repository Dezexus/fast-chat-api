import logging
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core.db import get_db
from app.schemas.chat import ChatCreate, ChatRead, ChatWithMessages
from app.schemas.message import MessageCreate, MessageRead

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=ChatRead, status_code=status.HTTP_201_CREATED)
async def create_chat(
    chat_in: ChatCreate, db: AsyncSession = Depends(get_db)
) -> ChatRead:
    """Создает новый чат."""
    logger.info(f"Request to create chat with title: '{chat_in.title}'")
    chat = await crud.chat.create(db, obj_in=chat_in)
    logger.info(f"Chat created successfully with id={chat.id}")
    return chat


@router.post(
    "/{id}/messages/", response_model=MessageRead, status_code=status.HTTP_201_CREATED
)
async def create_message(
    id: int, message_in: MessageCreate, db: AsyncSession = Depends(get_db)
) -> MessageRead:
    """Добавляет сообщение в указанный чат."""
    logger.debug(f"Request to add message to chat_id={id}")

    chat = await crud.chat.get(db, id=id)
    if not chat:
        logger.warning(f"Failed to add message: Chat with id={id} not found")
        raise HTTPException(status_code=404, detail="Chat not found")

    message = await crud.chat.create_message(db, chat_id=id, obj_in=message_in)
    logger.info(f"Message created in chat_id={id}, message_id={message.id}")
    return message


@router.get("/{id}", response_model=ChatWithMessages)
async def get_chat(
    id: int, limit: int = Query(20, ge=1, le=100), db: AsyncSession = Depends(get_db)
) -> ChatWithMessages:
    """Возвращает информацию о чате и последние сообщения."""
    logger.debug(f"Fetching chat_id={id} with limit={limit}")

    chat = await crud.chat.get_with_messages(db, chat_id=id, limit=limit)
    if not chat:
        logger.warning(f"Chat retrieval failed: Chat with id={id} not found")
        raise HTTPException(status_code=404, detail="Chat not found")

    return chat


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(id: int, db: AsyncSession = Depends(get_db)):
    """Удаляет чат и все связанные сообщения."""
    logger.info(f"Request to delete chat_id={id}")

    chat = await crud.chat.remove(db, id=id)
    if not chat:
        logger.warning(f"Deletion failed: Chat with id={id} not found")
        raise HTTPException(status_code=404, detail="Chat not found")

    logger.info(f"Chat_id={id} and its messages deleted successfully")
    return None
