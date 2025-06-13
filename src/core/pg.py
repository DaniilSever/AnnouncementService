from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .configs import AdsConfig, AccountConfig, AuthConfig

AUTH_URL = AuthConfig().AUTH_DB_URL
ACC_URL = AccountConfig().ACCOUNT_DB_URL
ADS_URL = AdsConfig().ADS_DB_URL


AsyncAuthRepoSession = sessionmaker(
    bind=create_async_engine(AUTH_URL, echo=True),
    expire_on_commit=False,
    class_=AsyncSession,
)

AsyncAccRepoSession = sessionmaker(
    bind=create_async_engine(ACC_URL, echo=True),
    expire_on_commit=False,
    class_=AsyncSession,
)

AsyncAdsRepoSession = sessionmaker(
    bind=create_async_engine(ADS_URL, echo=True),
    expire_on_commit=False,
    class_=AsyncSession,
)
