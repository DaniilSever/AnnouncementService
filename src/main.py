import importlib
from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import ORJSONResponse
from core.exception import ExpError

services = {
    "auth.api": ("handlers.auth.api", True),
    "acc.api": ("handlers.account.api", True),
    "ads.api": ("handlers.ads.api", True),
    "compl.api": ("handlers.compl.api", True),
}


@asynccontextmanager
async def lifespan(__app: FastAPI):
    """Обрабатывает события жизненного цикла FastAPI-приложения.

    Args:
        __app (FastAPI): Экземпляр приложения FastAPI.

    Yields:
        None: Управление возвращается FastAPI во время работы приложения.
    """
    yield


def get_services() -> tuple[list[APIRouter], list[dict]]:
    """Импортирует активные сервисы и извлекает их роутеры и метаданные.

    Returns:
        tuple[list[APIRouter], list[dict]]: Список роутеров и описаний тегов для документации.
    """
    routers = []
    metadata = []
    for service, info in services.items():
        service_path, status = info
        if not status:
            print(f"{service}, DISABLE")
            continue
        try:
            module = importlib.import_module(service_path)
            if not module.router or not module.tags:
                raise KeyError("Отсутствует router + tags_metadata")
            routers.append(module.router)
            metadata.append(module.tags)
        except (ModuleNotFoundError, ImportError, KeyError) as e:
            print(e)
            continue

    return routers, metadata


def create_app() -> FastAPI:
    """Создаёт и настраивает экземпляр FastAPI-приложения для сервиса объявлений.

    Returns:
        FastAPI: Полностью сконфигурированное приложение FastAPI.
    """
    all_routers, all_tags_metadata = get_services()
    __app = FastAPI(
        title="Announcement Service",
        openapi_tags=all_tags_metadata,
        lifespan=lifespan,
        openapi_url="/api/openapi.json",
        docs_url="/api/swagger",
        redoc_url="/api/redoc",
        default_response_class=ORJSONResponse,
    )

    for router in all_routers:
        __app.include_router(router)

    @__app.exception_handler(ExpError)
    async def error_exception_handler(_: Request, exc: ExpError):
        return ORJSONResponse(
            status_code=int(exc.status_code), content=exc.response.model_dump()
        )

    return __app
