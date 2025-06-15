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
    """Управляет бизнес-логикой работы с жалобами.

    Args:
        _repo (ComplRepo): Репозиторий для взаимодействия с данными жалоб.
    """

    def __init__(self, _repo: ComplRepo):
        self.cfg = ComplConfig()
        self.repo: IComplRepo = _repo

    async def create_compl(self, req: QCreateCompl) -> ZCompl:
        """Создаёт новую жалобу.

        Args:
            req (QCreateCompl): Запрос с данными для создания жалобы.

        Returns:
            ZCompl: Валидационная модель созданной жалобы.
        """
        res: XCompl = await self.repo.create_compl(req)
        return ZCompl.model_validate(res.model_dump(mode="json"))

    async def get_my_complaint(self, compl_id: UUID, acc_id: UUID) -> ZCompl:
        """Возвращает конкретную жалобу пользователя.

        Args:
            compl_id (UUID): Идентификатор жалобы.
            acc_id (UUID): Идентификатор аккаунта пользователя.

        Returns:
            ZCompl: Валидационная модель найденной жалобы.
        """
        try:
            res: XCompl = await self.repo.get_my_complaint(compl_id, acc_id)
        except KeyError as e:
            raise ExpError(ExpCode.COMPL_NOT_FOUND, str(e)) from e
        return ZCompl.model_validate(res.model_dump(mode="json"))

    async def get_my_complaints(
        self, acc_id: UUID, complaints_of: Service | None = None
    ) -> ZManyCompl:
        """Возвращает список жалоб, отправленных пользователем.

        Args:
            acc_id (UUID): Идентификатор аккаунта пользователя.
            complaints_of (Service | None): Фильтр по типу сервиса (опционально).

        Returns:
            ZManyCompl: Список жалоб с метаинформацией.
        """
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
        """Возвращает список жалоб для административного просмотра по заданному фильтру.

        Args:
            qfilter (QFilter): Параметры фильтрации жалоб.

        Returns:
            ZManyCompl: Список жалоб с метаинформацией.
        """
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
        """Возвращает конкретную жалобу по идентификатору для администратора.

        Args:
            compl_id (UUID): Идентификатор жалобы.

        Returns:
            ZCompl: Валидационная модель найденной жалобы.
        """
        try:
            res: XCompl = await self.repo.adm_get_complaint(compl_id)
        except KeyError as e:
            raise ExpError(ExpCode.COMPL_NOT_FOUND, str(e)) from e
        return ZCompl.model_validate(res.model_dump(mode="json"))
