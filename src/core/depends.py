from .pg import AsyncAccRepoSession, AsyncAdsRepoSession, AsyncAuthRepoSession
from sqlalchemy.ext.asyncio import AsyncSession


async def get_account_repo_session() -> AsyncSession:
    async with AsyncAccRepoSession() as session:
        yield session


async def get_auth_repo_session() -> AsyncSession:
    async with AsyncAuthRepoSession() as session:
        yield session

async def get_ads_repo_session() -> AsyncSession:
    async with AsyncAdsRepoSession() as session:
        yield session
