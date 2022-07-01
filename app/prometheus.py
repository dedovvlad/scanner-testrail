from collections import defaultdict

from prometheus_client.core import REGISTRY, GaugeMetricFamily


class CustomPrometheusMetrics:
    """Класс в котором кастомизировн интерфейс Gauge."""

    structure = []

    def collect(self):
        """
        Дефолтная функция для корректной работы прометеус клиента.
        """
        for data in self.structure:
            if data:
                testrail_data = GaugeMetricFamily(
                    f"get_testrail_data_{data['data_type']}",
                    "Данные Test Rail по проектам",
                    labels=["project_name", "suite_name", data["data_type"]],
                )
                for types, count in data["data"].items():
                    testrail_data.add_metric(
                        labels=[
                            data["project"],
                            data["suite"],
                            types,
                        ],
                        value=count,
                    )
                yield testrail_data


class CoverageMetrics:
    """Обертка над метрикой code-coverage сервисов"""

    _structure = defaultdict(dict)

    @classmethod
    def write_gauge(cls, team: str, service: str, coverage: float):
        """
        Метод для обновления счетчика code coverage
        """
        cls._structure[team].update({service: coverage})

    def collect(self):
        """
        Дефолтная функция для корректной работы прометеус клиента.
        """
        request_metric = GaugeMetricFamily(
            "get_code_coverage",
            "Метрика для вывода code coverage сервисов",
            labels=["team", "service"],
        )

        for team, services in self._structure.items():
            for service, coverage in services.items():
                request_metric.add_metric(labels=[team, service], value=coverage)

        yield request_metric


# Необходимая инициализация клиента прометеуса, для корректной работы класса
# CustomPrometheusMetrics
REGISTRY.register(CustomPrometheusMetrics())
REGISTRY.register(CoverageMetrics())
