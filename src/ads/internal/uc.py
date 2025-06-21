from uuid import UUID

from kernel.configs import AdsConfig
from kernel.exception import ExpError, ExpCode

from ..domain.irepo import IAdsRepo
from ..domain.dto import (
    QCreateAds,
    QAdsCategory,
    QFilter,
    QChangeAds,
    QAddAdsComment,
    QUpdateAdsComment,
    QDelAdsComment,
    ZAds,
    ZAdsComment,
    ZManyAds,
    ZManyAdsComment,
)
from compl.domain.dto import QCreateCompl, ZCompl

from ..infra.repo import AdsRepo
from ..infra.xdao import XAds, XAdsComment

from compl.external.svc import ComplService
from notice.external.tg.client import TgClient
from notice.external.tg.const_msg import get_ads_warning_msg


class AdsUseCase:
    """Управляет бизнес-логикой для работы с объявлениями и комментариями.

    Args:
        _repo (AdsRepo): Репозиторий для операций с объявлениями.
        _compl_svc (ComplService): Сервис для работы с жалобами.
        _tg_svc (TgClient): Клиент для отправки сообщений в Telegram.
    """

    def __init__(self, _repo: AdsRepo, _compl_svc: ComplService, _tg_svc: TgClient):
        self.cfg = AdsConfig()
        self.repo: IAdsRepo = _repo
        self.compl_svc: ComplService = _compl_svc
        self.tg_svc: TgClient = _tg_svc

    async def create_ads(
        self, req: QCreateAds, ads_category: QAdsCategory, acc_id: UUID | None = None
    ):
        """Создаёт новое объявление.

        Args:
            req (QCreateAds): Данные для создания объявления.
            ads_category (QAdsCategory): Категория объявления.
            acc_id (UUID | None): Идентификатор аккаунта, если есть.

        Returns:
            ZAds: Созданное объявление.
        """
        res: XAds = await self.repo.create_ads(req, ads_category, acc_id)
        return ZAds.model_validate(res.model_dump(mode="json"))

    async def get_ads_all(self, qfilter: QFilter) -> ZManyAds:
        """Получает список всех объявлений с учётом фильтра.

        Args:
            qfilter (QFilter): Фильтр для выборки объявлений.

        Returns:
            ZManyAds: Множество объявлений с метаданными.
        """
        total, xres = await self.repo.get_ads_all(qfilter)
        res = []
        for xads in xres:
            res.append(ZAds(**xads.model_dump(mode="json")))
        return ZManyAds(total=total, count=len(res), offeset=qfilter.offset, items=res)

    async def get_ads_by_id(self, ads_id: UUID) -> ZAds:
        """Получает объявление по его идентификатору.

        Args:
            ads_id (UUID): Идентификатор объявления.

        Returns:
            ZAds: Найденное объявление.
        """
        try:
            res: XAds = await self.repo.get_ads_by_id(ads_id)
        except KeyError as e:
            raise ExpError(ExpCode.ADS_NOT_FOUND, str(e)) from e
        return ZAds.model_validate(res.model_dump(mode="json"))

    async def get_ads_by_account_id(self, acc_id: UUID) -> ZAds:
        """Получает объявления по идентификатору аккаунта.

        Args:
            acc_id (UUID): Идентификатор аккаунта.

        Returns:
            ZManyAds: Множество объявлений данного аккаунта.
        """
        total, xres = await self.repo.get_ads_by_account_id(acc_id)
        res = []
        for xads in xres:
            res.append(ZAds(**xads.model_dump(mode="json")))
        return ZManyAds(total=total, count=len(res), items=res)

    async def change_my_ads(self, req: QChangeAds, acc_id: UUID) -> ZAds:
        """Обновляет собственное объявление.

        Args:
            req (QChangeAds): Данные для обновления объявления.
            acc_id (UUID): Идентификатор аккаунта владельца.

        Returns:
            ZAds: Обновлённое объявление.
        """
        try:
            res: XAds = await self.repo.update_ads(req, acc_id)
        except KeyError as e:
            raise ExpError(ExpCode.ADS_NOT_FOUND, str(e)) from e
        return ZAds.model_validate(res.model_dump(mode="json"))

    async def change_category_ads(
        self, ads_id: UUID, req: QAdsCategory, acc_id: UUID
    ) -> ZAds:
        """Изменяет категорию объявления.

        Args:
            ads_id (UUID): Идентификатор объявления.
            req (QAdsCategory): Новая категория объявления.
            acc_id (UUID): Идентификатор аккаунта владельца.

        Returns:
            ZAds: Обновлённое объявление с новой категорией.
        """
        try:
            res: XAds = await self.repo.update_category_ads(ads_id, req, acc_id)
        except KeyError as e:
            raise ExpError(ExpCode.ADS_NOT_FOUND, str(e)) from e
        return ZAds.model_validate(res.model_dump(mode="json"))

    async def delete_ads(self, ads_id: UUID, acc_id: UUID) -> bool:
        """Удаляет объявление владельцем.

        Args:
            ads_id (UUID): Идентификатор объявления.
            acc_id (UUID): Идентификатор аккаунта владельца.

        Returns:
            bool: Результат удаления (True при успешном удалении).
        """
        await self.repo.delete_ads(ads_id, acc_id)
        return True

    async def adm_delete_ads(self, ads_id: UUID, reason: str) -> bool:
        """Администратор удаляет объявление и отправляет предупреждение в Telegram.

        Args:
            ads_id (UUID): Идентификатор объявления.
            reason (str): Причина удаления.

        Returns:
            bool: Результат удаления (True при успешном удалении).
        """
        ads = await self.repo.get_ads_by_id(ads_id)

        await self.repo.adm_delete_ads(ads_id)

        msg = await get_ads_warning_msg(ads.title, reason)
        await self.tg_svc.send_message(msg)
        return True

    async def get_count_ads_by_acc_id(self, acc_id: UUID) -> int:
        """Получает количество объявлений по идентификатору аккаунта.

        Args:
            acc_id (UUID): Идентификатор аккаунта.

        Returns:
            int: Количество объявлений.
        """
        res = await self.repo.get_count_ads_by_acc_id(acc_id)
        return res

    # ---------- AdsCommentary -------------

    async def create_ads_commentary(
        self, req: QAddAdsComment, acc_id: UUID
    ) -> ZAdsComment:
        """Создаёт комментарий к объявлению.

        Args:
            req (QAddAdsComment): Данные комментария.
            acc_id (UUID): Идентификатор аккаунта автора комментария.

        Returns:
            ZAdsComment: Созданный комментарий.
        """
        try:
            res: XAdsComment = await self.repo.create_ads_commentary(req, acc_id)
        except KeyError as e:
            raise ExpError(ExpCode.ADS_NOT_FOUND, str(e)) from e
        return ZAdsComment.model_validate(res.model_dump(mode="json"))

    async def get_ads_commentary(self, ads_id: UUID, comment_id: UUID) -> ZAdsComment:
        """Получает комментарий по идентификаторам объявления и комментария.

        Args:
            ads_id (UUID): Идентификатор объявления.
            comment_id (UUID): Идентификатор комментария.

        Returns:
            ZAdsComment: Найденный комментарий.
        """
        try:
            res: XAdsComment = await self.repo.get_ads_commentary(ads_id, comment_id)
        except KeyError as e:
            raise ExpError(ExpCode.ADS_COMMENTARY_NOT_FOUND, str(e)) from e
        return ZAdsComment.model_validate(res.model_dump(mode="json"))

    async def get_ads_commentaries(self, ads_id: UUID) -> ZManyAdsComment:
        """Получает все комментарии к объявлению.

        Args:
            ads_id (UUID): Идентификатор объявления.

        Returns:
            ZManyAdsComment: Множество комментариев с метаданными.
        """
        total, xres = await self.repo.get_ads_commentaries(ads_id)
        res = []
        for xads in xres:
            res.append(ZAdsComment(**xads.model_dump(mode="json")))
        return ZManyAdsComment(total=total, count=len(res), items=res)

    async def update_ads_commentary(self, req: QUpdateAdsComment) -> ZAdsComment:
        """Обновляет комментарий к объявлению.

        Args:
            req (QUpdateAdsComment): Данные для обновления комментария.

        Returns:
            ZAdsComment: Обновлённый комментарий.
        """
        try:
            res: XAdsComment = await self.repo.update_ads_commentary(req)
        except KeyError as e:
            raise ExpError(ExpCode.ADS_COMMENTARY_NOT_FOUND, str(e)) from e
        return ZAdsComment.model_validate(res.model_dump(mode="json"))

    async def delete_ads_commentary(self, req: QDelAdsComment) -> bool:
        """Удаляет комментарий к объявлению.

        Args:
            req (QDelAdsComment): Данные для удаления комментария.

        Returns:
            bool: Результат удаления (True при успешном удалении).
        """
        try:
            await self.repo.delete_ads_commentary(
                req.ads_id, req.comm_id, req.account_id
            )
        except KeyError as e:
            raise ExpError(ExpCode.ADS_COMMENTARY_NOT_FOUND, str(e)) from e
        return True

    async def adm_delete_ads_commentary(self, comm_id: UUID) -> bool:
        """Администратор удаляет комментарий к объявлению.

        Args:
            comm_id (UUID): Идентификатор комментария.

        Returns:
            bool: Результат удаления (True при успешном удалении).
        """
        try:
            ads_id = await self.repo.get_ads_id_by_comm_id(comm_id)
        except KeyError as e:
            raise ExpError(ExpCode.ADS_COMMENTARY_NOT_FOUND, str(e)) from e

        try:
            await self.repo.adm_delete_ads_commentary(comm_id, ads_id)
        except KeyError as e:
            raise ExpError(ExpCode.ADS_COMMENTARY_NOT_FOUND, str(e)) from e
        return True

    async def send_complaint(self, req: QCreateCompl) -> ZCompl:
        """Отправляет жалобу.

        Args:
            req (QCreateCompl): Данные жалобы.

        Returns:
            ZCompl: Созданная жалоба.
        """
        try:
            res = await self.compl_svc.create_compl(req)
        except ExpError as e:
            raise e
        return res

    async def is_author_complaint_ads(self, ads_id: UUID, acc_id: str) -> bool:
        """Проверяет, является ли аккаунт автором объявления.

        Args:
            ads_id (UUID): Идентификатор объявления.
            acc_id (str): Идентификатор аккаунта.

        Returns:
            bool: True, если аккаунт является автором объявления, иначе False.
        """
        ads = await self.get_ads_by_id(ads_id)

        if str(ads.account_id) == acc_id:
            return True
        return False
