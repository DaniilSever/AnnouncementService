from account.external.svc import AccService
from ads.external.svc import AdsService
from compl.external.svc import ComplService
from notice.external.tg.client import TgClient

from .pg import (
    AsyncAccRepoSession,
    AsyncAdsRepoSession,
    AsyncAuthRepoSession,
    AsyncComplRepoSession,
)
from .configs import AccountConfig, AdsConfig, ComplConfig, TgConfig


async def get_account_repo_session():
    """Получает асинхронную сессию репозитория аккаунтов.

    Yields:
        AsyncSession: Асинхронная сессия для работы с аккаунтами.
    """
    async with AsyncAccRepoSession() as session:
        yield session


async def get_auth_repo_session():
    """Получает асинхронную сессию репозитория аутентификации.

    Yields:
        AsyncSession: Асинхронная сессия для работы с аутентификацией.
    """
    async with AsyncAuthRepoSession() as session:
        yield session


async def get_ads_repo_session():
    """Получает асинхронную сессию репозитория объявлений.

    Yields:
        AsyncSession: Асинхронная сессия для работы с объявлениями.
    """
    async with AsyncAdsRepoSession() as session:
        yield session


async def get_compl_repo_session():
    """Получает асинхронную сессию репозитория жалоб.

    Yields:
        AsyncSession: Асинхронная сессия для работы с жалобами.
    """
    async with AsyncComplRepoSession() as session:
        yield session


def get_account_serivce() -> AccService:
    """Создаёт и возвращает сервис для работы с аккаунтами.

    Returns:
        AccService: Сервис для взаимодействия с аккаунтами.
    """
    cfg = AccountConfig()
    return AccService(cfg.API_URL)


def get_ads_serivce() -> AdsService:
    """Создаёт и возвращает сервис для работы с объявлениями.

    Returns:
        AdsService: Сервис для взаимодействия с объявлениями.
    """
    cfg = AdsConfig()
    return AdsService(cfg.API_URL)


def get_compl_serivce() -> ComplService:
    """Создаёт и возвращает сервис для работы с жалобами.

    Returns:
        ComplService: Сервис для взаимодействия с жалобами.
    """
    cfg = ComplConfig()
    return ComplService(cfg.API_URL)


def get_tg_bot() -> TgClient:
    """Создаёт и возвращает клиент Telegram бота.

    Returns:
        TgClient: Клиент для взаимодействия с Telegram ботом.
    """
    cfg = TgConfig()
    return TgClient(cfg.TGBOT_TOKEN, cfg.TGBOT_CHATID)
