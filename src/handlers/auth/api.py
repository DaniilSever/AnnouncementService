from fastapi import APIRouter, Depends

from core.endpoints import Endpoints as Enp
from core.depends import get_auth_repo_session

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
async def healthcheck(
    _repo_session = Depends(get_auth_repo_session)
):
    pass