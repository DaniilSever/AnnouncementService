from enum import Enum
from datetime import datetime
from pydantic import BaseModel, EmailStr, UUID4
from .models import AccRole


class BannedTo(Enum):
    WEEK = "week"
    MONTH = "month"
    MONTH3 = "month3"
    YEAR = "year"
    FOREVER = "forever"

class ZIsBusy(BaseModel):
    is_busy: bool


class QEmail(BaseModel):
    email: str


class QEmailSignupData(BaseModel):
    """Запись в бд SignupAccount"""

    id: UUID4
    email: EmailStr | str
    pwd_hash: str
    salt: str
    code: int
    created_at: datetime = datetime.now()
    updated_at: datetime | None = None
    blocked_till: datetime | None = None
    attempts: int = 1


class ZAccount(BaseModel):
    """Запись в бд Account"""

    id: UUID4
    email: str
    pwd_hash: str
    salt: str
    role: AccRole = AccRole.USER,
    count_ads: int
    is_banned: bool = False
    created_at: datetime = datetime.now()
    updated_at: datetime | None = None
    blocked_at: datetime | None = None
    reason_blocked: str | None = None
    blocked_to: datetime | None = None


class ZAccountID(BaseModel):
    id: UUID4
