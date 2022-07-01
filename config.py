import os

env = os.environ.get

# Конфиги для Test Rail
TESTRAIL_HOST = env(
    "TESTRAIL_HOST", ""
)
TESTRAIL_USER = env("TESTRAIL_USER", "")
TESTRAIL_PASSWORD = env("TESTRAIL_PASSWORD", "")

# Конфиги для Uvicorn
DEBUG = env("DEBUG", True)
PREFIX = env("PREFIX", "")
UVICORN_HOST = env("UVICORN_HOST", "0.0.0.0")
UVICORN_PORT = env("UVICORN_PORT", 8080)

# Время задержки в цикле
DELAY = env("DELAY", 43200)

# Postgres
DB_USER = env("DB_USER", "postgres")
DB_PASSWORD = env("DB_PASSWORD", "postgres")
DB_NAME = env("DB_NAME", "postgres")
DB_HOST = env("DB_HOST", "postgres")
DB_PORT = env("DB_PORT", 5432)
