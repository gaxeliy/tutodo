import asyncio
import datetime

import pytest
from httpx import AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from app.database import Base
from app.dependencies import get_repository
from app.main import app
from app.tasks.serializers import ProjectSchema, TaskSchema
from app.tasks.use_cases import Repository


@pytest.fixture
def rep_():
    postgres = PostgresContainer('postgres:14.9-alpine3.18')
    with postgres:
        postgres.driver = "asyncpg"
        connection_url = postgres.get_connection_url()
        engine = create_async_engine(connection_url, echo=True, future=True, poolclass=NullPool)
        async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)  # type: ignore
        rep = Repository(async_session)

        async def init_models():
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)

        asyncio.run(init_models())

        yield rep


@pytest.fixture
def app_client(rep_):
    app.dependency_overrides[get_repository] = lambda: rep_
    return AsyncClient(app=app, base_url='http://localhost:8000/')


@pytest.fixture
def tasks_list(rep_):
    async def async_task_list():
        project = await rep_.create_project(ProjectSchema(title='project1',
                                                          description='project description1'))
        await rep_.create_task(TaskSchema(title='task1',
                                          description='task description1',
                                          done=False,
                                          created_at=datetime.datetime(1971, 1, 2),
                                          scheduled_at=datetime.datetime(1971, 2, 2),
                                          my_day_date=None,
                                          project_id=project.id))

    asyncio.run(async_task_list())
    yield
