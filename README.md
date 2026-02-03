# FastChat API

Асинхронный REST API для управления чатами и сообщениями.

## Стек
*   **Core:** Python 3.11, FastAPI, Uvicorn
*   **DB:** PostgreSQL, Asyncpg, SQLAlchemy 2.0, Alembic
*   **Infra:** Docker, Docker Compose

## Установка и запуск

1. **Создать файл `.env`** в корне:

   ```ini
   POSTGRES_USER=user
   POSTGRES_PASSWORD=password
   POSTGRES_DB=fastchat
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   DATABASE_URL=postgresql+asyncpg://user:password@db:5432/fastchat
   ```

2. **Запустить проект:**
   ```bash
   docker-compose up -d --build
   ```
   *Миграции применяются автоматически.*

## Использование

Документация (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)

### API Endpoints
*   `POST /api/v1/chats/` — Создать чат.
*   `POST /api/v1/chats/{id}/messages/` — Отправить сообщение.
*   `GET /api/v1/chats/{id}?limit=20` — Получить чат и последние сообщения.
*   `DELETE /api/v1/chats/{id}` — Удалить чат (каскадно).

## Тесты

```bash
docker-compose exec web pytest
```
