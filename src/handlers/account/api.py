from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, Depends, Path, Body

from core.depends import get_account_repo_session, AsyncSession
from core.endpoints import Endpoints as Enp
from core.response import responses, SuccessResp

from app.account.uc import AccUseCase

from domain.account.dto import QEmail, QEmailSignupData
from domain.account.dto import ZAccount, ZAccountID, ZIsBusy

from infra.account.repo import AccRepo

router = APIRouter(tags=["account"])
tags = {"name": "account", "description": "Внутренние эндпоинты работы с аккаунтом"}

# @router.get(
#     Enp.ACCOUNT_HEALTHCHECK,
#     summary="Проверка работоспособности account сервиса",
#     status_code=200,
# )
# async def healthcheck():
#     pass

# @router.get(
#     Enp.ACCOUNT_CURRENT,
#     summary="Получить информацию о текущем пользователе",
#     status_code=200,
# )
# async def get_account_current():
#     pass


@router.get(
    Enp.ACCOUNT_GET_BY_ID,
    summary="Получить аккаунт по ID",
    status_code=200,
    responses=responses(400, 404),
)
async def get_account_by_id(
    acc_id: Annotated[UUID, Path()],
    __repo_session: Annotated[AsyncSession, Depends(get_account_repo_session)],
) -> SuccessResp[ZAccount]:
    """Обрабатывает HTTP-запрос на получение аккаунта по его ID."""
    uc = AccUseCase(AccRepo(__repo_session))
    res = await uc.get_account_by_id(acc_id)
    return SuccessResp[ZAccount](payload=res)


@router.get(
    Enp.ACCOUNT_GET_BY_EMAIL,
    summary="Получить аккаунт по Email",
    status_code=200,
    responses=responses(400, 404),
)
async def get_account_by_email(
    req: Annotated[QEmail, Path()],
    __repo_session: Annotated[AsyncSession, Depends(get_account_repo_session)],
) -> SuccessResp[ZAccount]:
    """Обрабатывает HTTP-запрос на получение аккаунта по email."""
    uc = AccUseCase(AccRepo(__repo_session))
    res = await uc.get_account_by_email(req)
    return SuccessResp[ZAccount](payload=res)


@router.post(
    Enp.ACCOUNT_COPY_FOR_SIGNUP,
    summary="Копирование аккаунта после регистрации",
    status_code=200,
    responses=responses(400, 404),
)
async def copy_account_from_signup(
    req: Annotated[QEmailSignupData, Body()],
    __repo_session: Annotated[AsyncSession, Depends(get_account_repo_session)],
) -> SuccessResp[ZAccountID]:
    """Обрабатывает HTTP-запрос на копирование аккаунта после регистрации."""
    uc = AccUseCase(AccRepo(__repo_session))
    res = await uc.copy_account_from_signup(req)
    return SuccessResp[ZAccountID](payload=res)


@router.post(
    Enp.ACCOUNT_IS_EMAIL_BUSY,
    summary="Проверка существования email",
    status_code=200,
    responses=responses(404),
)
async def is_email_busy(
    req: Annotated[QEmail, Path()],
    __repo_session: Annotated[AsyncSession, Depends(get_account_repo_session)],
) -> SuccessResp[ZIsBusy]:
    """Обрабатывает HTTP-запрос на проверку существования email."""
    uc = AccUseCase(AccRepo(__repo_session))
    res = await uc.is_email_busy(req)
    return SuccessResp[ZIsBusy](payload=res)


@router.get(
    Enp.ACCOUNT_GET_ALL,
    summary="Получить все аккаунты",
    status_code=200,
)
async def get_accounts(
    __repo_session: Annotated[AsyncSession, Depends(get_account_repo_session)]
) -> SuccessResp[list[ZAccount]]:
    """Обрабатывает HTTP-запрос на получение списка всех аккаунтов."""
    uc = AccUseCase(AccRepo(__repo_session))
    res = await uc.get_accounts()
    return SuccessResp[list[ZAccount]](payload=res)


# @router.get(
#     Enp.ACCOUNT_GET_WARNINGS,
#     summary="Получить информацию о предупреждениях за нарушения",
#     status_code=200,
# )
# async def get_account_warnings():
#     pass

# @router.get(
#     Enp.ACCOUNT_GET_WARNING_BY_ID,
#     summary="Получить информацию о предупреждении за нарушение",
#     status_code=200,
# )
# async def get_account_warning_by_id():
#     pass
