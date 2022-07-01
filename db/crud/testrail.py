from datetime import datetime

from sqlalchemy import select

from db.model.testrail import testrail
from db_connector import db


async def insert_data(project: str, suite: str, data_type: str, data: dict):
    query = testrail.insert().values(
        project=project,
        suite=suite,
        create_datetime=datetime.now(),
        data_type=data_type,
        data=data,
        is_old=False,
    )
    return await db.execute(query)


async def update_data():
    query = testrail.update().where(testrail.c.is_old == False).values(is_old=True)
    return await db.execute(query)


async def get_data():
    return await db.fetch_all(
        select(
            testrail.c.project, testrail.c.suite, testrail.c.data_type, testrail.c.data
        ).where(testrail.c.is_old == False)
    )
