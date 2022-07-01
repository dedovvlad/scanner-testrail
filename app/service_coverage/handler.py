import re

from app.prometheus import CoverageMetrics

percent_pattern = re.compile(r"(\d+(\.\d+)?)")


class ServiceCoverage:
    @classmethod
    def handle(cls, team: str, service: str, content: str):
        match = percent_pattern.findall(content)
        if len(match) > 0:
            CoverageMetrics.write_gauge(team, service, float(match[0][0]))
