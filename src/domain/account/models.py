from uuid import uuid4
from datetime import datetime
import enum
from sqlalchemy import (
    Column,
    String,
    TIMESTAMP,
    Boolean,
    Integer,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy."""


class AccRole(enum.Enum):
    """Перечисление ролей пользователей."""

    USER = "user"
    ADMIN = "admin"


class Account(Base):
    """Модель аккаунта пользователя.

    Attributes:
        id (UUID): Уникальный идентификатор аккаунта.
        email (str): Email аккаунта.
        pwd_hash (str): SHA-256 хеш пароля.
        salt (str): Соль для хеша пароля.
        role (str): Роль пользователя (например, user, admin).
        count_ads (int): Количество созданных объявлений пользователем.
        is_banned (bool): Флаг, забанен ли аккаунт.
        created_at (datetime): Дата создания аккаунта.
        updated_at (datetime | None): Дата последнего обновления аккаунта.
        blocked_at (datetime | None): Дата блокировки аккаунта.
        reason_blocked (str | None): Причина блокировки аккаунта.
        blocked_to (datetime | None): Дата снятия блокировки.
    """

    __tablename__ = "Account"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        comment="ID аккаунта в системе",
    )
    email = Column(String(255), nullable=False, comment="Email аккаунта")
    pwd_hash = Column(String(255), nullable=False, comment="SHA-256-хеш пароля")
    salt = Column(String, nullable=False, comment="Соль для хеша")
    role = Column(String, nullable=False, comment="Роли пользователей")
    count_ads = Column(
        Integer, nullable=False, comment="Количество созданных объявлений"
    )
    is_banned = Column(
        Boolean, nullable=False, default=False, comment="Забанен ли аккаунт"
    )
    created_at = Column(
        TIMESTAMP, nullable=False, default=datetime.now, comment="Дата создания аккаута"
    )
    updated_at = Column(TIMESTAMP, nullable=True, comment="Дата обновления аккаунта")
    blocked_at = Column(TIMESTAMP, nullable=True, comment="Дата блокировки аккаунта")
    reason_blocked = Column(String, nullable=True, comment="Причина блокировки")
    blocked_to = Column(TIMESTAMP, nullable=True, comment="Дата снятие блокировки")
