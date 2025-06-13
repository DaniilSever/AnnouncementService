from typing import Annotated
from fastapi import APIRouter, Depends, Body

from core.endpoints import Endpoints as Enp
from core.depends import get_auth_repo_session, AsyncSession
from core.response import responses, SuccessResp

from app.auth.uc import AuthUseCase

from domain.auth.dto import QEmailSignup, QConfirmCode
from domain.auth.dto import ZEmailSignup, ZAccountID

from infra.auth.repo import AuthRepo

router = APIRouter(tags=["auth"])
tags = {
    "name": "auth",
    "description": "Внутренние эндпоинты авторизации"
}

# @router.get(
#     Enp.AUTH_HEALTHCHECK,
#     summary="Проверка работоспособности Auth сервиса",
#     status_code=200,
# )
# async def healthcheck(
#     _repo_session = Depends(get_auth_repo_session)
# ):
#     pass


@router.post(
    Enp.AUTH_SIGNUP_EMAIL,
    summary="Регистрация по email+пароль, с отправкой кода подтверждения",
    status_code=200,
    responses=responses(400, 404)
)
async def signup_email(
    req: Annotated[QEmailSignup, Body()],
    _repo_session: Annotated[AsyncSession, Depends(get_auth_repo_session)],
) -> SuccessResp[ZEmailSignup]:
    uc = AuthUseCase(AuthRepo(_repo_session))
    res = await uc.signup_email(req)
    return SuccessResp[ZEmailSignup](payload=res)

@router.post(
    Enp.AUTH_CONFIRM_EMAIL,
    summary="Подтверждение емейла вводом кода",
    status_code=200,
    responses=responses(400, 404)
)
async def confirm_email(
    req: Annotated[QConfirmCode, Body()],
    _repo_session: Annotated[AsyncSession, Depends(get_auth_repo_session)],
) -> SuccessResp[ZAccountID]:
    uc = AuthUseCase(AuthRepo(_repo_session))
    res = await uc.confirm_email(req)
    return SuccessResp[ZAccountID](payload=res)
