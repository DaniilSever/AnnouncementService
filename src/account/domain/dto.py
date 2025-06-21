from enum import Enum
from datetime import datetime
from pydantic import BaseModel, EmailStr, UUID4
from .models import AccRole


class BannedTo(Enum):
    """Периоды блокировки аккаунта."""

    WEEK = "week"
    MONTH = "month"
    MONTH3 = "month3"
    YEAR = "year"
    FOREVER = "forever"


class ZBanned(BaseModel):
    """Информация о блокировке аккаунта."""

    account_id: UUID4
    is_banned: bool
    blocked_at: datetime
    reason_blocked: str
    blocked_to: datetime


class ZIsBusy(BaseModel):
    """Статус занятости, например, email."""

    is_busy: bool


class QEmail(BaseModel):
    """Модель для передачи email."""

    email: str


class QEmailSignupData(BaseModel):
    """Данные для временной регистрации пользователя."""

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
    """Модель подтверждённого аккаунта."""

    id: UUID4
    email: str
    pwd_hash: str
    salt: str
    role: AccRole = (AccRole.USER,)
    count_ads: int
    is_banned: bool = False
    created_at: datetime = datetime.now()
    updated_at: datetime | None = None
    blocked_at: datetime | None = None
    reason_blocked: str | None = None
    blocked_to: datetime | None = None


class ZAccountID(BaseModel):
    """Модель с ID аккаунта."""

    id: UUID4
