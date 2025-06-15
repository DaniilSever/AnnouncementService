from enum import Enum
from datetime import datetime
from pydantic import BaseModel, UUID4


class QAdsCategory(Enum):
    """Категории объявлений."""

    SELLING = "selling"
    BUYING = "buying"
    PROVIDING_SERVICES = "providing services"


class QAdsPriceFilter(Enum):
    """Варианты сортировки по цене."""

    BY_INCREASE = "ASC"
    BY_DECREASE = "DESC"


class QFilter(BaseModel):
    """Параметры фильтрации объявлений."""

    limit: int = 10
    offset: int = 0
    price: QAdsPriceFilter | None = None
    price_from: int | None = None
    price_to: int | None = None
    ads_category: QAdsCategory | None = None


class QCreateAds(BaseModel):
    """Данные для создания объявления."""

    title: str
    description: str
    price: int


class QChangeAds(BaseModel):
    """Данные для обновления объявления."""

    ads_id: UUID4
    title: str
    description: str
    price: int


class QAdmDeleteAds(BaseModel):
    """Данные для админского удаления объявления."""

    ads_id: UUID4
    reason_deletion: str


class ZBanned(BaseModel):
    """Информация о бане аккаунта."""

    account_id: UUID4
    is_banned: bool
    blocked_at: datetime
    reason_blocked: str
    blocked_to: datetime


class ZAds(BaseModel):
    """Модель объявления."""

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
    """Коллекция объявлений с пагинацией."""

    total: int
    count: int
    offeset: int = 0
    items: list[ZAds] = []


# ---------- AdsComment ---------


class QAddAdsComment(BaseModel):
    """Данные для создания комментария к объявлению."""

    ads_id: UUID4
    ads_comment: str


class QUpdateAdsComment(BaseModel):
    """Данные для обновления комментария к объявлению."""

    comm_id: UUID4
    ads_id: UUID4
    acccount_id: UUID4
    ads_comment: str


class QDelAdsComment(BaseModel):
    """Данные для удаления комментария к объявлению."""

    comm_id: UUID4
    ads_id: UUID4
    account_id: UUID4


class ZAdsComment(BaseModel):
    """Модель комментария к объявлению."""

    id: UUID4
    ads_id: UUID4
    account_id: UUID4
    ads_comment: str
    created_at: datetime = datetime.now()
    updated_at: datetime | None = None


class ZManyAdsComment(BaseModel):
    """Коллекция комментариев с пагинацией."""

    total: int
    count: int
    offeset: int = 0
    items: list[ZAdsComment] = []
