from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, Depends, Body, Header, Query, Path

from core.endpoints import Endpoints as Enp
from core.depends import get_ads_repo_session, AsyncSession
from core.response import responses, SuccessResp
from core.security import AJwt, ApiKey
from core.exception import ErrExp, ExpCode

from app.ads.uc import AdsUseCase

from domain.ads.dto import QCreateAds, QFilter
from domain.ads.dto import ZAds

from infra.ads.repo import AdsRepo

router = APIRouter(tags=["ads"])
tags = {
    "name": "ads",
    "description": "Внутренние эндпоинты работы с объявлениями"
}

@router.post(
    Enp.ADS_CREATE,
    summary="Создать объявление",
    status_code=200,
    responses=responses(400, 404, 500, 503),
)
async def create_ads(
    jwt: AJwt,
    apikey: ApiKey,
    req: Annotated[QCreateAds, Body()],
    __repo_session: Annotated[AsyncSession, Depends(get_ads_repo_session)],
    account_id: Annotated[UUID | None, Header(description="Для APIKEY")] = None,
) -> SuccessResp[ZAds]:
    uc = AdsUseCase(AdsRepo(__repo_session))

    if not apikey and not jwt:
        raise ErrExp(ExpCode.SYS_UNAUTHORIZE)

    if jwt:
        account_id = jwt["sub"]

    res = await uc.create_ads(req, account_id)
    return SuccessResp[ZAds](payload=res)

@router.get(
    Enp.ADS_GET_ALL,
    summary="Получить все объявление по фильтру",
    status_code=200,
    responses=responses(400)
)
async def get_ads_all(
    qfilter: Annotated[QFilter, Query()],
    __repo_session: Annotated[AsyncSession, Depends(get_ads_repo_session)]
) -> SuccessResp[list[ZAds]]:
    uc = AdsUseCase(AdsRepo(__repo_session))
    res = await uc.get_ads_all(qfilter)
    return SuccessResp[list[ZAds]](payload=res)

@router.get(
    Enp.ADS_GET_BY_ID,
    summary="Получить объявление по его id",
    status_code=200,
    responses=responses(400,404)
)
async def get_ads_by_id(
    ads_id: Annotated[UUID, Query()],
    __repo_session: Annotated[AsyncSession, Depends(get_ads_repo_session)]
) -> SuccessResp[ZAds]:
    uc = AdsUseCase(AdsRepo(__repo_session))
    res = await uc.get_ads_by_id(ads_id)
    return SuccessResp[ZAds](payload=res)

@router.get(
    Enp.ADS_GET_BY_ACCOUNT,
    summary="Получить объявление по его id",
    status_code=200,
    responses=responses(400, 404)
)
async def get_ads_by_account(
    acc_id: Annotated[UUID, Query()],
    __repo_session: Annotated[AsyncSession, Depends(get_ads_repo_session)]
) -> SuccessResp[list[ZAds]]:
    uc = AdsUseCase(AdsRepo(__repo_session))
    res = await uc.get_ads_by_account_id(acc_id)
    return SuccessResp[list[ZAds]](payload=res)

@router.get(
    Enp.ADS_GET_BY_ME,
    summary="Получить мои объявления",
    status_code=200,
    responses=responses(400, 404)
)
async def get_my_ads(
    jwt: AJwt,
    __repo_session: Annotated[AsyncSession, Depends(get_ads_repo_session)]
) -> SuccessResp[list[ZAds]]:
    uc = AdsUseCase(AdsRepo(__repo_session))

    if not jwt:
        raise ErrExp(ExpCode.SYS_UNAUTHORIZE)
    acc_id = jwt["sub"]
    res = await uc.get_ads_by_account_id(acc_id)
    return SuccessResp[list[ZAds]](payload=res)
