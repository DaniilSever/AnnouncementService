from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, delete, update, text
from sqlalchemy.exc import NoResultFound

from core.exception import ErrExp, ExpCode

from domain.ads.irepo import IAdsRepo
from domain.ads.dto import QCreateAds, QFilter, QAdsCategory, QAdsPriceFilter, QChangeAds
from domain.ads.models import Ads

from .xdao import XAds


class AdsRepo(IAdsRepo):

    def __init__(self, _session: AsyncSession):
        self.session: AsyncSession = _session

    async def create_ads(self, ads: QCreateAds, ads_category: QAdsCategory, acc_id: UUID | None = None):
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

    async def get_ads_all(self, qfilter: QFilter) -> list[XAds]:
        req = (
            select(Ads)
            .limit(qfilter.limit)
            .offset(qfilter.offset)
        )
        if qfilter.ads_category:
            req = req.where(Ads.ads_category == qfilter.ads_category.value)

        if qfilter.price:
            if qfilter.price == QAdsPriceFilter.BY_DECREASE:
                req = req.order_by(Ads.price.desc())
            elif qfilter.price == QAdsPriceFilter.BY_INCREASE:
                req = req.order_by(Ads.price.asc())
            else:
                raise ErrExp(ExpCode.ADS_FILTER_ERR)

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
        return res

    async def get_ads_by_id(self, ads_id: UUID) -> XAds:
        req = (
            update(Ads)
            .values(
                count_views = Ads.count_views + 1
            )
            .where(
                Ads.id == ads_id
            )
        )
        try:
            res = await self.session.execute(req)
        except NoResultFound as e:
            raise KeyError("Объявление не найдено") from e
        await self.session.commit()

        req = (
            select(Ads)
            .where(Ads.id == ads_id)
        )
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

    async def get_ads_by_account_id(self, acc_id: UUID) -> list[XAds]:
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
        return res

    async def update_ads(self, new_ads: QChangeAds, acc_id: UUID) -> XAds:
        req = (
            update(Ads)
            .values(
                title=new_ads.title,
                description=new_ads.description,
                price=new_ads.price,
            )
            .where(
                Ads.account_id == acc_id,
                Ads.id == new_ads.ads_id
            )
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

    async def update_category_ads(self, ads_id: UUID, new_category: QAdsCategory, acc_id: UUID) -> XAds:
        req = (
            update(Ads)
            .values(
                ads_category=new_category.value
            )
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
        req = (
            delete(Ads)
            .where(
                Ads.account_id == acc_id,
                Ads.id == ads_id
            )
        )
        await self.session.execute(req)
        await self.session.commit()

    async def adm_delete_ads(self, ads_id: UUID) -> None:
        req = delete(Ads).where(Ads.id == ads_id)
        await self.session.execute(req)
        await self.session.commit()