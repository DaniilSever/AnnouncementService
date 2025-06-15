from datetime import datetime
from pydantic import BaseModel, UUID4

from domain.compl.models import Service

class ZBanned(BaseModel):
    account_id: UUID4
    is_banned: bool
    blocked_at: datetime
    reason_blocked: str
    blocked_to: datetime


class QFilter(BaseModel):
    complaints_of: Service | None = None
    is_today: bool = True
    is_notified: bool = False
    is_resolved: bool = False
    limit: int = 10
    offset: int = 0

class QCreateCompl(BaseModel):
    compl_on_id: UUID4
    service: Service
    author_id: UUID4
    complaints: str
    is_notified: bool = False
    is_resolved: bool = False


class ZCompl(BaseModel):
    id: UUID4
    compl_on_id: UUID4
    services: Service
    author_id: UUID4
    complaints: str
    is_notified: bool = False
    is_resolved: bool = False
    created_at: datetime = datetime.now()


class ZManyCompl(BaseModel):
    total_ads: int
    total_acc: int
    count: int
    offeset: int = 0
    items: list[ZCompl] = []
