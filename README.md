### Структура проекта:
```
├── metrics-service
│   ├── app                        Пакет для хранения разных саб-приложений
│   │   └── testrail               Пакет с саб-приложением Test Rail
│   │   │   ├ projects.yml         YML файл для хранения структуры с проектами из Test Rail
│   │   │   ├ testrail_request.py  Модуль с логикой по работе с API Test Rail
│   │   │   ├ structure.py         Модуль, где хранится темплейт структуры ответа с данными из Test Rail
│   │   └── service_coverage       Пакет с саб-приложением для забора % покрытия unit тестов в бэкенд сервисах
│   │   │   ├ handler.py           Модуль с логикой где матчится названия сервисов с % покрытия
│   │   ├── prometheus.py          Модуль с кастомизированным классом прометеус клиента
│   │   └── routes.py              Модуль, в котором хранится эндпоинт /metrics
│   ├── config.py                  Модуль, в котором хранятся конфигурации для работы с сервисом и внешними зависимостями
│   ├── main.py                    Главнй испольняемый модуль
│   └── requirements.txt           Зависимости для проекта
```

### Запуск сервиса локально:
1. Подключить виртуальное окружение Python
2. Установить все зависимости, выполнить из корня проекта команду `pip install -r requirements.txt`
3. Перейти в модуль main.py и запустить через интерпретатор IDE
4. Перейти в консоль и выполнить из корня проекта команду `python main.py`

### Изменение некоторых переменных:
Если есть необходимость изменения некоторых параметров для работы с сервисом или внешними приложениями, 
необходимо перейти в модуль `config.py` и изменить значение в переменной env

### Локальный запуск Prometheus + Grafana

```
логин/пароль для prometheus & grafana в UI admin/admin
```

1. Спуллить prometheus `docker pull prom/prometheus` (!) Возможно нужно выключить VPN 
2. Спуллить grafana `docker pull grafana/grafana`
3. Создать в корне проекта `prometheus.yml`
4. Внести в файл ^:
````
global:
  scrape_interval:     115s # By default, scrape targets every 115 seconds.

  # Attach these labels to any time series or alerts when communicating with
  # external systems (federation, remote storage, Alertmanager).
  external_labels:
    monitor: 'codelab-monitor'

# A scrape configuration containing exactly one endpoint to scrape:
# Here it's Prometheus itself.
scrape_configs:
  # The job name is added as a label `job=<job_name>` to any timeseries scraped from this config.
  - job_name: 'prometheus'

    # Override the global default and scrape targets from this job every 5 seconds.
    scrape_interval: 5s

    static_configs:
      - targets: ['host.docker.internal:8080']
````
5. Запустить приложение metrics-service на порту `8080`
6. Запустить образ Prometheus `docker run -p 9090:9090 -v {your_absolute_path}/metrics-service/prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus` 
из корня проекта
7. Запустить образ Grafana `docker run -d -p 3000:3000 --name grafana grafana/grafana` из корня проекта
8. Перейти в прометеус `http://localhost:9090/targets` - убедиться, что добавлен таргет с эндпоинтом и состояние `UP`
9. Перейти в графану `http://localhost:3000/datasources` - добавить source prometheus (browser) HTTP URL `http://localhost:9090`
10. Создать борд

### Версии зависимостей:
- Python 3.10 (не ниже)