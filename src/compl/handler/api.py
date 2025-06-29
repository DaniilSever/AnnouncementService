from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, Depends, Body, Query, Path

from kernel.endpoints import Endpoints as Enp
from kernel.depends import get_compl_repo_session
from kernel.response import responses, SuccessResp
from kernel.security import AJwt
from kernel.exception import ExpError, ExpCode

from ..domain.dto import QCreateCompl, QFilter, ZCompl, ZManyCompl, ZBanned
from ..domain.models import Service
from account.domain.models import AccRole

from ..internal.uc import ComplUseCase

from ..infra.repo import ComplRepo, AsyncSession

router = APIRouter(tags=["compl"])
tags = {"name": "compl", "description": "Внутренние эндпоинты жалоб"}


@router.post(
    Enp.COMPL_ADD_COMPLAINT,
    summary="Создать жалобу через другой сервис (enp только для svc)",
    status_code=200,
)
async def create_compl(
    req: Annotated[QCreateCompl, Body()],
    __repo_session: Annotated[AsyncSession, Depends(get_compl_repo_session)],
) -> SuccessResp[ZCompl]:
    """Обрабатывает HTTP-запрос на создание новой жалобы."""
    uc = ComplUseCase(ComplRepo(__repo_session))
    res = await uc.create_compl(req)
    return SuccessResp[ZCompl](payload=res)


@router.get(
    Enp.COMPL_GET_MY_COMPLAINT,
    summary="Получить информацию по моей жалобе",
    status_code=200,
    responses=responses(400, 404),
)
async def get_my_complaint(
    jwt: AJwt,
    compl_id: Annotated[UUID, Path()],
    __repo_session: Annotated[AsyncSession, Depends(get_compl_repo_session)],
) -> SuccessResp[ZCompl]:
    """Обрабатывает HTTP-запрос на получение информации по жалобе пользователя."""
    uc = ComplUseCase(ComplRepo(__repo_session))

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

    account_id = jwt["acc_id"]

    res = await uc.get_my_complaint(compl_id, account_id)
    return SuccessResp[ZCompl](payload=res)


@router.get(
    Enp.COMPL_GET_MY_COMPLAINTS,
    summary="Получить список моих жалоб",
    status_code=200,
)
async def get_my_complaints(
    jwt: AJwt,
    __repo_session: Annotated[AsyncSession, Depends(get_compl_repo_session)],
    complaints_of: Annotated[Service | None, Query()] = None,
) -> SuccessResp[ZManyCompl]:
    """Обрабатывает HTTP-запрос на получение списка жалоб текущего пользователя."""
    uc = ComplUseCase(ComplRepo(__repo_session))

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

    account_id = jwt["acc_id"]

    res = await uc.get_my_complaints(account_id, complaints_of)
    return SuccessResp[ZManyCompl](payload=res)


@router.get(
    Enp.ADM_GET_COMPLAINTS,
    summary="Получить список жалоб (Администратор)",
    status_code=200,
)
async def adm_get_complaints(
    jwt: AJwt,
    qfilter: Annotated[QFilter, Query()],
    __repo_session: Annotated[AsyncSession, Depends(get_compl_repo_session)],
) -> SuccessResp[ZManyCompl]:
    """Обрабатывает HTTP-запрос администратора на получение списка жалоб."""
    uc = ComplUseCase(ComplRepo(__repo_session))

    if not jwt:
        raise ExpError(ExpCode.SYS_UNAUTHORIZE)

    if jwt["role"] != AccRole.ADMIN.value:
        raise ExpError(ExpCode.ADS_INCORRECT_ROLE)

    res = await uc.adm_get_complaints(qfilter)
    return SuccessResp[ZManyCompl](payload=res)


@router.get(
    Enp.ADM_GET_COMPLAINT_BY_ID,
    summary="Получить данные жалобы по ID (Администратор)",
    status_code=200,
)
async def adm_get_complaint(
    jwt: AJwt,
    compl_id: Annotated[UUID, Path()],
    __repo_session: Annotated[AsyncSession, Depends(get_compl_repo_session)],
) -> SuccessResp[ZCompl]:
    """Обрабатывает HTTP-запрос администратора на получение жалобы по ID."""
    uc = ComplUseCase(ComplRepo(__repo_session))

    if not jwt:
        raise ExpError(ExpCode.SYS_UNAUTHORIZE)

    if jwt["role"] != AccRole.ADMIN.value:
        raise ExpError(ExpCode.ADS_INCORRECT_ROLE)

    res = await uc.adm_get_complaint(compl_id)
    return SuccessResp[ZCompl](payload=res)
