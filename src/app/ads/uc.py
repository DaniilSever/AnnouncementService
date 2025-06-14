from uuid import UUID
from core.configs import AdsConfig
from core.exception import ErrExp, ExpCode

from domain.ads.irepo import IAdsRepo
from domain.ads.dto import QCreateAds, QAdsCategory, QFilter, QChangeAds
from domain.ads.dto import ZAds

from infra.ads.repo import AdsRepo
from infra.ads.xdao import XAds

class AdsUseCase:

    def __init__(self, _repo: AdsRepo):
        self.cfg = AdsConfig()
        self.repo: IAdsRepo = _repo

    async def create_ads(self, req: QCreateAds, ads_category: QAdsCategory, acc_id: UUID | None = None):
        res: XAds = await self.repo.create_ads(req, ads_category, acc_id)
        return ZAds.model_validate(res.model_dump(mode="json"))

    async def get_ads_all(self, qfilter: QFilter) -> list[ZAds]:
        xres = await self.repo.get_ads_all(qfilter)
        res = []
        for xads in xres:
            res.append(ZAds(**xads.model_dump(mode="json")))
        return res

    async def get_ads_by_id(self, ads_id: UUID) -> ZAds:
        try:
            res: XAds = await self.repo.get_ads_by_id(ads_id)
        except KeyError as e:
            raise ErrExp(ExpCode.ADS_NOT_FOUND, str(e)) from e
        return ZAds.model_validate(res.model_dump(mode="json"))

    async def get_ads_by_account_id(self, acc_id: UUID) -> ZAds:
        xres = await self.repo.get_ads_by_account_id(acc_id)
        res = []
        for xads in xres:
            res.append(ZAds(**xads.model_dump(mode="json")))
        return res

    async def change_my_ads(self, req: QChangeAds, acc_id: UUID) -> ZAds:
        try:
            res: XAds = await self.repo.update_ads(req, acc_id)
        except KeyError as e:
            raise ErrExp(ExpCode.ADS_NOT_FOUND, str(e)) from e
        return ZAds.model_validate(res.model_dump(mode="json"))

    async def change_category_ads(self, ads_id: UUID, req: QAdsCategory, acc_id: UUID) -> ZAds:
        try:
            res: XAds = await self.repo.update_category_ads(ads_id, req, acc_id)
        except KeyError as e:
            raise ErrExp(ExpCode.ADS_NOT_FOUND, str(e)) from e
        return ZAds.model_validate(res.model_dump(mode="json"))

    async def delete_ads(self, ads_id: UUID, acc_id: UUID) -> bool:
        await self.repo.delete_ads(ads_id, acc_id)
        return True
