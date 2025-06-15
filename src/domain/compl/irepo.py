from uuid import UUID

from domain.compl.dto import QCreateCompl, QFilter

from domain.compl.models import Service

from infra.compl.xdao import XCompl


class IComplRepo:

    async def create_compl(self, req: QCreateCompl) -> XCompl:
        raise NotImplementedError

    async def get_my_complaint(self, compl_id: UUID, acc_id: UUID) -> XCompl:
        raise NotImplementedError

    async def get_my_complaints(
        self, acc_id: UUID, complaints_of: Service | None = None
    ) -> list[XCompl]:
        raise NotImplementedError

    async def adm_get_complaint(self, compl_id: UUID) -> XCompl:
        raise NotImplementedError

    async def adm_get_complaints(self, qfilter: QFilter) -> list[XCompl]:
        raise NotImplementedError
