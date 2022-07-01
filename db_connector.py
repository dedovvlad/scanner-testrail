from databases import Database
from sqlalchemy import MetaData

import config

DB_URL = f"postgresql://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"

db = Database(DB_URL)
metadata = MetaData()


async def db_connect():
    await db.connect()


async def db_disconnect():
    await db.disconnect()
