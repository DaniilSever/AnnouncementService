from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, delete, update, text
from sqlalchemy.exc import IntegrityError

from core.exception import ErrExp, ExpCode

from domain.ads.irepo import IAdsRepo
from domain.ads.dto import QCreateAds, QFilter, QAdsPriceFilter
from domain.ads.models import Ads

from .xdao import XAds


class AdsRepo(IAdsRepo):

    def __init__(self, _session: AsyncSession):
        self.session: AsyncSession = _session

    async def create_ads(self, ads: QCreateAds, acc_id: UUID | None = None):
        req = (
            insert(Ads)
            .values(
                account_id=acc_id,
                title=ads.title,
                description=ads.description,
                ads_category=ads.ads_category.value,
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
