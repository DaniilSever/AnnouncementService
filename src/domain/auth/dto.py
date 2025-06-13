from datetime import datetime
from pydantic import BaseModel, EmailStr, UUID4, ConfigDict

class QEmailSignin(BaseModel):
    """Запрос: вход по email"""
    email: EmailStr
    password: str

class QEmailSignup(BaseModel):
    """Запрос: регистрация по email"""
    email: EmailStr
    password: str

class QConfirmCode(BaseModel):
    """Запрос: подтверждение регистрации"""
    signup_id: UUID4
    code: int

class QRefreshToken(BaseModel):
    """Запрос: обновления access токена"""
    refresh_token: str

class QRevokeToken(BaseModel):
    """Запрос: отозвать токен"""
    account_id: UUID4


class ZToken(BaseModel):
    """Ответ: токен"""
    access_token: str
    refresh_token: str | None
    token_type: str = "bearer"

class ZEmailSignup(BaseModel):
    """Ответ: заявка на регистрацию создана"""
    id: UUID4
    created_at: datetime = datetime.now()
    expired_at: datetime | None = None
    confirm_attempts: int = 1

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "04387f0e-842a-42ba-87dc-c2a3d30b7547",
                "created_at": "2025-12-13 05:37:40.483836",
                "expired_at": "2025-12-14 05:37:40.483836",
                "confirm_attempts": 1,
            }
        }
    )

class ZAccountID(BaseModel):
    """Ответ: аккаунт создан"""
    id: UUID4

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "04387f0e-842a-42ba-87dc-c2a3d30b7547",
            }
        }
    )
