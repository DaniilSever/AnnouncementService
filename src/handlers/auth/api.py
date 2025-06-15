from typing import Annotated
from fastapi import APIRouter, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm

from core.endpoints import Endpoints as Enp
from core.depends import (
    get_auth_repo_session,
    AsyncSession,
    get_account_serivce,
    AccService,
)
from core.response import responses, SuccessResp

from app.auth.uc import AuthUseCase

from domain.auth.dto import (
    QEmailSignup,
    QConfirmCode,
    QEmailSignin,
    QRefreshToken,
    QRevokeToken,
)
from domain.auth.dto import ZEmailSignup, ZAccountID, ZToken, ZRevokedTokens

from infra.auth.repo import AuthRepo

router = APIRouter(tags=["auth"])
tags = {"name": "auth", "description": "Внутренние эндпоинты авторизации"}

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
    responses=responses(400, 404),
)
async def signup_email(
    req: Annotated[QEmailSignup, Body()],
    __repo_session: Annotated[AsyncSession, Depends(get_auth_repo_session)],
    _acc_svc: Annotated[AccService, Depends(get_account_serivce)],
) -> SuccessResp[ZEmailSignup]:
    """Обрабатывает HTTP-запрос на регистрацию пользователя по email с отправкой кода подтверждения."""
    uc = AuthUseCase(AuthRepo(__repo_session), _acc_svc)
    res = await uc.signup_email(req)
    return SuccessResp[ZEmailSignup](payload=res)


@router.post(
    Enp.AUTH_CONFIRM_EMAIL,
    summary="Подтверждение емейла вводом кода",
    status_code=200,
    responses=responses(400, 404),
)
async def confirm_email(
    req: Annotated[QConfirmCode, Body()],
    __repo_session: Annotated[AsyncSession, Depends(get_auth_repo_session)],
    _acc_svc: Annotated[AccService, Depends(get_account_serivce)],
) -> SuccessResp[ZAccountID]:
    """Обрабатывает HTTP-запрос на подтверждение email с помощью кода подтверждения."""
    uc = AuthUseCase(AuthRepo(__repo_session), _acc_svc)
    res = await uc.confirm_email(req)
    return SuccessResp[ZAccountID](payload=res)


@router.post(
    Enp.AUTH_SIGNIN_EMAIL,
    summary="Авторизация в системе",
    status_code=200,
    responses=responses(400, 404),
)
async def signin_email(
    req: Annotated[QEmailSignin, Body()],
    __repo_session: Annotated[AsyncSession, Depends(get_auth_repo_session)],
    _acc_svc: Annotated[AccService, Depends(get_account_serivce)],
) -> SuccessResp[ZToken]:
    """Обрабатывает HTTP-запрос на авторизацию пользователя по email и паролю."""
    uc = AuthUseCase(AuthRepo(__repo_session), _acc_svc)
    res = await uc.signin_email(req)
    return SuccessResp[ZToken](payload=res)


@router.post(
    Enp.AUTH_SIGNIN_EMAIL_FORM,
    summary="Авторизация в системе (сваггер)",
    status_code=200,
    responses=responses(400, 404),
)
async def signin_email_form(
    form: Annotated[OAuth2PasswordRequestForm, Depends()],
    __repo_session: Annotated[AsyncSession, Depends(get_auth_repo_session)],
    _acc_svc: Annotated[AccService, Depends(get_account_serivce)],
) -> ZToken:
    """Обрабатывает HTTP-запрос на авторизацию пользователя по email и паролю через форму OAuth2."""
    uc = AuthUseCase(AuthRepo(__repo_session), _acc_svc)
    req = QEmailSignin(email=form.username, password=form.password)
    res = await uc.signin_email(req)
    return res


@router.post(
    Enp.AUTH_REFRESH_TOKEN,
    summary="Рефреш токена",
    status_code=200,
    responses=responses(400, 404),
)
async def refresh_token(
    req: Annotated[QRefreshToken, Body()],
    __repo_session: Annotated[AsyncSession, Depends(get_auth_repo_session)],
    _acc_svc: Annotated[AccService, Depends(get_account_serivce)],
) -> SuccessResp[ZToken]:
    """Обрабатывает HTTP-запрос на обновление access-токена с использованием refresh-токена."""
    uc = AuthUseCase(AuthRepo(__repo_session), _acc_svc)
    res = await uc.refresh_token(req)
    return SuccessResp[ZToken](payload=res)


@router.post(
    Enp.AUTH_REVOKE_TOKEN,
    summary="Деактивация докетов по acc_id",
    status_code=200,
    responses=responses(400, 404),
)
async def revoke_token(
    req: Annotated[QRevokeToken, Body()],
    __repo_session: Annotated[AsyncSession, Depends(get_auth_repo_session)],
    _acc_svc: Annotated[AccService, Depends(get_account_serivce)],
) -> SuccessResp[ZRevokedTokens]:
    """Обрабатывает HTTP-запрос на деактивацию (отзыв) токенов по идентификатору аккаунта."""
    uc = AuthUseCase(AuthRepo(__repo_session), _acc_svc)
    res = await uc.revoke_token(req)
    return SuccessResp[ZRevokedTokens](payload=res)
