from uuid import UUID
from core.configs import AdsConfig
from core.exception import ErrExp, ExpCode

from domain.ads.irepo import IAdsRepo
from domain.ads.dto import QCreateAds, QAdsCategory, QFilter, QChangeAds, QAddAdsComment, QUpdateAdsComment, QDelAdsComment
from domain.ads.dto import ZAds, ZAdsComment

from infra.ads.repo import AdsRepo
from infra.ads.xdao import XAds, XAdsComment

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

    # ---------- AdsCommentary -------------

    async def create_ads_commentary(self, req: QAddAdsComment, acc_id: UUID) -> ZAdsComment:
        try:
            res: XAdsComment = await self.repo.create_ads_commentary(req, acc_id)
        except KeyError as e:
            raise ErrExp(ExpCode.ADS_NOT_FOUND, str(e)) from e
        return ZAdsComment.model_validate(res.model_dump(mode="json"))

    async def get_ads_commentary(self, ads_id: UUID, comment_id: UUID) -> ZAdsComment:
        try:
            res: XAdsComment = await self.repo.get_ads_commentary(ads_id, comment_id)
        except KeyError as e:
            raise ErrExp(ExpCode.ADS_COMMENTARY_NOT_FOUND, str(e)) from e
        return ZAdsComment.model_validate(res.model_dump(mode="json"))

    async def get_ads_commentaries(self, ads_id: UUID) -> list[ZAdsComment]:
        xres = await self.repo.get_ads_commentaries(ads_id)
        res = []
        for xads in xres:
            res.append(ZAdsComment(**xads.model_dump(mode="json")))
        return res

    async def update_ads_commentary(self, req: QUpdateAdsComment) -> ZAdsComment:
        try:
            res: XAdsComment = await self.repo.update_ads_commentary(req)
        except KeyError as e:
            raise ErrExp(ExpCode.ADS_COMMENTARY_NOT_FOUND, str(e)) from e
        return ZAdsComment.model_validate(res.model_dump(mode="json"))

    async def delete_ads_commentary(self, req: QDelAdsComment) -> bool:
        try:
            await self.repo.delete_ads_commentary(req.ads_id, req.comm_id, req.account_id)
        except KeyError as e:
            raise ErrExp(ExpCode.ADS_COMMENTARY_NOT_FOUND, str(e)) from e
        return True
