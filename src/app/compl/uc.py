from uuid import UUID
from core.configs import ComplConfig
from core.exception import ExpCode, ExpError

from domain.compl.irepo import IComplRepo
from domain.compl.dto import (
    Service,
    QCreateCompl,
    QFilter,
    ZCompl,
    ZManyCompl,
)

from infra.compl.repo import ComplRepo
from infra.compl.xdao import XCompl


class ComplUseCase:

    def __init__(self, _repo: ComplRepo):
        self.cfg = ComplConfig()
        self.repo: IComplRepo = _repo

    async def create_compl(self, req: QCreateCompl) -> ZCompl:
        res: XCompl = await self.repo.create_compl(req)
        return ZCompl.model_validate(res.model_dump(mode="json"))

    async def get_my_complaint(self, compl_id: UUID, acc_id: UUID) -> ZCompl:
        try:
            res: XCompl = await self.repo.get_my_complaint(compl_id, acc_id)
        except KeyError as e:
            raise ExpError(ExpCode.COMPL_NOT_FOUND, str(e)) from e
        return ZCompl.model_validate(res.model_dump(mode="json"))

    async def get_my_complaints(
        self, acc_id: UUID, complaints_of: Service | None = None
    ) -> ZManyCompl:
        total_acc, total_ads, xres = await self.repo.get_my_complaints(
            acc_id, complaints_of
        )
        res = []
        for xcompl in xres:
            res.append(ZCompl(**xcompl.model_dump(mode="json")))
        return ZManyCompl(
            total_ads=total_ads,
            total_acc=total_acc,
            count=len(res),
            items=res,
        )

    async def adm_get_complaints(self, qfilter: QFilter) -> ZManyCompl:
        total_ads, total_acc, xres = await self.repo.adm_get_complaints(qfilter)
        res = []
        for xcompl in xres:
            res.append(ZCompl(**xcompl.model_dump(mode="json")))
        return ZManyCompl(
            total_ads=total_ads,
            total_acc=total_acc,
            count=len(res),
            items=res,
        )

    async def adm_get_complaint(self, compl_id: UUID) -> ZCompl:
        try:
            res: XCompl = await self.repo.adm_get_complaint(compl_id)
        except KeyError as e:
            raise ExpError(ExpCode.COMPL_NOT_FOUND, str(e)) from e
        return ZCompl.model_validate(res.model_dump(mode="json"))
