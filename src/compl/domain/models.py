from enum import Enum
from uuid import uuid4
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    TIMESTAMP,
    Boolean,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Service(Enum):
    """Перечисление доступных сервисов для жалоб."""

    ACCOUNT = "account"
    ADS = "ads"


class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy."""


class Complaints(Base):
    """Модель таблицы жалоб на пользователей и объявления.

    Attributes:
        id (UUID): Уникальный идентификатор жалобы.
        compl_on_id (UUID): ID объекта жалобы (объявление или аккаунт).
        services (str): Имя сервиса, из которого поступила жалоба.
        author_id (UUID): ID автора жалобы.
        complaints (str): Текст жалобы.
        is_notified (bool): Флаг, уведомлен ли автор жалобы.
        is_resolved (bool): Флаг, решена ли жалоба.
        created_at (datetime): Дата и время создания записи.
    """

    __tablename__ = "Complaints"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        comment="ID жалобы в системе",
    )
    compl_on_id = Column(
        UUID(as_uuid=True), nullable=False, comment="Жалоба на ID (Ads | Account)"
    )
    services = Column(
        String, nullable=False, comment="Сервис из которого жалоба (Ads | Account)"
    )
    author_id = Column(UUID(as_uuid=True), nullable=False, comment="ID автора жалобы")
    complaints = Column(String, nullable=False, comment="Жалоба")
    is_notified = Column(Boolean, nullable=False, comment="Уведомлен ли автор")
    is_resolved = Column(Boolean, nullable=False, comment="Решена ли жалоба")
    created_at = Column(
        TIMESTAMP, nullable=False, default=datetime.now, comment="Дата создания"
    )

    __table_args__ = (
        Index("ix_complaints_compl_on_id", "compl_on_id"),
        Index("ix_complaints_services", "services"),
        Index("ix_complaints_author_id", "author_id"),
    )
