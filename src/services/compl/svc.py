import httpx
from core.endpoints import Endpoints as Enp
from core.exception import ExpError

from domain.compl.dto import QCreateCompl, ZCompl

class ComplService:
    def __init__(self, _base_url: str):
        self.base_url = _base_url

    async def create_compl(self, compl: QCreateCompl) -> ZCompl:
        url = self.base_url + Enp.COMPL_ADD_COMPLAINT
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=compl.model_dump(mode="json"))
            resp_js = resp.json()
            if not resp_js["ok"]:
                raise ExpError(code_msg=(resp_js["err"]["code"], resp_js["err"]["msg"]))
            res = resp_js["payload"]
            return res
