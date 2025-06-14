from uuid import UUID
from core.configs import AccountConfig
from core.exception import ErrExp, ExpCode
from domain.account.irepo import IAccRepo
from domain.account.dto import QEmailSignupData, QEmail
from domain.account.dto import ZAccount, ZAccountID, ZIsBusy
from infra.account.repo import AccRepo
from infra.account.xdao import XAccount


class AccUseCase:

    def __init__(self, _repo: AccRepo):
        self.cfg = AccountConfig()
        self.repo: IAccRepo = _repo

    async def get_account_by_id(self, acc_id: UUID) -> ZAccount:
        try:
            x_acc: XAccount = await self.repo.get_account_by_id(acc_id)
        except KeyError as e:
            raise ErrExp(ExpCode.ACC_ACCOUNT_NOT_FOUND, str(e)) from e
        return ZAccount.model_validate(x_acc.model_dump(mode="json"))

    async def get_account_by_email(self, req: QEmail) -> ZAccount:
        try:
            x_acc: XAccount = await self.repo.get_account_by_email(req.email)
        except KeyError as e:
            raise ErrExp(ExpCode.ACC_ACCOUNT_NOT_FOUND, str(e)) from e
        return ZAccount.model_validate(x_acc.model_dump(mode="json"))

    async def copy_account_from_signup(self, signup: QEmailSignupData) -> ZAccountID:
        xacc_id = await self.repo.copy_account_from_signup(signup)
        return ZAccountID(id=xacc_id.id)

    async def is_email_busy(self, req: QEmail) -> ZIsBusy:
        is_busy = await self.repo.is_email_busy(req.email)
        return ZIsBusy(is_busy=is_busy)

    async def get_accounts(self) -> list[ZAccount]:
        xres = await self.repo.get_accounts()
        res = []
        for xacc in xres:
            res.append(ZAccount(**xacc.model_dump(mode="json")))
        return res
