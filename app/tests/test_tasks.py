import asyncio
from unittest.mock import patch

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from starlette.testclient import TestClient
from testcontainers.postgres import PostgresContainer

from app import dependencies
from app.database import Base
from app.main import app
from app.tasks.use_cases import Repository


@pytest.fixture
def get_repository_():
    postgres = PostgresContainer(
        'postgres:14.9-alpine3.18',
    )
    with postgres:
        postgres.driver = "asyncpg"
        engine = create_async_engine(postgres.get_connection_url(), echo=True, future=True)
        async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)  # type: ignore
        rep = Repository(async_session)

        async def init_models():
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)
        asyncio.run(init_models())

        with patch.object(dependencies, 'get_repository', return_value=rep):
            yield


@pytest.fixture
def app_client(get_repository_):
    return TestClient(app)


@pytest.mark.asyncio
async def test_get_tasks(app_client):
    result = app_client.post('/tasks', json={'title': 'test',
                                             'description': 'test',
                                             'done': False,
                                             'scheduled_at': None,
                                             'my_day_date': None})
    pass
