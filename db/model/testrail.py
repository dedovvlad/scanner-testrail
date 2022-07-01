from sqlalchemy import (JSON, Boolean, Column, DateTime, Integer, String,
                        Table, func)

from db_connector import metadata

testrail = Table(
    "testrail",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("project", String),
    Column("suite", String),
    Column("create_datetime", DateTime, default=func.now(), nullable=False),
    Column("data_type", String),
    Column("data", JSON),
    Column("is_old", Boolean),
)
