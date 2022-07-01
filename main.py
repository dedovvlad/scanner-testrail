import asyncio
import threading
import time

import uvicorn
from fastapi import FastAPI

from app.routes import router
from app.testrail.testrail_request import TestRail
from config import DELAY, PREFIX, UVICORN_HOST, UVICORN_PORT

app = FastAPI()
app.include_router(
    router=router,
    prefix=PREFIX,
)


def run_loop_for_update_metrics():
    """
    Бесконечный цикл для того,
    чтобы итеративно с некоторой задержкой получать данные из сервисов.
    Этот цикл дает возможность получать метрики моментально не нагружая сервисы.

    Цикл работает в фоне, с заданным интервалом обращается к сервису.
    """
    while True:
        asyncio.run(TestRail().get_service_info())
        time.sleep(DELAY)


if __name__ == "__main__":
    # Запуск отдельного треда с циклом, который итеративно с задержкой ходит в сервис
    th = threading.Thread(target=run_loop_for_update_metrics, daemon=True)
    th.start()

    # Запуск HTTP сервера UVICORN для возможности получения данных по эндпоинту /metrics
    uvicorn.run(app=app, host=UVICORN_HOST, port=UVICORN_PORT)
