from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, Depends, Body, Query, Path

from core.endpoints import Endpoints as Enp
from core.depends import get_compl_repo_session, AsyncSession
from core.response import responses, SuccessResp
from core.security import AJwt
from core.exception import ExpError, ExpCode

from domain.compl.dto import QCreateCompl, QFilter, ZCompl, ZManyCompl, ZBanned
from domain.compl.models import Service
from domain.account.models import AccRole

from app.compl.uc import ComplUseCase
from infra.compl.repo import ComplRepo

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
    uc = ComplUseCase(ComplRepo(__repo_session))

    if not jwt:
        raise ExpError(ExpCode.SYS_UNAUTHORIZE)

    if jwt["role"] != AccRole.ADMIN.value:
        raise ExpError(ExpCode.ADS_INCORRECT_ROLE)

    res = await uc.adm_get_complaint(compl_id)
    return SuccessResp[ZCompl](payload=res)
