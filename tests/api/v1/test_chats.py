import pytest
from httpx import AsyncClient

VALID_CHAT_TITLE = "Test Chat"
VALID_MESSAGE_TEXT = "Hello, World!"


class TestChats:
    """Тесты для управления чатами (CRUD)."""

    @pytest.mark.asyncio
    async def test_create_chat(self, client: AsyncClient):
        """Успешное создание чата."""
        response = await client.post("/api/v1/chats/", json={"title": VALID_CHAT_TITLE})
        assert response.status_code == 201

        data = response.json()
        assert data["title"] == VALID_CHAT_TITLE
        assert isinstance(data["id"], int)
        assert "created_at" in data

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "invalid_title, expected_status",
        [
            ("", 422),  # Пустая строка
            ("   ", 422),  # Только пробелы
            (None, 422),  # Отсутствует поле
        ],
    )
    async def test_create_chat_validation(
        self, client: AsyncClient, invalid_title, expected_status
    ):
        """Валидация при создании чата."""
        payload = {"title": invalid_title} if invalid_title is not None else {}
        response = await client.post("/api/v1/chats/", json=payload)
        assert response.status_code == expected_status

    @pytest.mark.asyncio
    async def test_get_chat(self, client: AsyncClient):
        """Получение существующего чата."""
        # 1. Создаем
        create_res = await client.post("/api/v1/chats/", json={"title": "To Get"})
        chat_id = create_res.json()["id"]

        # 2. Получаем
        response = await client.get(f"/api/v1/chats/{chat_id}")
        assert response.status_code == 200
        assert response.json()["id"] == chat_id

    @pytest.mark.asyncio
    async def test_delete_chat(self, client: AsyncClient):
        """Удаление чата."""
        # 1. Создаем
        create_res = await client.post("/api/v1/chats/", json={"title": "To Delete"})
        chat_id = create_res.json()["id"]

        # 2. Удаляем
        response = await client.delete(f"/api/v1/chats/{chat_id}")
        assert response.status_code == 204

        # 3. Проверяем отсутствие
        get_res = await client.get(f"/api/v1/chats/{chat_id}")
        assert get_res.status_code == 404

    @pytest.mark.asyncio
    async def test_chat_not_found(self, client: AsyncClient):
        """Операции с несуществующим чатом возвращают 404."""
        non_existent_id = 999999

        # GET
        assert (await client.get(f"/api/v1/chats/{non_existent_id}")).status_code == 404
        # DELETE
        assert (
            await client.delete(f"/api/v1/chats/{non_existent_id}")
        ).status_code == 404


class TestMessages:
    """Тесты для работы с сообщениями."""

    @pytest.fixture
    async def chat_id(self, client: AsyncClient) -> int:
        """Фикстура: создает чат и возвращает его ID."""
        res = await client.post("/api/v1/chats/", json={"title": "Message Chat"})
        return res.json()["id"]

    @pytest.mark.asyncio
    async def test_create_message(self, client: AsyncClient, chat_id: int):
        """Успешное создание сообщения."""
        response = await client.post(
            f"/api/v1/chats/{chat_id}/messages/", json={"text": VALID_MESSAGE_TEXT}
        )
        assert response.status_code == 201

        data = response.json()
        assert data["text"] == VALID_MESSAGE_TEXT
        assert data["chat_id"] == chat_id

    @pytest.mark.asyncio
    async def test_get_chat_history_with_pagination(
        self, client: AsyncClient, chat_id: int
    ):
        """Получение истории сообщений с пагинацией (limit)."""
        # Создаем 5 сообщений
        for i in range(5):
            await client.post(
                f"/api/v1/chats/{chat_id}/messages/", json={"text": f"Msg {i}"}
            )

        # Запрашиваем лимит 3
        response = await client.get(f"/api/v1/chats/{chat_id}?limit=3")
        assert response.status_code == 200

        messages = response.json()["messages"]
        assert len(messages) == 3
        # Проверяем структуру сообщения
        assert "text" in messages[0]
        assert "created_at" in messages[0]

    @pytest.mark.asyncio
    async def test_create_message_in_missing_chat(self, client: AsyncClient):
        """Попытка отправить сообщение в несуществующий чат."""
        response = await client.post(
            "/api/v1/chats/999999/messages/", json={"text": "Fail"}
        )
        assert response.status_code == 404

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "invalid_text",
        [
            "",  # Пустое
            "a" * 5001,  # Слишком длинное (>5000)
        ],
    )
    async def test_message_validation(
        self, client: AsyncClient, chat_id: int, invalid_text
    ):
        """Валидация текста сообщения."""
        response = await client.post(
            f"/api/v1/chats/{chat_id}/messages/", json={"text": invalid_text}
        )
        assert response.status_code == 422
