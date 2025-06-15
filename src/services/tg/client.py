from json import JSONDecodeError
import httpx


class TgClient:
    """Клиент для взаимодействия с Telegram Bot API."""

    def __init__(self, token, chat_id: str | int):
        """Инициализирует клиент Telegram бота.

        Args:
            token (str): Токен бота, полученный от @BotFather.
            chat_id (str | int): ID чата/канала для отправки сообщений.
                              Может быть числовым ID или username (для публичных чатов).
        """
        self.token = token
        self.chat_id = chat_id

    async def send_message(self, message: str) -> dict:
        """Отправляет форматированное сообщение в Telegram чат.

        Args:
            message (str): Текст сообщения. Поддерживается HTML-разметка.
                        Автоматически очищается от тегов <br />.

        Returns:
            dict: Ответ Telegram API в формате JSON с информацией об отправке.

        Raises:
            ValueError: Если возникла ошибка при:
                      - обработке ответа API
                      - API вернуло статус ошибки
            httpx.RequestError: Если произошла сетевая ошибка при запросе.
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
