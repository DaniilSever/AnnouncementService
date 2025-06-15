from typing import Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T", bound=BaseModel)


class SuccessResp(BaseModel, Generic[T]):
    """Универсальная модель успешного ответа с необязательным полезным нагрузочным объектом.

    Args:
        T (Generic): Тип полезного объекта в ответе.

    Attributes:
        ok (bool): Флаг успешного выполнения, всегда True.
        payload (T | None): Объект ответа, может быть None.
    """
    ok: bool = True
    payload: T | None  = Field(None, description="Объект ответа")

class ErrDetail(BaseModel):
    """Модель детализации ошибки.

    Attributes:
        code (str): Код ошибки.
        msg (str): Сообщение об ошибке.
        details (str | None): Дополнительные детали ошибки.
    """
    code: str = ""
    msg: str = ""
    details: str | None = None

class ErrResp(BaseModel):
    """Модель ошибки в ответе API.

    Attributes:
        ok (bool): Флаг успешного выполнения, всегда False.
        err (ErrDetail): Объект с деталями ошибки.
    """
    ok: bool = False
    err: ErrDetail = Field(description="Объект ошибки")

responses_model = {
    400: {"model": ErrResp, "description": "Bad Request"},
    403: {"model": ErrResp, "description": "Forbidden"},
    404: {"model": ErrResp, "description": "Not Found"},
    500: {"model": ErrResp, "description": "Internal Server Error"},
    503: {"model": ErrResp, "description": "Service Unavailable"},
}

def responses(*args) -> dict:  # pragma: no cover
    """Возвращает словарь моделей ответов по переданным HTTP-кодам.

    Args:
        *args (int): HTTP-коды статусов.

    Returns:
        dict: Словарь с моделями ответов и описаниями для указанных кодов.
    """
    if len(args) == 0:
        return responses_model
    return {k: v for k, v in responses_model.items() if k in args}
