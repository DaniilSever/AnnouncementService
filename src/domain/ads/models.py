from uuid import uuid4
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Integer,
    TIMESTAMP,
    Index,
    ForeignKey,
    BOOLEAN,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy."""


class Ads(Base):
    """Модель таблицы объявлений.

    Attributes:
        id (UUID): ID объявления в системе.
        account_id (UUID): ID аккаунта владельца объявления.
        title (str): Название объявления.
        description (str): Описание объявления.
        ads_category (str): Категория объявления.
        price (int): Цена услуги.
        count_views (int): Количество просмотров объявления.
        count_comments (int): Количество комментариев.
        is_deleted (bool): Флаг удаления объявления.
        created_at (datetime): Дата создания объявления.
        updated_at (datetime | None): Дата последнего изменения объявления.
        deleted_at (datetime | None): Дата удаления объявления.
        reason_deletion (str | None): Причина удаления объявления.
    """

    __tablename__ = "Ads"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        comment="ID объявления в системе",
    )
    account_id = Column(
        UUID(as_uuid=True), nullable=False, comment="ID аккаунта владельца объявления"
    )
    title = Column(String(255), nullable=False, comment="Название объявления")
    description = Column(String, nullable=False, comment="Описания объявления")
    ads_category = Column(String, nullable=False, comment="Категория объявления")
    price = Column(Integer, nullable=False, comment="Цена услуги")
    count_views = Column(
        Integer, nullable=False, default=0, comment="Количество просмотров объявления"
    )
    count_comments = Column(
        Integer, nullable=False, default=0, comment="Количество комментариев"
    )
    is_deleted = Column(
        BOOLEAN, nullable=False, default=False, comment="Удалено ли объявление"
    )
    created_at = Column(
        TIMESTAMP, nullable=False, default=datetime.now, comment="Дата создания"
    )
    updated_at = Column(TIMESTAMP, nullable=True, comment="Дата последнего изменения")
    deleted_at = Column(TIMESTAMP, nullable=True, comment="Дата удаления объявления")
    reason_deletion = Column(
        String, nullable=True, comment="Причина удаления объявления"
    )

    __table_args__ = (Index("ix_ads_account_id", "account_id"),)


class AdsComment(Base):
    """Модель таблицы комментариев к объявлению.

    Attributes:
        id (UUID): Уникальный идентификатор комментария.
        ads_id (UUID): Идентификатор объявления, к которому относится комментарий.
        account_id (UUID): Идентификатор автора комментария.
        ads_comment (str): Текст комментария.
        created_at (datetime): Дата и время создания комментария.
        updated_at (datetime | None): Дата и время последнего обновления комментария.
    """


    __tablename__ = "AdsComment"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        comment="ID комментария в системе",
    )
    ads_id = Column(
        UUID(as_uuid=True),
        ForeignKey("Ads.id", ondelete="CASCADE"),
        nullable=False,
        comment="ID Объявления",
    )
    account_id = Column(
        UUID(as_uuid=True), nullable=False, comment="ID Автора комментария"
    )
    ads_comment = Column(String, nullable=False, comment="Комментарий в объявлении")
    created_at = Column(
        TIMESTAMP, nullable=False, default=datetime.now, comment="Дата создания"
    )
    updated_at = Column(TIMESTAMP, nullable=True, comment="Дата последнего изменения")

    __table_args__ = (
        Index("ix_adscomment_ads_id", "ads_id"),
        Index("ix_adscomment_account_id", "account_id"),
    )
