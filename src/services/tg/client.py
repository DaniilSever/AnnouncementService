from json import JSONDecodeError
import httpx


class TgClient:
    """Реализация TgBot для работы с Telegram ботом."""

    def __init__(self, token, chat_id: str | int):
        """Инициализация TgClient.

        Args:
            token: Токен Telegram бота.
            chat_id: Идентификатор чата или группы.
        """
        self.token = token
        self.chat_id = chat_id

    async def send_message(self, message: str) -> dict:
        """Отправляет сообщение в Telegram чат или группу.

        Args:
            message: Текст сообщения.

        Returns:
            dict: Ответ от Telegram API.

        Raises:
            ValueError: Если произошла ошибка при отправке сообщения.
        """
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        params = {
            "chat_id": self.chat_id,
            "text": message.replace("<br />", ""),
            "parse_mode": "HTML",
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=params)

        try:
            res = response.json()
        except (JSONDecodeError, TypeError, ValueError) as e:
            raise ValueError(str(e)) from e

        if not res.get("ok", False):
            raise ValueError(str(res["error_code"]) + ": " + res["description"])
        return dict(res)
