from datetime import datetime
from pydantic import BaseModel, EmailStr, UUID4

from domain.account.models import AccRole


class XAccountID(BaseModel):
    """Запись ID в бд Account"""

    id: UUID4


class XAccount(BaseModel):
    """Запись в бд Account"""

    id: UUID4
    email: str
    pwd_hash: str
    salt: str
    role: AccRole = AccRole.USER
    count_ads: int
    is_banned: bool = False
    created_at: datetime = datetime.now()
    updated_at: datetime | None = None
    blocked_at: datetime | None = None
    blocked_till: datetime | None = None
