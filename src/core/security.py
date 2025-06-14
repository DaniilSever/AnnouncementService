import hashlib
import random
import secrets
import string
from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

import jwt
from jwt.exceptions import InvalidTokenError

from .endpoints import Endpoints as Enp
from .configs import AuthConfig

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=Enp.AUTH_SIGNIN_EMAIL_FORM)

def create_password_hash(pwd: str, salt: str | None = None) -> tuple[str, str]:
    """Генерирует хеш пароля с использованием соли.

    Args:
        pwd (str): Пароль для хеширования.
        salt (str, optional): Соль для хеширования. Если не указана, генерируется автоматически.

    Returns:
        tuple[str, str]: Хеш пароля и соль.
    """
    if not salt:
        salt = secrets.token_hex(16)
    hash_object = hashlib.sha256((pwd + salt).encode())
    hash_hex = hash_object.hexdigest()
    return hash_hex, salt

def create_confirm_code() -> str:
    """Генерирует 10-значный код подтверждения.

    Returns:
        str: Строка из 10 цифр.
    """
    size = 10
    alphabet = string.digits
    random_str = "".join(random.choice(alphabet) for _ in range(size))
    return random_str

def create_jwt_token(payload: dict, private_key: str, delta: int | None = None) -> str:
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
        "exp_at": exp,
        "exp_in": int(delta),
        **payload,
    }
    encoded = jwt.encode(new_payload, private_key.strip(), algorithm="RS512")
    return encoded


async def decode_jwt(token: str, key: str) -> dict:
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
) -> dict:  # pragma: no cover, не знаю как покрыть
    cfg = AuthConfig()
    try:
        res: dict = await decode_jwt(token, cfg.JWT_PUBLIC_KEY)
    except ValueError as e:
        raise e
    return res
