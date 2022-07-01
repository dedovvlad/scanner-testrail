import http
import os

from fastapi import APIRouter, Body, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.service_coverage.handler import ServiceCoverage

router = APIRouter(tags=["Metrics"])

app_version = os.getenv("VERSION")
app_name = os.getenv("APP")
app_build_number = os.getenv("BUILD_NUMBER")


@router.get("/health/check", summary="Health Check")
async def health_check():
    """Health Check"""
    return {
        "app_version": app_version,
        "app_build_number": app_build_number,
        "app_name": app_name,
    }


@router.get("/metrics")
async def get_metrics():
    """
    Асинхронная функция вызывается как эндпоинт.
    Отдает метрики для prometheus
    """
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@router.post("/coverage/{team}/{service}")
async def post_service_coverage(team: str, service: str, body: str = Body(...)):
    """
    Принимает значение покрытия сервиса тестами
    """
    ServiceCoverage.handle(team, service, body)
    return Response(
        "", status_code=http.HTTPStatus.NO_CONTENT, media_type=CONTENT_TYPE_LATEST
    )
