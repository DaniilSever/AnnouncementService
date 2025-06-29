from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, delete, update, text, func
from sqlalchemy.exc import NoResultFound

from kernel.exception import ExpError, ExpCode

from ..domain.irepo import IAdsRepo
from ..domain.dto import (
    QCreateAds,
    QFilter,
    QAdsCategory,
    QAdsPriceFilter,
    QChangeAds,
    QAddAdsComment,
    QUpdateAdsComment,
)
from ..domain.models import Ads, AdsComment

from .xdao import XAds, XAdsComment


class AdsRepo(IAdsRepo):
    """Реализация репозитория для работы с объявлениями.

    Args:
        _session (AsyncSession): Асинхронная сессия базы данных.
    """

    def __init__(self, _session: AsyncSession):
        self.session: AsyncSession = _session

    async def create_ads(
        self, ads: QCreateAds, ads_category: QAdsCategory, acc_id: UUID | None = None
    ) -> XAds:
        """Создаёт объявление в базе данных.

        Args:
            ads (QCreateAds): Данные объявления.
            ads_category (QAdsCategory): Категория объявления.
            acc_id (UUID | None): Идентификатор аккаунта (необязательно).

        Returns:
            XAds: Созданное объявление.
        """
        req = (
            insert(Ads)
            .values(
                account_id=acc_id,
                title=ads.title,
                description=ads.description,
                ads_category=ads_category.value,
                price=ads.price,
            )
            .returning(Ads)
        )
        res = await self.session.execute(req)
        await self.session.commit()
        row = res.scalar_one()
        return XAds(
            id=row.id,
            account_id=row.account_id,
            title=row.title,
            description=row.description,
            ads_category=row.ads_category,
            price=row.price,
            count_views=row.count_views,
            count_comments=row.count_comments,
            is_deleted=row.is_deleted,
            created_at=row.created_at,
            updated_at=row.updated_at,
            deleted_at=row.deleted_at,
            reason_deletion=row.reason_deletion,
        )

    async def get_ads_all(self, qfilter: QFilter) -> tuple[int, list[XAds]]:
        """Получает все объявления с учётом фильтров и пагинации.

        Args:
            qfilter (QFilter): Параметры фильтрации и пагинации.

        Returns:
            tuple[int, list[XAds]]: Общее количество объявлений и список объявлений.
        """
        count_req = select(func.count()).select_from(Ads)
        count_res = await self.session.execute(count_req)
        await self.session.commit()
        total = count_res.scalar_one()

        req = select(Ads).limit(qfilter.limit).offset(qfilter.offset)
        if qfilter.ads_category:
            req = req.where(Ads.ads_category == qfilter.ads_category.value)

        if qfilter.price:
            if qfilter.price == QAdsPriceFilter.BY_DECREASE:
                req = req.order_by(Ads.price.desc())
            elif qfilter.price == QAdsPriceFilter.BY_INCREASE:
                req = req.order_by(Ads.price.asc())
            else:
                raise ExpError(ExpCode.ADS_FILTER_ERR)

        if qfilter.price_from:
            req = req.where(Ads.price > qfilter.price_from)

        if qfilter.price_to:
            req = req.where(Ads.price < qfilter.price_to)

        xres = await self.session.execute(req)
        await self.session.commit()
        res = []
        for row in xres.scalars().all():
            res.append(
                XAds(
                    id=row.id,
                    account_id=row.account_id,
                    title=row.title,
                    description=row.description,
                    ads_category=row.ads_category,
                    price=row.price,
                    count_views=row.count_views,
                    count_comments=row.count_comments,
                    is_deleted=row.is_deleted,
                    created_at=row.created_at,
                    updated_at=row.updated_at,
                    deleted_at=row.deleted_at,
                    reason_deletion=row.reason_deletion,
                )
            )
        return total, res

    async def get_ads_by_id(self, ads_id: UUID) -> XAds:
        """Получает объявление по ID и увеличивает счётчик просмотров.

        Args:
            ads_id (UUID): Идентификатор объявления.

        Returns:
            XAds: Объявление с указанным ID.
        """
        req = (
            update(Ads).values(count_views=Ads.count_views + 1).where(Ads.id == ads_id)
        )
        try:
            res = await self.session.execute(req)
        except NoResultFound as e:
            raise KeyError("Объявление не найдено") from e
        await self.session.commit()

        req = select(Ads).where(Ads.id == ads_id)
        res = await self.session.execute(req)
        await self.session.commit()
        row = res.scalar_one_or_none()
        if row is None:
            raise KeyError("Объявление в бд не найдено")
        return XAds(
            id=row.id,
            account_id=row.account_id,
            title=row.title,
            description=row.description,
            ads_category=row.ads_category,
            price=row.price,
            count_views=row.count_views,
            count_comments=row.count_comments,
            is_deleted=row.is_deleted,
            created_at=row.created_at,
            updated_at=row.updated_at,
            deleted_at=row.deleted_at,
            reason_deletion=row.reason_deletion,
        )

    async def get_ads_by_account_id(self, acc_id: UUID) -> tuple[int, list[XAds]]:
        """Получает все объявления по идентификатору аккаунта.

        Args:
            acc_id (UUID): Идентификатор аккаунта.

        Returns:
            tuple[int, list[XAds]]: Общее количество объявлений и список объявлений аккаунта.
        """
        count_req = select(func.count()).select_from(Ads)
        count_res = await self.session.execute(count_req)
        await self.session.commit()
        total = count_res.scalar_one()

        req = select(Ads).where(Ads.account_id == acc_id)
        xres = await self.session.execute(req)
        await self.session.commit()
        res = []
        for row in xres.scalars().all():
            res.append(
                XAds(
                    id=row.id,
                    account_id=row.account_id,
                    title=row.title,
                    description=row.description,
                    ads_category=row.ads_category,
                    price=row.price,
                    count_views=row.count_views,
                    count_comments=row.count_comments,
                    is_deleted=row.is_deleted,
                    created_at=row.created_at,
                    updated_at=row.updated_at,
                    deleted_at=row.deleted_at,
                    reason_deletion=row.reason_deletion,
                )
            )
        return total, res

    async def update_ads(self, new_ads: QChangeAds, acc_id: UUID) -> XAds:
        """Обновляет объявление по данным и идентификатору аккаунта.

        Args:
            new_ads (QChangeAds): Новые данные объявления.
            acc_id (UUID): Идентификатор аккаунта.

        Returns:
            XAds: Обновлённое объявление.
        """
        req = (
            update(Ads)
            .values(
                title=new_ads.title,
                description=new_ads.description,
                price=new_ads.price,
                updated_at=text("NOW()"),
            )
            .where(Ads.account_id == acc_id, Ads.id == new_ads.ads_id)
            .returning(Ads)
        )
        try:
            res = await self.session.execute(req)
        except NoResultFound as e:
            raise KeyError("Объявление не найдено") from e
        await self.session.commit()
        row = res.scalar_one()
        return XAds(
            id=row.id,
            account_id=row.account_id,
            title=row.title,
            description=row.description,
            ads_category=row.ads_category,
            price=row.price,
            count_views=row.count_views,
            count_comments=row.count_comments,
            is_deleted=row.is_deleted,
            created_at=row.created_at,
            updated_at=row.updated_at,
            deleted_at=row.deleted_at,
            reason_deletion=row.reason_deletion,
        )

    async def update_category_ads(
        self, ads_id: UUID, new_category: QAdsCategory, acc_id: UUID
    ) -> XAds:
        """Обновляет категорию объявления по ID объявления и аккаунта.

        Args:
            ads_id (UUID): Идентификатор объявления.
            new_category (QAdsCategory): Новая категория объявления.
            acc_id (UUID): Идентификатор аккаунта.

        Returns:
            XAds: Обновлённое объявление с новой категорией.
        """
        req = (
            update(Ads)
            .values(ads_category=new_category.value, updated_at=text("NOW()"))
            .where(Ads.account_id == acc_id, Ads.id == ads_id)
            .returning(Ads)
        )
        try:
            res = await self.session.execute(req)
        except NoResultFound as e:
            raise KeyError("Объявление не найдено") from e
        await self.session.commit()
        row = res.scalar_one()
        return XAds(
            id=row.id,
            account_id=row.account_id,
            title=row.title,
            description=row.description,
            ads_category=row.ads_category,
            price=row.price,
            count_views=row.count_views,
            count_comments=row.count_comments,
            is_deleted=row.is_deleted,
            created_at=row.created_at,
            updated_at=row.updated_at,
            deleted_at=row.deleted_at,
            reason_deletion=row.reason_deletion,
        )

    async def delete_ads(self, ads_id: UUID, acc_id: UUID) -> None:
        """Удаляет объявление по ID объявления и аккаунта.

        Args:
            ads_id (UUID): Идентификатор объявления.
            acc_id (UUID): Идентификатор аккаунта.

        Returns:
            None
        """
        req = delete(Ads).where(Ads.account_id == acc_id, Ads.id == ads_id)
        await self.session.execute(req)
        await self.session.commit()

    async def adm_delete_ads(self, ads_id: UUID) -> None:
        """Удаляет объявление администратором по ID объявления.

        Args:
            ads_id (UUID): Идентификатор объявления.

        Returns:
            None
        """
        req = delete(Ads).where(Ads.id == ads_id)
        await self.session.execute(req)
        await self.session.commit()

    async def get_count_ads_by_acc_id(self, acc_id: UUID) -> int:
        """Получает количество объявлений по ID аккаунта.

        Args:
            acc_id (UUID): Идентификатор аккаунта.

        Returns:
            int: Количество объявлений аккаунта.
        """

        req = select(func.count()).select_from(Ads).where(Ads.account_id == acc_id)
        count_ads = await self.session.execute(req)
        await self.session.commit()
        return count_ads.scalar_one()

    # -------------------- AdsCommentary -------------------

    async def create_ads_commentary(
        self, new_comment: QAddAdsComment, acc_id: UUID
    ) -> XAdsComment:
        """Создаёт комментарий к объявлению и увеличивает счётчик комментариев.

        Args:
            new_comment (QAddAdsComment): Данные нового комментария.
            acc_id (UUID): Идентификатор аккаунта, создающего комментарий.

        Returns:
            XAdsComment: Созданный комментарий к объявлению.
        """
        req = (
            update(Ads)
            .values(count_comments=Ads.count_comments + 1)
            .where(Ads.id == new_comment.ads_id)
        )
        try:
            res = await self.session.execute(req)
        except NoResultFound as e:
            raise KeyError("Объявление не найдено") from e
        await self.session.commit()

        req = (
            insert(AdsComment)
            .values(
                ads_id=new_comment.ads_id,
                account_id=acc_id,
                ads_comment=new_comment.ads_comment,
            )
            .returning(AdsComment)
        )
        res = await self.session.execute(req)
        await self.session.commit()
        row = res.scalar_one()
        return XAdsComment(
            id=row.id,
            ads_id=row.ads_id,
            account_id=row.account_id,
            ads_comment=row.ads_comment,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    async def get_ads_commentary(self, ads_id: UUID, comment_id: UUID) -> XAdsComment:
        """Получает комментарий по ID объявления и комментария.

        Args:
            ads_id (UUID): Идентификатор объявления.
            comment_id (UUID): Идентификатор комментария.

        Returns:
            XAdsComment: Найденный комментарий.
        """
        req = select(AdsComment).where(
            AdsComment.ads_id == ads_id, AdsComment.id == comment_id
        )
        res = await self.session.execute(req)
        await self.session.commit()
        row = res.scalar_one_or_none()
        if row is None:
            raise KeyError("Объявление в бд не найдено")
        return XAdsComment(
            id=row.id,
            ads_id=row.ads_id,
            account_id=row.account_id,
            ads_comment=row.ads_comment,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    async def get_ads_commentaries(self, ads_id: UUID) -> tuple[int, list[XAdsComment]]:
        """Получает все комментарии к объявлению и их общее количество.

        Args:
            ads_id (UUID): Идентификатор объявления.

        Returns:
            tuple[int, list[XAdsComment]]: Общее количество комментариев и список комментариев.
        """
        count_req = select(func.count()).select_from(AdsComment)
        count_res = await self.session.execute(count_req)
        await self.session.commit()
        total = count_res.scalar_one()

        req = select(AdsComment).where(AdsComment.ads_id == ads_id)
        xres = await self.session.execute(req)
        await self.session.commit()
        res = []
        for row in xres.scalars().all():
            res.append(
                XAdsComment(
                    id=row.id,
                    ads_id=row.ads_id,
                    account_id=row.account_id,
                    ads_comment=row.ads_comment,
                    created_at=row.created_at,
                    updated_at=row.updated_at,
                )
            )
        return total, res

    async def update_ads_commentary(
        self, update_comm: QUpdateAdsComment
    ) -> XAdsComment:
        """Обновляет комментарий к объявлению.

        Args:
            update_comm (QUpdateAdsComment): Данные для обновления комментария.

        Returns:
            XAdsComment: Обновлённый комментарий.
        """
        req = (
            update(AdsComment)
            .values(ads_comment=update_comm.ads_comment, updated_at=text("NOW()"))
            .where(
                AdsComment.account_id == update_comm.acccount_id,
                AdsComment.ads_id == update_comm.ads_id,
                AdsComment.id == update_comm.comm_id,
            )
            .returning(AdsComment)
        )
        try:
            res = await self.session.execute(req)
        except NoResultFound as e:
            raise KeyError("Объявление не найдено") from e
        await self.session.commit()
        row = res.scalar_one()
        return XAdsComment(
            id=row.id,
            ads_id=row.ads_id,
            account_id=row.account_id,
            ads_comment=row.ads_comment,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )

    async def delete_ads_commentary(
        self, ads_id: UUID, comm_id: UUID, acc_id: UUID
    ) -> None:
        """Удаляет комментарий к объявлению и обновляет счётчик комментариев.

        Args:
            ads_id (UUID): Идентификатор объявления.
            comm_id (UUID): Идентификатор комментария.
            acc_id (UUID): Идентификатор аккаунта, к которому принадлежит комментарий.

        Returns:
            None
        """
        req = (
            update(Ads)
            .values(count_comments=Ads.count_comments - 1)
            .where(Ads.id == ads_id)
        )
        try:
            await self.session.execute(req)
        except NoResultFound as e:
            raise KeyError("Объявление не найдено") from e
        await self.session.commit()

        req = delete(AdsComment).where(
            AdsComment.account_id == acc_id,
            AdsComment.ads_id == ads_id,
            AdsComment.id == comm_id,
        )
        await self.session.execute(req)
        await self.session.commit()

    async def get_ads_id_by_comm_id(self, comm_id: UUID) -> UUID:
        """Получает ID объявления по ID комментария.

        Args:
            comm_id (UUID): Идентификатор комментария.

        Returns:
            UUID: Идентификатор связанного объявления.

        Raises:
            KeyError: Если комментарий не найден.
        """
        req = select(AdsComment).where(AdsComment.id == comm_id)
        res = await self.session.execute(req)
        await self.session.commit()

        row = res.scalar_one_or_none()
        if row is None:
            raise KeyError("Объявление в бд не найдено")
        return row.ads_id

    async def adm_delete_ads_commentary(self, comm_id: UUID, ads_id: UUID) -> None:
        """Удаляет администратором комментарий к объявлению и обновляет счётчик комментариев.

        Args:
            comm_id (UUID): Идентификатор комментария.

        Returns:
            None
        """
        req = (
            update(Ads)
            .values(count_comments=Ads.count_comments - 1)
            .where(Ads.id == ads_id)
        )
        try:
            await self.session.execute(req)
        except NoResultFound as e:
            raise KeyError("Объявление не найдено") from e
        await self.session.commit()

        req = delete(AdsComment).where(
            AdsComment.ads_id == ads_id,
            AdsComment.id == comm_id,
        )
        await self.session.execute(req)
        await self.session.commit()
