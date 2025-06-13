from fastapi import APIRouter

router = APIRouter(tags=["ads"])
tags = {
    "name": "ads",
    "description": "Внутренние эндпоинты работы с объявлениями"
}
