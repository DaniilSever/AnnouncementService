import hashlib
import random
import secrets
import string
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, Security
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.api_key import APIKeyHeader

import jwt
from jwt.exceptions import InvalidTokenError

from .exception import ExpCode, ExpError
from .endpoints import Endpoints as Enp
from .configs import AuthConfig

cfg = AuthConfig()
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=Enp.AUTH_SIGNIN_EMAIL_FORM, auto_error=False
)

ApiKeyHeader = Annotated[
    str | None,
    Security(
        APIKeyHeader(
            name="X-API-KEY",
            auto_error=False,
            description="",
            scheme_name="ApiKey",
        )
    ),
]


def create_password_hash(
    pwd: str, salt: str | None = None
) -> tuple[str, str]:  # pragma: no cover
    """Генерирует хеш пароля с использованием соли.

    Args:
        pwd (str): Пароль для хеширования.
        salt (str, optional): Соль для хеширования. Если не указана, генерируется автоматически.

    Returns:
        tuple[str, str]: Кортеж из хеша пароля и соли.
    """
    if not salt:
        salt = secrets.token_hex(16)
    hash_object = hashlib.sha256((pwd + salt).encode())
    hash_hex = hash_object.hexdigest()
    return hash_hex, salt


def create_confirm_code() -> str:
    """Генерирует 5-значный код подтверждения.

    Returns:
        str: Строка из 5 цифр.
    """
    size = 5
    alphabet = string.digits
    random_str = "".join(random.choice(alphabet) for _ in range(size))
    return random_str


def create_jwt_token(
    payload: dict, private_key: str, delta: int | None = None
) -> str:  # pragma: no cover
    """Генерирует JWT токен.

    Args:
        payload (dict): Полезная нагрузка токена.
        private_key (str): Приватный ключ для подписи токена.
        delta (int, optional): Время жизни токена в секундах. По умолчанию 24 часа.

    Returns:
        str: Сгенерированный JWT токен.

    Raises:
        TypeError: Если переданные аргументы имеют неверный тип.
    """
    if not delta:
        delta = 24 * 60 * 60
    seconds = timedelta(seconds=int(delta))
    now = datetime.now()

    exp = now + seconds

    new_payload = {
        "iat": int(now.timestamp()),
        "iss": "auth.announcenment",
        "exp": int(exp.timestamp()),
        "exp_at": exp.isoformat(),
        "exp_in": int(delta),
        **payload,
    }
    encoded = jwt.encode(new_payload, private_key.strip(), algorithm="RS512")
    return encoded


async def decode_jwt(token: str, key: str) -> dict:  # pragma: no cover
    """Декодирует JWT токен.

    Args:
        token (str): JWT токен для декодирования.
        key (str): Публичный ключ для проверки подписи токена.

    Returns:
        dict: Полезная нагрузка токена.

    Raises:
        ValueError: Если токен истек или некорректен.
    """
    try:
        payload = jwt.decode(token, key.strip(), algorithms=["RS512"])
    except jwt.ExpiredSignatureError as e:
        raise ValueError("JWT token has expired") from e
    except InvalidTokenError as e:
        raise ValueError("incorrect jwt") from e
    return payload


async def get_jwt_payload(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> dict:  # pragma: no cover
    """Обрабатывает JWT-токен и возвращает полезную нагрузку.

    Args:
        token (str): JWT-токен из заголовка Authorization.

    Returns:
        dict: Полезная нагрузка токена.

    Raises:
        ValueError: Если токен недействителен или истёк.
    """
    try:
        res: dict = await decode_jwt(token, cfg.JWT_PUBLIC_KEY)
    except ValueError as e:
        raise e
    return res


async def check_jwt(
    jwt_token: Annotated[str | None, Depends(oauth2_scheme)],
) -> dict | None:
    """Проверяет авторизацию пользователя через JWT-токен.

    Args:
        jwt_token (str | None): JWT-токен из заголовка Authorization.

    Returns:
        dict | None: Расшифрованные данные из JWT-токена, если авторизация прошла успешно, иначе None.

    Raises:
        ExpError: Если токен некорректен или истёк.
    """
    if not jwt_token:
        return None

    try:
        res: dict = await decode_jwt(jwt_token, cfg.JWT_PUBLIC_KEY)
    except ValueError as e:
        raise ExpError(ExpCode.SYS_INVALID_JWT_TOKEN, str(e)) from e
    return res


async def check_apikey(
    api_key: ApiKeyHeader,
) -> bool:  # pragma: no cover
    """Проверяет авторизацию пользователя через API-ключ.

    Args:
        api_key (ApiKeyHeader): API-ключ, полученный из заголовка.

    Returns:
        bool: True, если API-ключ валиден, иначе ошибка.

    Raises:
        ExpError: Если API-ключ некорректен.
    """
    if not api_key:
        return False

    if api_key != cfg.API_KEY:
        raise ExpError(ExpCode.SYS_INVALID_API_KEY)
    return True


ApiKey = Annotated[bool, Depends(check_apikey)]
AJwt = Annotated[dict | None, Depends(check_jwt)]
