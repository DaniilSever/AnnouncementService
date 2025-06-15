from enum import Enum
from datetime import datetime
from pydantic import BaseModel, UUID4


class QAdsCategory(Enum):
    SELLING = "selling"
    BUYING = "buying"
    PROVIDING_SERVICES = "providing services"


class QAdsPriceFilter(Enum):
    BY_INCREASE = "ASC"
    BY_DECREASE = "DESC"


class QFilter(BaseModel):
    limit: int = 10
    offset: int = 0
    price: QAdsPriceFilter | None = None
    price_from: int | None = None
    price_to: int | None = None
    ads_category: QAdsCategory | None = None


class QCreateAds(BaseModel):
    title: str
    description: str
    price: int


class QChangeAds(BaseModel):
    ads_id: UUID4
    title: str
    description: str
    price: int


class QAdmDeleteAds(BaseModel):
    ads_id: UUID4
    reason_deletion: str


class ZBanned(BaseModel):
    account_id: UUID4
    is_banned: bool
    blocked_at: datetime
    reason_blocked: str
    blocked_to: datetime


class ZAds(BaseModel):
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


class ZManyAds(BaseModel):
    total: int
    count: int
    offeset: int = 0
    items: list[ZAds] = []


# ---------- AdsComment ---------


class QAddAdsComment(BaseModel):
    ads_id: UUID4
    ads_comment: str


class QUpdateAdsComment(BaseModel):
    comm_id: UUID4
    ads_id: UUID4
    acccount_id: UUID4
    ads_comment: str


class QDelAdsComment(BaseModel):
    comm_id: UUID4
    ads_id: UUID4
    account_id: UUID4


class ZAdsComment(BaseModel):
    id: UUID4
    ads_id: UUID4
    account_id: UUID4
    ads_comment: str
    created_at: datetime = datetime.now()
    updated_at: datetime | None = None


class ZManyAdsComment(BaseModel):
    total: int
    count: int
    offeset: int = 0
    items: list[ZAdsComment] = []
