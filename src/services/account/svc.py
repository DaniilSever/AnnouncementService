from uuid import UUID
import httpx
from core.endpoints import Endpoints as Enp
from core.exception import ExpError
from domain.account.dto import QEmailSignupData
from domain.account.dto import ZAccount

class AccService:

    def __init__(self, _base_url: str):
        self.base_url = _base_url

    async def is_email_busy(self, email: str) -> bool:
        url = self.base_url + Enp.ACCOUNT_IS_EMAIL_BUSY.format(email = email)
        async with httpx.AsyncClient() as client:
            resp = await client.post(url)
            resp_js = resp.json()
            if not resp_js["ok"]:
                raise ExpError(code_msg=(resp_js["err"]["code"], resp_js["err"]["msg"]))
            res = resp_js["payload"]
            return res.get("is_busy", False)

    async def copy_account_from_signup(self, signup: QEmailSignupData) -> UUID:
        url = self.base_url + Enp.ACCOUNT_COPY_FOR_SIGNUP
        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=signup.model_dump(mode="json"))
            resp_js = resp.json()
            if not resp_js["ok"]:
                raise ExpError(code_msg=(resp_js["err"]["code"], resp_js["err"]["msg"]))
            res = resp_js["payload"]
            return res.get("id")

    async def get_account_by_email(self, email:str) -> ZAccount:
        url = self.base_url + Enp.ACCOUNT_GET_BY_EMAIL.format(email=email)
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            resp_js = resp.json()
            if not resp_js["ok"]:
                raise ExpError(code_msg=(resp_js["err"]["code"], resp_js["err"]["msg"]))
            res = resp_js["payload"]
            return ZAccount.model_validate(res)