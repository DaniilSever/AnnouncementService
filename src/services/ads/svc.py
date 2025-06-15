from uuid import UUID
import httpx
from core.endpoints import Endpoints as Enp
from core.exception import ExpError


class AdsService:
    """Сервис для работы с объявлениями через внешнее API."""

    def __init__(self, _base_url: str):
        """Инициализирует сервис объявлений с базовым URL API.

        Args:
            _base_url (str): Базовый URL API сервиса объявлений.
        """
        self.base_url = _base_url

    async def get_count_ads_by_acc_id(self, acc_id: UUID) -> int:
        """Получает количество объявлений для указанного аккаунта.

        Args:
            acc_id (UUID): Уникальный идентификатор аккаунта.

        Returns:
            int: Количество объявлений, принадлежащих аккаунту.

        Raises:
            ExpError: Если API возвращает ошибку. Содержит:
                    - code (int): код ошибки
                    - msg (str): сообщение об ошибке
            httpx.RequestError: При проблемах с сетевым соединением.
            ValueError: При некорректном формате ответа API.
        """
        url = self.base_url + Enp.ADS_GET_COUNT_ADS_BY_ACCOUNT + f"?acc_id={acc_id}"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            resp_js = resp.json()
            if not resp_js["ok"]:
                raise ExpError(code_msg=(resp_js["err"]["code"], resp_js["err"]["msg"]))
            res = resp_js["payload"]
            return res
