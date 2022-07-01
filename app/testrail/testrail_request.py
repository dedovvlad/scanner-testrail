from loguru import logger

import config
from app.core.request import AsyncAPIClient
from app.core.utils import FileHelper
from app.prometheus import CustomPrometheusMetrics
from db.crud.testrail import get_data, insert_data, update_data
from db_connector import db, db_connect, db_disconnect


class TestRail(AsyncAPIClient):
    """
    Класс для непосредственной работы с API,
    также класс агрегирует полученные ответы в общий темплейт.
    """

    def __init__(self):
        super().__init__(
            url=config.TESTRAIL_HOST,
            user=config.TESTRAIL_USER,
            password=config.TESTRAIL_PASSWORD,
        )

    async def get_service_info(self):
        """
        Асинхронная функция является основной вызываемой.

        Функция содержит в себе функцию генератор get_suite.

        Алгоритм функции содержит цикл в цикле, который рекурсивно проходит по
        .yml и вызывает API для каждого проекта + каждого сьюта

        На выходе функция обновляет dict CustomPrometheusMetrics.structure строками из БД
        """

        # АПИ вызовы используются для счетчиков искомых данных
        global response_priority, response_automation_state, response_case_type

        response_priority = await self.get("get_priorities")
        response_case_type = await self.get("get_case_types")
        response_automation_state = FileHelper.string_processing(
            next(
                (
                    x["configs"][0]["options"].get("items")
                    for x in await self.get("get_case_fields")
                    if x["system_name"] == "custom_automation_state"
                ),
                "undefined",
            )
        )

        _test_rail_date = []
        if not db.is_connected:
            await db_connect()
        await update_data()

        async def get_suite(pr_name: str):
            """
            Асинхронная функция генератор, необходима для того,
            чтобы разделить список проектов на три объекта.

            project_id - идентификатор пространства в Test Rail
            suite_name - имя Suite в Test Rail
            suite_id - - идентификатор Suite в Test Rail

            Функция нужна для того чтобы цикл на втором уровне мог асинхронно записывать
            в template вложенные словари с данными по Test Rail

            :param pr_name: имя проекта Test Rail из .yml
            """
            async for project_name, project_meta in self.get_config_data():

                # Проверка на случай, если в файле projects.yml проект окажется без сьютов
                try:
                    if project_name == pr_name:
                        for suite_name, suite_id in project_meta.get("suites").items():
                            yield project_meta.get("project_id"), suite_name, suite_id

                except AttributeError:
                    logger.error(f"Structure: projects.yml '{project_name}' is empty")

        async for project_name, _ in self.get_config_data():

            async for project_id, suite_name, suite_id in get_suite(project_name):
                case_data = await self.get_amount_cases(
                    project_id=project_id, suite_id=suite_id
                )
                for data_type, data in case_data.items():
                    await insert_data(project_name, suite_name, data_type, data)

        CustomPrometheusMetrics.structure = [dict(row) for row in await get_data()]
        await db_disconnect()

    @staticmethod
    async def get_config_data():
        """
        Асинхронная функция генератор, которая отдает
        project_name - имя пространства в Test Rail
        project_meta - идентификатор пространства и список сьютов из .yml
        """
        file = FileHelper.parse_yaml("app/testrail/projects.yml")

        # Проверка на случай, если файл projects.yml окажется пустым
        try:
            for project_name, project_meta in file.items():
                yield project_name, project_meta
        except AttributeError:
            logger.error("Structure: projects.yml is empty")

    async def get_amount_cases(self, project_id: int, suite_id: int) -> dict:
        """
        Асинхронная функция, используется как связка
        между внешней функцией get_service_info и функцией get_method из класса API.

        :param project_id: идентификатор пространства int
        :param suite_id: идентификатор сьюта int
        :return: возвращает dict с искомыми объектами и счетчиками,
        """
        response = await self.get(f"get_cases/{project_id}&suite_id={suite_id}")

        # счетчики для элементов из поля 'Priority', 'Automation State', 'Type'
        priority, status_auto, case_type = {}, {}, {}

        # Луп, в котором инкрементируются счетчики по соответствующим полям
        for cases in response:
            # Проверка на наличие текущего проекта или сьюта
            if isinstance(response, dict) and response.get("error"):
                logger.error(
                    f"{response.get('error')},"
                    f"project id: {project_id},"
                    f"suite id: {suite_id}"
                )
                continue

            # секция для инкремента счетчиков 'Priority', 'Automation State', 'Type'
            increment_sections = (
                (response_priority, priority, "priority_id"),
                (response_case_type, case_type, "type_id"),
                (response_automation_state, status_auto, "custom_automation_state"),
            )

            for response_item, structure, field in increment_sections:
                matching = str(
                    next(
                        (
                            x.get("name")
                            for x in response_item
                            if x["id"] == cases.get(field)
                        ),
                        "undefined",
                    )
                ).lower()

                if matching not in structure:
                    structure.update({matching: 1})
                else:
                    structure[matching] += 1

        # Ответ в dict для передачи в БД
        return {
            "priority": priority,
            "automation_state": status_auto,
            "case_type": case_type,
        }
