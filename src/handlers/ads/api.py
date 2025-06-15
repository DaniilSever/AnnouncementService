from uuid import UUID
from typing import Annotated
from fastapi import APIRouter, Depends, Body, Header, Query, Path

from core.endpoints import Endpoints as Enp
from core.depends import get_ads_repo_session, AsyncSession
from core.response import responses, SuccessResp
from core.security import AJwt, ApiKey
from core.exception import ExpError, ExpCode

from app.ads.uc import AdsUseCase

from domain.ads.dto import (
    QCreateAds,
    QAdsCategory,
    QFilter,
    QChangeAds,
    QAddAdsComment,
    QUpdateAdsComment,
    QDelAdsComment,
)
from domain.ads.dto import ZAds, ZAdsComment, ZManyAds, ZManyAdsComment

from infra.ads.repo import AdsRepo

router = APIRouter(tags=["ads"])
tags = {"name": "ads", "description": "Внутренние эндпоинты работы с объявлениями"}


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
    ads_category: QAdsCategory = QAdsCategory.SELLING,
) -> SuccessResp[ZAds]:
    """Обрабатывает HTTP-запрос на создание объявления с авторизацией и валидацией."""
    uc = AdsUseCase(AdsRepo(__repo_session))

    if not apikey and not jwt:
        raise ExpError(ExpCode.SYS_UNAUTHORIZE)

    if jwt:
        account_id = jwt["sub"]

    res = await uc.create_ads(req, ads_category, account_id)
    return SuccessResp[ZAds](payload=res)


@router.get(
    Enp.ADS_GET_ALL,
    summary="Получить все объявление по фильтру",
    status_code=200,
    responses=responses(400),
)
async def get_ads_all(
    qfilter: Annotated[QFilter, Query()],
    __repo_session: Annotated[AsyncSession, Depends(get_ads_repo_session)],
) -> SuccessResp[ZManyAds]:
    """Обрабатывает HTTP-запрос на получение всех объявлений по фильтру."""
    uc = AdsUseCase(AdsRepo(__repo_session))
    res = await uc.get_ads_all(qfilter)
    return SuccessResp[ZManyAds](payload=res)


@router.get(
    Enp.ADS_GET_BY_ID,
    summary="Получить объявление по его id",
    status_code=200,
    responses=responses(400, 404),
)
async def get_ads_by_id(
    ads_id: Annotated[UUID, Query()],
    __repo_session: Annotated[AsyncSession, Depends(get_ads_repo_session)],
) -> SuccessResp[ZAds]:
    """Обрабатывает HTTP-запрос на получение объявления по его идентификатору."""
    uc = AdsUseCase(AdsRepo(__repo_session))
    res = await uc.get_ads_by_id(ads_id)
    return SuccessResp[ZAds](payload=res)


@router.get(
    Enp.ADS_GET_BY_ACCOUNT,
    summary="Получить все объявления пользователя",
    status_code=200,
    responses=responses(400, 404),
)
async def get_ads_by_account(
    acc_id: Annotated[UUID, Query()],
    __repo_session: Annotated[AsyncSession, Depends(get_ads_repo_session)],
) -> SuccessResp[ZManyAds]:
    """Обрабатывает HTTP-запрос на получение всех объявлений пользователя."""
    uc = AdsUseCase(AdsRepo(__repo_session))
    res = await uc.get_ads_by_account_id(acc_id)
    return SuccessResp[ZManyAds](payload=res)


@router.get(
    Enp.ADS_GET_BY_ME,
    summary="Получить мои объявления",
    status_code=200,
    responses=responses(400, 404),
)
async def get_my_ads(
    jwt: AJwt,
    __repo_session: Annotated[AsyncSession, Depends(get_ads_repo_session)],
) -> SuccessResp[ZManyAds]:
    """Обрабатывает HTTP-запрос на получение моих объявлений с авторизацией."""
    uc = AdsUseCase(AdsRepo(__repo_session))

    if not jwt:
        raise ExpError(ExpCode.SYS_UNAUTHORIZE)
    acc_id = jwt["sub"]
    res = await uc.get_ads_by_account_id(acc_id)
    return SuccessResp[ZManyAds](payload=res)


@router.patch(
    Enp.ADS_CHANGE,
    summary="Изменить мое объявление",
    status_code=200,
    responses=responses(400, 404),
)
async def change_my_ads(
    jwt: AJwt,
    req: QChangeAds,
    __repo_session: Annotated[AsyncSession, Depends(get_ads_repo_session)],
) -> SuccessResp[ZAds]:
    """Обрабатывает HTTP-запрос на изменение моего объявления с авторизацией."""
    uc = AdsUseCase(AdsRepo(__repo_session))

    if not jwt:
        raise ExpError(ExpCode.SYS_UNAUTHORIZE)
    acc_id = jwt["sub"]
    res = await uc.change_my_ads(req, acc_id)
    return SuccessResp[ZAds](payload=res)


@router.patch(
    Enp.ADS_CHANGE_CATEGORY,
    summary="Изменить категорию объявления",
    status_code=200,
    responses=responses(400, 404),
)
async def change_category_ads(
    jwt: AJwt,
    ads_id: Annotated[UUID, Path()],
    req: Annotated[QAdsCategory, Query()],
    __repo_session: Annotated[AsyncSession, Depends(get_ads_repo_session)],
) -> SuccessResp[ZAds]:
    """Обрабатывает HTTP-запрос на изменение категории объявления с авторизацией."""
    uc = AdsUseCase(AdsRepo(__repo_session))

    if not jwt:
        raise ExpError(ExpCode.SYS_UNAUTHORIZE)
    acc_id = jwt["sub"]
    res = await uc.change_category_ads(ads_id, req, acc_id)
    return SuccessResp[ZAds](payload=res)


