from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, Depends, Path, Body, Query

from core.depends import get_account_repo_session, AsyncSession, get_ads_serivce, AdsService, get_compl_serivce, ComplService, get_tg_bot, TgClient
from core.endpoints import Endpoints as Enp
from core.response import responses, SuccessResp
from core.security import AJwt
from core.exception import ExpError, ExpCode

from app.account.uc import AccUseCase

from domain.account.dto import BannedTo, QEmail, QEmailSignupData
from domain.account.dto import ZAccount, ZAccountID, ZIsBusy, ZBanned
from domain.account.models import AccRole
from domain.compl.dto import QCreateCompl, ZCompl
from domain.compl.models import Service

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


@router.get(
    Enp.ACCOUNT_GET_BY_ID,
    summary="Получить аккаунт по ID",
    status_code=200,
    responses=responses(400, 404),
)
async def get_account_by_id(
    acc_id: Annotated[UUID, Path()],
    __repo_session: Annotated[AsyncSession, Depends(get_account_repo_session)],
    __ads_svc: Annotated[AdsService, Depends(get_ads_serivce)],
    __compl_svc: Annotated[ComplService, Depends(get_compl_serivce)],
    __tg_svc: Annotated[TgClient, Depends(get_tg_bot)]
) -> SuccessResp[ZAccount]:
    """Обрабатывает HTTP-запрос на получение аккаунта по его ID."""
    uc = AccUseCase(AccRepo(__repo_session), __ads_svc, __compl_svc, __tg_svc)
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
    __ads_svc: Annotated[AdsService, Depends(get_ads_serivce)],
    __compl_svc: Annotated[ComplService, Depends(get_compl_serivce)],
    __tg_svc: Annotated[TgClient, Depends(get_tg_bot)]
) -> SuccessResp[ZAccount]:
    """Обрабатывает HTTP-запрос на получение аккаунта по email."""
    uc = AccUseCase(AccRepo(__repo_session), __ads_svc, __compl_svc, __tg_svc)
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
    __ads_svc: Annotated[AdsService, Depends(get_ads_serivce)],
    __compl_svc: Annotated[ComplService, Depends(get_compl_serivce)],
    __tg_svc: Annotated[TgClient, Depends(get_tg_bot)]
) -> SuccessResp[ZAccountID]:
    """Обрабатывает HTTP-запрос на копирование аккаунта после регистрации."""
    uc = AccUseCase(AccRepo(__repo_session), __ads_svc, __compl_svc, __tg_svc)
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
    __ads_svc: Annotated[AdsService, Depends(get_ads_serivce)],
    __compl_svc: Annotated[ComplService, Depends(get_compl_serivce)],
    __tg_svc: Annotated[TgClient, Depends(get_tg_bot)]
) -> SuccessResp[ZIsBusy]:
    """Обрабатывает HTTP-запрос на проверку существования email."""
    uc = AccUseCase(AccRepo(__repo_session), __ads_svc, __compl_svc, __tg_svc)
    res = await uc.is_email_busy(req)
    return SuccessResp[ZIsBusy](payload=res)


@router.get(
    Enp.ACCOUNT_GET_ALL,
    summary="Получить все аккаунты",
    status_code=200,
)
async def get_accounts(
    __repo_session: Annotated[AsyncSession, Depends(get_account_repo_session)],
    __ads_svc: Annotated[AdsService, Depends(get_ads_serivce)],
    __compl_svc: Annotated[ComplService, Depends(get_compl_serivce)],
    __tg_svc: Annotated[TgClient, Depends(get_tg_bot)]
) -> SuccessResp[list[ZAccount]]:
    """Обрабатывает HTTP-запрос на получение списка всех аккаунтов."""
    uc = AccUseCase(AccRepo(__repo_session), __ads_svc, __compl_svc, __tg_svc)
    res = await uc.get_accounts()
    return SuccessResp[list[ZAccount]](payload=res)

@router.get(
    Enp.ACCOUNT_CURRENT,
    summary="Получить текущий аккаунт",
    status_code=200,
)
async def get_current_account(
    jwt: AJwt,
    __repo_session: Annotated[AsyncSession, Depends(get_account_repo_session)],
    __ads_svc: Annotated[AdsService, Depends(get_ads_serivce)],
    __compl_svc: Annotated[ComplService, Depends(get_compl_serivce)],
    __tg_svc: Annotated[TgClient, Depends(get_tg_bot)]
) -> SuccessResp[ZAccount]:
    """Обрабатывает HTTP-запрос на получение текущего аккаунта."""
    uc = AccUseCase(AccRepo(__repo_session), __ads_svc, __compl_svc, __tg_svc)

    if not jwt:
        raise ExpError(ExpCode.SYS_UNAUTHORIZE)

    acc_id = jwt["acc_id"]

    res = await uc.get_current_account(acc_id)
    return SuccessResp[ZAccount](payload=res)

