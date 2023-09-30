import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import sessionmaker
from starlette.requests import Request
from starlette.responses import HTMLResponse

from app.helpers import get_response_class
from app.tasks.models import Tag
from app.tasks.serializers import TaskCreateRequest, TaskSchema, ProjectSchema, ProjectCreateRequest, \
    ProjectByIdResponse, TagSchema, TagResponse, TaskSchemaListResponse
from app.tasks.use_cases import Repository
from app.dependencies import get_repository

router = APIRouter(
    prefix='/tasks', tags=['tasks'],
)


@router.get('/', response_class=get_response_class('task_list.html'))
async def get_tasks(request: Request, rep: Annotated[Repository, Depends(get_repository)]) -> TaskSchemaListResponse:
    all_tasks = await rep.get_tasks()
    return TaskSchemaListResponse(tasks=all_tasks, headers=request.headers)


@router.post('/')
async def create_task(task_create_request: TaskCreateRequest,
                      rep: Annotated[Repository, Depends(get_repository)]) -> TaskSchema:
    task_schema_dict = task_create_request.model_dump()
    task_schema_dict = {**task_schema_dict, 'created_at': datetime.datetime.now(), 'id': None}
    task_schema = TaskSchema(
        **task_schema_dict
    )
    task_schema = await rep.create_task(task_schema)
    return task_schema


@router.get('/{id}')
async def get_task(id: int, rep: Annotated[Repository, Depends(get_repository)]) -> TaskSchema:
    task = await rep.get_task(id)
    return TaskSchema(**task.__dict__)


@router.post('/done/{task_id}')
async def done_task(task_id: int,
                    rep: Annotated[Repository, Depends(get_repository)]) -> TaskSchema:
    return await rep.getting_done(task_id)


@router.post('/undone/{task_id}')
async def undone_task(task_id: int,
                      rep: Annotated[Repository, Depends(get_repository)]) -> TaskSchema:
    return await rep.getting_done(task_id, done=False)


@router.delete('/{id}')
async def delete_task(id: int, rep: Annotated[Repository, Depends(get_repository)]):
    await rep.delete_task(id)


@router.get('/projects/')
async def get_projects(rep: Annotated[Repository, Depends(get_repository)]) -> list[ProjectSchema]:
    all_projects = await rep.get_projects()
    return all_projects


@router.get('/projects/{id}')
async def get_project(id: int, rep: Annotated[Repository, Depends(get_repository)]) -> ProjectByIdResponse:
    project = await rep.get_project(id)
    tasks = await rep.get_tasks_by_project_id(id)
    return ProjectByIdResponse(**project.__dict__, tasks=tasks)


@router.post('/projects')
async def create_project(project_create_request: ProjectCreateRequest,
                         rep: Annotated[Repository, Depends(get_repository)]) -> ProjectSchema:
    project_schema_dict = project_create_request.model_dump()
    project_schema_dict = {**project_schema_dict, 'id': None}
    project_schema = ProjectSchema(
        **project_schema_dict
    )
    project_schema = await rep.create_project(project_schema)
    return project_schema


@router.delete('/projects/{id}')
async def delete_project(id: int, rep: Annotated[Repository, Depends(get_repository)]):
    await rep.delete_project(id)


@router.post('/projects/{task_id}/{project_id}')
async def attach_project_to_task(task_id: int, project_id: int, rep: Annotated[Repository, Depends(get_repository)]):
    await rep.attach_project_task(task_id, project_id)


@router.get('/tags/')
async def get_tags(rep: Annotated[Repository, Depends(get_repository)]) -> list[TagSchema]:
    all_tags = await rep.get_tags()
    return all_tags


@router.get('/tags/{id}')
async def get_tag(id: int, rep: Annotated[Repository, Depends(get_repository)]) -> TagResponse:
    tag = await rep.get_tag(id)
    tasks = await rep.get_tasks_by_tag_id(id)

    return TagResponse(**tag.__dict__, tasks=tasks)


@router.post('/tags')
async def create_tag(tag: str, rep: Annotated[Repository, Depends(get_repository)]) -> TagSchema:
    tag = await rep.create_tag(tag)
    return tag


@router.post('/tags/{task_id}/{tag_id}')
async def attach_task_to_tag(task_id: int, tag_id: int, rep: Annotated[Repository, Depends(get_repository)]):
    await rep.attach_task_to_tag(task_id, tag_id)


@router.delete('/tags/{id}')
async def delete_tag(id: int, rep: Annotated[Repository, Depends(get_repository)]):
    await rep.delete_tag(id)
