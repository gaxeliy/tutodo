import asyncio
from unittest.mock import patch

import pytest
from httpx import AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from starlette.testclient import TestClient
from testcontainers.postgres import PostgresContainer

from app import dependencies
from app.database import Base
from app.dependencies import get_repository
from app.main import app
from app.tasks.use_cases import Repository


@pytest.fixture
def get_repository_():
    postgres = PostgresContainer(
        'postgres:14.9-alpine3.18', user='postgres', password='postgres', dbname='postgres', port=5432
    )
    with postgres:
        postgres.driver = "asyncpg"
        postgres.get_container_host_ip = lambda: "0.0.0.0"
        # postgres.port_to_expose = 5432
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
def app_client(get_repository_):
    app.dependency_overrides[get_repository] = lambda: get_repository_
    return AsyncClient(app=app, base_url='http://localhost:8000/')


@pytest.mark.asyncio
async def test_get_tasks(app_client):
    result = await app_client.post('/tasks/', json={'title': 'test',
                                             'description': 'test',
                                             'done': False,
                                             'scheduled_at': None,
                                             'my_day_date': None})
    assert result.status_code == 200
