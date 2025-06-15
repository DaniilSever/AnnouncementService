from .pg import AsyncAccRepoSession, AsyncAdsRepoSession, AsyncAuthRepoSession
from sqlalchemy.ext.asyncio import AsyncSession
from .configs import AccountConfig
from services.account.svc import AccService


async def get_account_repo_session() -> AsyncSession:
    """Получает асинхронную сессию репозитория аккаунтов.

    Yields:
        AsyncSession: Асинхронная сессия для работы с аккаунтами.
    """
    async with AsyncAccRepoSession() as session:
        yield session


async def get_auth_repo_session() -> AsyncSession:
    """Получает асинхронную сессию репозитория аутентификации.

    Yields:
        AsyncSession: Асинхронная сессия для работы с аутентификацией.
    """
    async with AsyncAuthRepoSession() as session:
        yield session


async def get_ads_repo_session() -> AsyncSession:
    """Получает асинхронную сессию репозитория объявлений.

    Yields:
        AsyncSession: Асинхронная сессия для работы с объявлениями.
    """
    async with AsyncAdsRepoSession() as session:
        yield session


def get_account_serivce() -> AccService:
    """Создаёт и возвращает сервис для работы с аккаунтами.

    Returns:
        AccService: Сервис для взаимодействия с аккаунтами.
    """
    cfg = AccountConfig()
    return AccService(cfg.API_URL)
