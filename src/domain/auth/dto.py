from datetime import datetime
from pydantic import BaseModel, EmailStr, UUID4, ConfigDict


class QEmailSignin(BaseModel):
    """Модель запроса для входа по email."""

    email: EmailStr
    password: str


class QEmailSignup(BaseModel):
    """Модель запроса для регистрации по email."""

    email: EmailStr
    password: str


class QConfirmCode(BaseModel):
    """Модель запроса для подтверждения регистрации."""

    signup_id: UUID4
    code: str


class QRefreshToken(BaseModel):
    """Модель запроса для обновления access токена."""

    refresh_token: str


class QRevokeToken(BaseModel):
    """Модель запроса для отзыва токена."""

    account_id: UUID4


class ZToken(BaseModel):
    """Модель ответа с токенами."""

    access_token: str
    refresh_token: str | None
    token_type: str = "bearer"


class ZEmailSignup(BaseModel):
    """Модель ответа, подтверждающая создание заявки на регистрацию."""

    id: UUID4
    created_at: datetime = datetime.now()
    updated_at: datetime | None = None
    blocked_till: datetime | None = None
    attempts: int = 1

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "04387f0e-842a-42ba-87dc-c2a3d30b7547",
                "created_at": "2025-12-13 05:37:40.483836",
                "updated_at": "2025-12-14 05:37:40.483836",
                "blocked_till": "",
                "attempts": 1,
            }
        }
    )


class ZAccountID(BaseModel):
    """Модель ответа с идентификатором созданного аккаунта."""

    id: UUID4

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "04387f0e-842a-42ba-87dc-c2a3d30b7547",
            }
        }
    )


class ZRevokedTokens(BaseModel):
    """Модель ответа об отзыве токенов."""

    success: bool = True
    message: str
