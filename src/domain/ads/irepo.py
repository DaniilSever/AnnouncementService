from uuid import UUID

from domain.ads.dto import QAdsCategory
from infra.ads.xdao import XAds

class IAdsRepo:

    async def create_ads(self, req):
        raise NotImplementedError

    async def get_ads_by_id(self, ads_id: UUID):
        raise NotImplementedError

    async def get_ads_all(self):
        raise NotImplementedError

    async def update_ads(self, req):
        raise NotImplementedError
    
    async def update_category_ads(self, ads_id: UUID, new_category: QAdsCategory, acc_id: UUID) -> XAds:
        raise NotImplementedError

    async def delete_ads(self, req):
        raise NotImplementedError

    async def check_count_views(self, ads_id: UUID):
        raise NotImplementedError

    async def check_count_comments(self, ads_id: UUID):
        raise NotImplementedError

    async def create_ads_commentary(self, req):
        raise NotImplementedError

    async def get_ads_commentaries(self, ads_id: UUID):
        raise NotImplementedError

    async def get_ads_commentary(self, ads_id: UUID, commentary_id: UUID):
        raise NotImplementedError

    async def update_ads_commentary(self, ads_id: UUID, commentary_id: UUID):
        raise NotImplementedError
