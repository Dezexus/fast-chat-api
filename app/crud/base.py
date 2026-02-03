from typing import Any, Generic, Type, TypeVar, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=Any)


class CRUDBase(Generic[ModelType, CreateSchemaType]):
    """Базовый класс для CRUD операций."""

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """Возвращает запись по ID."""
        return await db.get(self.model, id)

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """Создает новую запись."""
        obj_data = obj_in.model_dump()
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        await db.commit()
        return db_obj

    async def remove(self, db: AsyncSession, *, id: int) -> Optional[ModelType]:
        """Удаляет запись по ID."""
        obj = await db.get(self.model, id)
        if obj:
            await db.delete(obj)
            await db.commit()
        return obj
