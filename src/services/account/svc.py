from uuid import UUID
import httpx
from core.endpoints import Endpoints as Enp
from core.exception import ExpError
from domain.account.dto import QEmailSignupData
from domain.account.dto import ZAccount


class AccService:
    """Сервис для работы с аккаунтами через внешнее API."""

    def __init__(self, _base_url: str):
        """Инициализирует сервис аккаунтов с базовым URL API.

        Args:
            _base_url (str): Базовый URL API сервиса аккаунтов.
        """
        self.base_url = _base_url

    async def is_email_busy(self, email: str) -> bool:
        """Проверяет, занят ли email в системе.

        Args:
            email (str): Email для проверки.

        Returns:
            bool: True если email уже занят, False если свободен.

        Raises:
            ExpError: Если API возвращает ошибку. Содержит:
                    - code (int): код ошибки
                    - msg (str): сообщение об ошибке
            httpx.RequestError: При проблемах с сетевым соединением.
            ValueError: При некорректном формате ответа API.
        """
        url = self.base_url + Enp.ACCOUNT_IS_EMAIL_BUSY.format(email=email)
        async with httpx.AsyncClient() as client:
            resp = await client.post(url)
            resp_js = resp.json()
            if not resp_js["ok"]:
                raise ExpError(code_msg=(resp_js["err"]["code"], resp_js["err"]["msg"]))
            res = resp_js["payload"]
            return res.get("is_busy", False)

    async def copy_account_from_signup(self, signup: QEmailSignupData) -> UUID:
        """Создает новый аккаунт на основе данных регистрации.

        Args:
            signup (QEmailSignupData): Данные регистрации.

        Returns:
            UUID: Уникальный идентификатор созданного аккаунта.

        Raises:
            ExpError: Если API возвращает ошибку. Содержит:
                    - code (int): код ошибки
                    - msg (str): сообщение об ошибке
            httpx.RequestError: При проблемах с сетевым соединением.
            ValueError: При некорректном формате ответа API.
        """
        url = self.base_url + Enp.ACCOUNT_COPY_FOR_SIGNUP
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=signup.model_dump(mode="json"))
            resp_js = resp.json()
            if not resp_js["ok"]:
                raise ExpError(code_msg=(resp_js["err"]["code"], resp_js["err"]["msg"]))
            res = resp_js["payload"]
            return res.get("id")

    async def get_account_by_email(self, email: str) -> ZAccount:
        """Получает информацию об аккаунте по email.

        Args:
            email (str): Email аккаунта для поиска.

        Returns:
            ZAccount: Объект с полной информацией об аккаунте.

        Raises:
            ExpError: Если API возвращает ошибку. Содержит:
                    - code (int): код ошибки
                    - msg (str): сообщение об ошибке
            httpx.RequestError: При проблемах с сетевым соединением.
            ValueError: При некорректном формате ответа API.
        """
        url = self.base_url + Enp.ACCOUNT_GET_BY_EMAIL.format(email=email)
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            resp_js = resp.json()
            if not resp_js["ok"]:
                raise ExpError(code_msg=(resp_js["err"]["code"], resp_js["err"]["msg"]))
            res = resp_js["payload"]
            return ZAccount.model_validate(res)
