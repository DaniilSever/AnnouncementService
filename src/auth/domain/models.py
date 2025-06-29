from uuid import uuid4
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Integer,
    TIMESTAMP,
    CheckConstraint,
    Boolean,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy."""


class SignupAccount(Base):
    """Модель регистрации аккаунта по email.

    Attributes:
        id (UUID): Уникальный идентификатор аккаунта.
        email (str): Email пользователя.
        pwd_hash (str): Хеш пароля пользователя.
        salt (str): Соль для хеширования пароля.
        code (str): Код подтверждения регистрации.
        created_at (datetime): Время создания записи.
        updated_at (datetime | None): Время последнего обновления записи.
        blocked_till (datetime | None): Время блокировки аккаунта.
        attempts (int): Количество попыток входа (максимум 5).
    """

    __tablename__ = "SignupAccount"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String(255), nullable=False)
    pwd_hash = Column(String(255), nullable=False)
    salt = Column(String, nullable=False)
    code = Column(String(10), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = Column(TIMESTAMP, nullable=True)
    blocked_till = Column(TIMESTAMP, nullable=True)
    attempts = Column(Integer, nullable=False, default=1)

    __table_args__ = (CheckConstraint("attempts <= 5", name="check_attempts"),)


class RefreshToken(Base):
    """
    Модель refresh-токена для продления сессии.

    Attributes:
        id (UUID): Уникальный идентификатор токена.
        account_id (UUID): ID аккаунта, которому принадлежит токен.
        token (str): Строковое представление refresh-токена.
        is_revoked (bool): Флаг, указывающий, отозван ли токен.
        created_at (datetime): Время создания токена.
        expires_at (datetime): Время истечения срока действия токена.
    """

    __tablename__ = "RefreshToken"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    account_id = Column(UUID(as_uuid=True), nullable=False)
    token = Column(String, nullable=False)
    is_revoked = Column(Boolean, nullable=False, default=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now())
    expires_at = Column(TIMESTAMP, nullable=False)

    __table_args__ = (
        Index("ix_refreshtoken_account_id", "account_id"),
        Index("ix_refreshtoken_is_revoked", "is_revoked"),
        Index("ix_refreshtoken_expires_at", "expires_at"),
    )
