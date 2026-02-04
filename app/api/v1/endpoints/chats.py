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
    """Инициализирует новый чат."""
    logger.info(f"Request to create chat with title: '{chat_in.title}'")
    chat = await crud.chat.create(db, obj_in=chat_in)
    logger.info(f"Chat created successfully with id={chat.id}")
    return chat


@router.post(
    "/{chat_id}/messages/",
    response_model=MessageRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_message(
    chat_id: int, message_in: MessageCreate, db: AsyncSession = Depends(get_db)
) -> MessageRead:
    """Публикует сообщение в указанный чат."""
    logger.debug(f"Request to add message to chat_id={chat_id}")

    chat = await crud.chat.get(db, obj_id=chat_id)
    if not chat:
        logger.warning(f"Failed to add message: Chat with id={chat_id} not found")
        raise HTTPException(status_code=404, detail="Chat not found")

    message = await crud.chat.create_message(db, chat_id=chat_id, obj_in=message_in)
    logger.info(f"Message created in chat_id={chat_id}, message_id={message.id}")
    return message


@router.get("/{chat_id}", response_model=ChatWithMessages)
async def get_chat(
    chat_id: int,
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> ChatWithMessages:
    """Загружает историю чата с пагинацией."""
    logger.debug(f"Fetching chat_id={chat_id} with limit={limit}")

    chat = await crud.chat.get_with_messages(db, chat_id=chat_id, limit=limit)
    if not chat:
        logger.warning(f"Chat retrieval failed: Chat with id={chat_id} not found")
        raise HTTPException(status_code=404, detail="Chat not found")

    return chat


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(chat_id: int, db: AsyncSession = Depends(get_db)):
    """Удаляет чат и всю связанную переписку."""
    logger.info(f"Request to delete chat_id={chat_id}")

    chat = await crud.chat.remove(db, obj_id=chat_id)
    if not chat:
        logger.warning(f"Deletion failed: Chat with id={chat_id} not found")
        raise HTTPException(status_code=404, detail="Chat not found")

    logger.info(f"Chat_id={chat_id} and its messages deleted successfully")
    return None
