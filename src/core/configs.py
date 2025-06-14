from pydantic_settings import BaseSettings


class AccountConfig(BaseSettings):
    """Конфиг Account сервиса"""
    APP_ENV: str
    API_URL: str
    ACCOUNT_DB_URL: str

class AuthConfig(BaseSettings):
    """Конфиг Auth сервиса"""
    APP_ENV: str
    API_URL: str
    API_KEY: str
    AUTH_DB_URL: str
    JWT_PUBLIC_KEY: str
    JWT_PRIVATE_KEY: str
    AUTH_JWT_TOKEN_EXPIRE: int = 60 * 24

class AdsConfig(BaseSettings):
    """Конфиг Ads сервиса"""
    APP_ENV: str
    API_URL: str
    ADS_DB_URL: str