@router.delete(
    Enp.ADS_DELETE,
    summary="Удалить объявление",
    status_code=200,
    responses=responses(400, 404),
)
async def delete_ads(
    jwt: AJwt,
    ads_id: Annotated[UUID, Path()],
    __repo_session: Annotated[AsyncSession, Depends(get_ads_repo_session)],
) -> SuccessResp:
    """Обрабатывает HTTP-запрос на удаление объявления с авторизацией."""
    uc = AdsUseCase(AdsRepo(__repo_session))

    if not jwt:
        raise ExpError(ExpCode.SYS_UNAUTHORIZE)
    acc_id = jwt["sub"]
    await uc.delete_ads(ads_id, acc_id)
    return SuccessResp()


@router.post(
    Enp.ADS_ADD_COMMENTARY,
    summary="Добавить комментарий к объявлению",
    status_code=200,
    responses=responses(400, 404),
)
async def create_ads_commentary(
    jwt: AJwt,
    ads_id: Annotated[UUID, Path()],
    commentary: Annotated[str, Body()],
    __repo_session: Annotated[AsyncSession, Depends(get_ads_repo_session)],
) -> SuccessResp[ZAdsComment]:
    """Обрабатывает HTTP-запрос на добавление комментария к объявлению с авторизацией."""
    uc = AdsUseCase(AdsRepo(__repo_session))

    if not jwt:
        raise ExpError(ExpCode.SYS_UNAUTHORIZE)
    acc_id = jwt["sub"]

    req = QAddAdsComment(ads_id=ads_id, ads_comment=commentary)
    res = await uc.create_ads_commentary(req, acc_id)
    return SuccessResp[ZAdsComment](payload=res)


@router.get(
    Enp.ADS_GET_COMMENTATIES,
    summary="Получить список комментариев в объявлении",
    status_code=200,
    responses=responses(400, 404),
)
async def get_ads_commentaries(
    ads_id: Annotated[UUID, Path()],
    __repo_session: Annotated[AsyncSession, Depends(get_ads_repo_session)],
) -> SuccessResp[ZManyAdsComment]:
    """Обрабатывает HTTP-запрос на получение списка комментариев в объявлении."""
    uc = AdsUseCase(AdsRepo(__repo_session))
    res = await uc.get_ads_commentaries(ads_id)
    return SuccessResp[ZManyAdsComment](payload=res)


@router.get(
    Enp.ADS_ACTION_COMMENTARY,
    summary="Получить данные по комментарию в объявлении",
    status_code=200,
    responses=responses(400, 404),
)
async def get_ads_commentary(
    ads_id: Annotated[UUID, Path()],
    comm_id: Annotated[UUID, Path()],
    __repo_session: Annotated[AsyncSession, Depends(get_ads_repo_session)],
) -> SuccessResp[ZAdsComment]:
    """Обрабатывает HTTP-запрос на получение данных по комментарию в объявлении."""
    uc = AdsUseCase(AdsRepo(__repo_session))
    res = await uc.get_ads_commentary(ads_id, comm_id)
    return SuccessResp[ZAdsComment](payload=res)


@router.patch(
    Enp.ADS_ACTION_COMMENTARY,
    summary="Изменить комментарий в объявлении",
    status_code=200,
    responses=responses(400, 404),
)
async def update_ads_commentary(
    jwt: AJwt,
    ads_id: Annotated[UUID, Path()],
    comm_id: Annotated[UUID, Path()],
    commentary: Annotated[str, Body()],
    __repo_session: Annotated[AsyncSession, Depends(get_ads_repo_session)],
) -> SuccessResp[ZAdsComment]:
    """Обрабатывает HTTP-запрос на изменение комментария в объявлении с авторизацией."""
    uc = AdsUseCase(AdsRepo(__repo_session))

    if not jwt:
        raise ExpError(ExpCode.SYS_UNAUTHORIZE)
    acc_id = jwt["sub"]

    req = QUpdateAdsComment(
        comm_id=comm_id, ads_id=ads_id, acccount_id=acc_id, ads_comment=commentary
    )
    res = await uc.update_ads_commentary(req)
    return SuccessResp[ZAdsComment](payload=res)


@router.delete(
    Enp.ADS_ACTION_COMMENTARY,
    summary="Удалить комментарий в объявлении",
    status_code=200,
    responses=responses(400, 404),
)
async def delete_ads_commentary(
    jwt: AJwt,
    ads_id: Annotated[UUID, Path()],
    comm_id: Annotated[UUID, Path()],
    __repo_session: Annotated[AsyncSession, Depends(get_ads_repo_session)],
) -> SuccessResp:
    """Обрабатывает HTTP-запрос на удаление комментария в объявлении."""
    uc = AdsUseCase(AdsRepo(__repo_session))

    if not jwt:
        raise ExpError(ExpCode.SYS_UNAUTHORIZE)
    acc_id = jwt["sub"]

    req = QDelAdsComment(comm_id=comm_id, ads_id=ads_id, account_id=acc_id)
    await uc.delete_ads_commentary(req)
    return SuccessResp()