@router.patch(
    Enp.ADM_SET_ROLE_ACCOUNT,
    summary="Изменить роль аккаунта (Администратор)",
    status_code=200,
    responses=responses(404)
)
async def set_role_account(
    jwt: AJwt,
    role: Annotated[AccRole, Query()],
    acc_id: Annotated[UUID, Path()],
    __repo_session: Annotated[AsyncSession, Depends(get_account_repo_session)],
    __ads_svc: Annotated[AdsService, Depends(get_ads_serivce)],
    __compl_svc: Annotated[ComplService, Depends(get_compl_serivce)],
    __tg_svc: Annotated[TgClient, Depends(get_tg_bot)]
) -> SuccessResp:
    """Обрабатывает HTTP-запрос администратора на изменение роли аккаунта."""
    uc = AccUseCase(AccRepo(__repo_session), __ads_svc, __compl_svc, __tg_svc)

    if not jwt:
        raise ExpError(ExpCode.SYS_UNAUTHORIZE)

    if jwt["role"] != AccRole.ADMIN.value:
        raise ExpError(ExpCode.ACC_INCORRECT_ROLE)

    await uc.set_role_account(acc_id, role)
    return SuccessResp()

@router.patch(
    Enp.ADM_SET_BAN_ACCOUNT,
    summary="Забанить аккаунт (Администратор)",
    status_code=200,
    responses=responses(404)
)
async def set_ban_account(
    jwt: AJwt,
    acc_id: Annotated[UUID, Path()],
    blocked_to: Annotated[BannedTo, Query()],
    reason_blocked: Annotated[str, Body()],
    __repo_session: Annotated[AsyncSession, Depends(get_account_repo_session)],
    __ads_svc: Annotated[AdsService, Depends(get_ads_serivce)],
    __compl_svc: Annotated[ComplService, Depends(get_compl_serivce)],
    __tg_svc: Annotated[TgClient, Depends(get_tg_bot)],
) -> SuccessResp:
    """Обрабатывает HTTP-запрос администратора на блокировку аккаунта."""
    uc = AccUseCase(AccRepo(__repo_session), __ads_svc, __compl_svc, __tg_svc)

    if not jwt:
        raise ExpError(ExpCode.SYS_UNAUTHORIZE)

    if jwt["role"] != AccRole.ADMIN.value:
        raise ExpError(ExpCode.ACC_INCORRECT_ROLE)

    await uc.set_ban_account(acc_id, blocked_to, reason_blocked)
    return SuccessResp()

@router.patch(
    Enp.ADM_SET_UNBAN_ACCOUNT,
    summary="Разбанить аккаунт (Администратор)",
    status_code=200,
    responses=responses(404),
)
async def set_unban_account(
    jwt: AJwt,
    acc_id: Annotated[UUID, Path()],
    __repo_session: Annotated[AsyncSession, Depends(get_account_repo_session)],
    __ads_svc: Annotated[AdsService, Depends(get_ads_serivce)],
    __compl_svc: Annotated[ComplService, Depends(get_compl_serivce)],
    __tg_svc: Annotated[TgClient, Depends(get_tg_bot)],
) -> SuccessResp:
    """Обрабатывает HTTP-запрос администратора на разблокировку аккаунта."""
    uc = AccUseCase(AccRepo(__repo_session), __ads_svc, __compl_svc, __tg_svc)

    if not jwt:
        raise ExpError(ExpCode.SYS_UNAUTHORIZE)

    if jwt["role"] != AccRole.ADMIN.value:
        raise ExpError(ExpCode.ACC_INCORRECT_ROLE)

    await uc.set_unban_account(acc_id)
    return SuccessResp()

@router.post(
    Enp.ACCOUNT_SEND_COMPLAINT,
    summary="Пожаловаться на аккаунт",
    status_code=200,
    responses=responses(400),
)
async def send_complaint(
    jwt: AJwt,
    acc_id: Annotated[UUID, Path()],
    msg: Annotated[str, Body()],
    __repo_session: Annotated[AsyncSession, Depends(get_account_repo_session)],
    __ads_svc: Annotated[AdsService, Depends(get_ads_serivce)],
    __compl_svc: Annotated[ComplService, Depends(get_compl_serivce)],
    __tg_svc: Annotated[TgClient, Depends(get_tg_bot)],
) -> SuccessResp[ZCompl]:
    uc = AccUseCase(AccRepo(__repo_session), __ads_svc, __compl_svc, __tg_svc)

    if not jwt:
        raise ExpError(ExpCode.SYS_UNAUTHORIZE)

    if jwt["is_banned"] == str(True):
        return SuccessResp[ZBanned](
            payload=ZBanned(
                account_id=jwt["acc_id"],
                is_banned=jwt["is_banned"],
                blocked_at=jwt["blocked_at"],
                reason_blocked=jwt["reason_blocked"],
                blocked_to=jwt["blocked_to"],
            )
        )

    if str(acc_id) == jwt["acc_id"]:
        raise ExpError(ExpCode.ACC_INCORRECT_ACCOUNT)

    req = QCreateCompl(
        compl_on_id=acc_id,
        service=Service.ACCOUNT,
        author_id=jwt["acc_id"],
        complaints=msg,
    )

    res = await uc.send_complaint(req)
    return SuccessResp[ZCompl](payload=res)
