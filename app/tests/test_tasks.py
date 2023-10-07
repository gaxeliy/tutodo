import os

import pytest

from app.tests.fixtures import rep_, app_client, tasks_list

os.chdir('..')


@pytest.mark.asyncio
async def test_create_task(app_client, rep_):
    result = await app_client.post('/tasks/', json={'title': 'test',
                                                    'description': 'test',
                                                    'done': False,
                                                    'scheduled_at': None,
                                                    'my_day_date': None})
    assert result.status_code == 200
    assert result.json()['data']['title'] == 'test'
    assert result.json()['data']['description'] == 'test'
    assert result.json()['data']['done'] is False
    assert result.json()['data']['scheduled_at'] is None
    assert result.json()['data']['my_day_date'] is None

    tasks = await rep_.get_tasks()
    assert len(tasks) <= 1
    pass


@pytest.mark.asyncio
async def test_get_tasks(app_client, rep_, tasks_list):
    result = await app_client.get('/tasks/')
    assert result.status_code == 200
    assert result.headers['content-type'] == 'application/json'
    result = await app_client.get('/tasks/', headers={'HX-Request': 'true'})
    assert result.status_code == 200
    assert 'text/html' in result.headers['content-type']
    pass


@pytest.mark.asyncio
async def test_get_task(app_client, rep_, tasks_list):
    result = await app_client.get('/tasks/1')
    assert result.status_code == 200
    assert result.headers['content-type'] == 'application/json'
    # TODO: Раскомментировать, когда доделаем hypermedia-api
    # result = await app_client.get('/tasks/1', headers={'HX-Request': 'true'})
    # assert result.status_code == 200
    # assert 'text/html' in result.headers['content-type']
    pass


@pytest.mark.asyncio
async def test_delete_task(app_client, rep_, tasks_list):
    result = await app_client.delete('/tasks/1')
    assert result.status_code == 200
    tasks = await rep_.get_tasks()
    assert len(tasks) == 0
    pass


@pytest.mark.asyncio
async def test_undone_task(app_client, rep_, tasks_list):
    result = await app_client.post('/tasks/done/1')
    assert result.status_code == 200
    tasks = await rep_.get_tasks()
    assert tasks[0].done is True
    result = await app_client.post('/tasks/undone/1')
    assert result.status_code == 200
    tasks = await rep_.get_tasks()
    assert tasks[0].done is False
    pass


@pytest.mark.asyncio
async def test_create_project(app_client, rep_):
    result = await app_client.post('/tasks/projects', json={'title': 'test',
                                                            'description': 'test'})
    assert result.status_code == 200
    assert result.json()['data']['title'] == 'test'
    assert result.json()['data']['description'] == 'test'
    pass
