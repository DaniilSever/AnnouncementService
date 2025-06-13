from datetime import datetime
from pydantic import BaseModel, EmailStr, UUID4

class XEmailSignup(BaseModel):
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

class XAccountID(BaseModel):
    """Запись в бд Account"""
    id: UUID4

class XRefreshToken(BaseModel):
    """Запись в бд RefershToken"""
    id: UUID4
    account_id: UUID4
    token: str
    is_revoked: bool = False
    created_at: datetime = datetime.now()
    expires_at: datetime | None = None
