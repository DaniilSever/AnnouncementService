from datetime import datetime
from pydantic import BaseModel, UUID4


class XAds(BaseModel):
    id: UUID4
    account_id: UUID4
    title: str
    description: str
    ads_category: str
    price: int
    count_views: int
    count_comments: int
    is_deleted: bool = False
    created_at: datetime = datetime.now()
    updated_at: datetime | None = None
    deleted_at: datetime | None = None
    reason_deletion: str | None = None


class XAdsComment(BaseModel):
    id: UUID4
    ads_id: UUID4
    account_id: UUID4
    ads_comment: str
    created_at: datetime = datetime.now()
    updated_at: datetime | None = None
