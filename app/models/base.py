from typing import Any
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Базовый класс для моделей SQLAlchemy."""

    id: Any
    __name__: str

    @property
    def __tablename__(self) -> str:
        """Генерирует имя таблицы на основе имени класса."""
        return self.__name__.lower() + "s"
