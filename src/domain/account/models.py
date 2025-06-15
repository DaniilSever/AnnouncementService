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
    """Базовый класс для всех моделей SQLAlchemy"""


class AccRole(enum.Enum):
    """Роли пользователей"""

    USER = "user"
    ADMIN = "admin"


class Account(Base):
    """Аккаунты (Подтвержденные)"""

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
    count_ads = Column(Integer, nullable=False, comment="Количество созданных объявлений")
    is_banned = Column(
        Boolean, nullable=False, default=False, comment="Забанен ли аккаунт"
    )
    created_at = Column(
        TIMESTAMP, nullable=False, default=datetime.now, comment="Дата создания аккаута"
    )
    updated_at = Column(TIMESTAMP, nullable=True, comment="Дата обновления аккаунта")
    blocked_at = Column(TIMESTAMP, nullable=True, comment="Дата блокировки аккаунта")
    blocked_till = Column(TIMESTAMP, nullable=True, comment="Дата снятие блокировки")
