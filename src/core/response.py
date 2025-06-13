from typing import Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T", bound=BaseModel)


class SuccessResp(BaseModel, Generic[T]):
    ok: bool = True
    payload: T | None  = Field(None, description="Объект ответа")

class ErrDetail(BaseModel):
    code: str = ""
    msg: str = ""
    details: str | None = None

class ErrResp(BaseModel):
    ok: bool = False
    err: ErrDetail = Field(description="Объект ошибки")

responses_model = {
    400: {"model": ErrResp, "description": "Bad Request"},
    403: {"model": ErrResp, "description": "Forbidden"},
    404: {"model": ErrResp, "description": "Not Found"},
    500: {"model": ErrResp, "description": "Internal Server Error"},
    503: {"model": ErrResp, "description": "Service Unavailable"},
}

def responses(*args) -> dict:
    if len(args) == 0:
        return responses_model
    return {k: v for k, v in responses_model.items() if k in args}
