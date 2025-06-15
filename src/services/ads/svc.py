from uuid import UUID
import httpx
from core.endpoints import Endpoints as Enp
from core.exception import ExpError

class AdsService:
    def __init__(self, _base_url: str):
        self.base_url = _base_url

    async def get_count_ads_by_acc_id(self, acc_id: UUID) -> int:
        url = self.base_url + Enp.ADS_GET_COUNT_ADS_BY_ACCOUNT + f"?acc_id={acc_id}"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            resp_js = resp.json()
            if not resp_js["ok"]:
                raise ExpError(code_msg=(resp_js["err"]["code"], resp_js["err"]["msg"]))
            res = resp_js["payload"]
            return res