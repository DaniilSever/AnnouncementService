from fastapi import APIRouter

from core.endpoints import Endpoints as Enp

router = APIRouter(tags=["auth"])
tags = {
    "name": "auth",
    "description": "Внутренние эндпоинты авторизации"
}

@router.get(
    Enp.AUTH_HEALTHCHECK,
    summary="Проверка работоспособности Auth сервиса",
    status_code=200,
)
async def healthcheck():
    pass