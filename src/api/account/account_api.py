from fastapi import APIRouter

from core.endpoints import Endpoints as Enp

router = APIRouter(tags=["account"])
tags = {
    "name": "account",
    "description": "Внутренние эндпоинты работы с аккаунтом"
}

@router.get(
    Enp.ACCOUNT_HEALTHCHECK,
    summary="Проверка работоспособности account сервиса",
    status_code=200,
)
async def healthcheck():
    pass

@router.get(
    Enp.ACCOUNT_CURRENT,
    summary="Получить информацию о текущем пользователе",
    status_code=200,
)
async def get_account_current():
    pass

@router.get(
    Enp.ACCOUNT_GET_BY_ID,
    summary="Получить аккаунт по ID",
    status_code=200,
)
async def get_account_by_id():
    pass

@router.get(
    Enp.ACCOUNT_GET_WARNINGS,
    summary="Получить информацию о предупреждениях за нарушения",
    status_code=200,
)
async def get_account_warnings():
    pass

@router.get(
    Enp.ACCOUNT_GET_WARNING_BY_ID,
    summary="Получить информацию о предупреждении за нарушение",
    status_code=200,
)
async def get_account_warning_by_id():
    pass
