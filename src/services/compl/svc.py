import httpx
from core.endpoints import Endpoints as Enp
from core.exception import ExpError

from domain.compl.dto import QCreateCompl, ZCompl


class ComplService:
    """Сервис для работы с жалобами через внешнее API."""

    def __init__(self, _base_url: str):
        """Инициализирует сервис жалоб с базовым URL API.

        Args:
            _base_url (str): Базовый URL API сервиса жалоб.
        """
        self.base_url = _base_url

    async def create_compl(self, compl: QCreateCompl) -> ZCompl:
        """Создает новую жалобу через API.

        Args:
            compl (QCreateCompl): Данные для создания жалобы.

        Returns:
            ZCompl: Созданная жалоба с присвоенным идентификатором и статусом.

        Raises:
            ExpError: Если API возвращает ошибку, содержит:
                    - код ошибки (code)
                    - сообщение об ошибке (msg)
            httpx.RequestError: При возникновении сетевых проблем.
            ValueError: При неверном формате ответа API.
        """
        url = self.base_url + Enp.COMPL_ADD_COMPLAINT
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=compl.model_dump(mode="json"))
            resp_js = resp.json()
            if not resp_js["ok"]:
                raise ExpError(code_msg=(resp_js["err"]["code"], resp_js["err"]["msg"]))
            res = resp_js["payload"]
            return res
