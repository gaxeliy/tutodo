import datetime
from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.dependencies import get_repository
from app.helpers import get_response_class, pass_headers, ResponseWithHeaders
from app.tasks.serializers import TaskCreateRequest, TaskSchema, ProjectSchema, ProjectCreateRequest, \
    ProjectByIdResponse, TagSchema, TagResponse
from app.tasks.use_cases import Repository

router = APIRouter(
    prefix='/tasks', tags=['tasks'],
)


@router.get('/',
            response_class=get_response_class('task_list.html'),
            response_model=ResponseWithHeaders[list[TaskSchema]])
@pass_headers
async def get_tasks(request: Request, rep: Annotated[Repository, Depends(get_repository)]) -> list[TaskSchema]:
    all_tasks = await rep.get_tasks()
    return all_tasks


@router.post('/',
             response_model=ResponseWithHeaders[TaskSchema])
@pass_headers
async def create_task(request: Request,
                      task_create_request: TaskCreateRequest,
                      rep: Annotated[Repository, Depends(get_repository)]) -> TaskSchema:
    task_schema_dict = task_create_request.model_dump()
    task_schema_dict = {**task_schema_dict, 'created_at': datetime.datetime.now(), 'id': None}
    task_schema = TaskSchema(
        **task_schema_dict
    )
    task_schema = await rep.create_task(task_schema)
    return task_schema


@router.get('/{id_}', response_model=ResponseWithHeaders[TaskSchema])
@pass_headers
async def get_task(request: Request, id_: int, rep: Annotated[Repository, Depends(get_repository)]) -> TaskSchema:
    task = await rep.get_task(id_)
    return TaskSchema(**task.__dict__)


@router.post('/done/{task_id}', response_model=ResponseWithHeaders[TaskSchema])
@pass_headers
async def done_task(request: Request,
                    task_id: int,
                    rep: Annotated[Repository, Depends(get_repository)]) -> TaskSchema:
    return await rep.getting_done(task_id)


@router.post('/undone/{task_id}', response_model=ResponseWithHeaders[TaskSchema])
@pass_headers
async def undone_task(request: Request,
                      task_id: int,
                      rep: Annotated[Repository, Depends(get_repository)]) -> TaskSchema:
    return await rep.getting_done(task_id, done=False)


@router.delete('/{id_}')
@pass_headers
async def delete_task(request: Request, id_: int, rep: Annotated[Repository, Depends(get_repository)]):
    await rep.delete_task(id_)


@router.get('/projects/', response_model=ResponseWithHeaders[list[ProjectSchema]],
            response_class=get_response_class('project_list.html'))
@pass_headers
async def get_projects(request: Request, rep: Annotated[Repository, Depends(get_repository)]) -> list[ProjectSchema]:
    all_projects = await rep.get_projects()
    return all_projects


@router.get('/projects/{id_}', response_model=ResponseWithHeaders[ProjectSchema])
@pass_headers
async def get_project(request: Request,
                      id_: int,
                      rep: Annotated[Repository, Depends(get_repository)]) -> ProjectByIdResponse:
    project = await rep.get_project(id_)
    tasks = await rep.get_tasks_by_project_id(id_)
    return ProjectByIdResponse(**project.__dict__, tasks=tasks)


@router.get('/tasks-by-project/{id_}',
            response_model=ResponseWithHeaders[list[TaskSchema]],
            response_class=get_response_class('task_list.html'))
@pass_headers
async def get_tasks_by_project(request: Request,
                               id_: int,
                               rep: Annotated[Repository, Depends(get_repository)]) -> list[TaskSchema]:
    tasks = await rep.get_tasks_by_project_id(id_)
    return tasks


@router.post('/projects', response_model=ResponseWithHeaders[ProjectSchema])
@pass_headers
async def create_project(request: Request,
                         project_create_request: ProjectCreateRequest,
                         rep: Annotated[Repository, Depends(get_repository)]) -> ProjectSchema:
    project_schema_dict = project_create_request.model_dump()
    project_schema_dict = {**project_schema_dict, 'id': None}
    project_schema = ProjectSchema(
        **project_schema_dict
    )
    project_schema = await rep.create_project(project_schema)
    return project_schema


@router.delete('/projects/{id_}')
async def delete_project(id_: int, rep: Annotated[Repository, Depends(get_repository)]):
    await rep.delete_project(id_)


@router.post('/projects/{task_id}/{project_id}')
async def attach_project_to_task(task_id: int, project_id: int, rep: Annotated[Repository, Depends(get_repository)]):
    await rep.attach_project_task(task_id, project_id)


@router.get('/tags/', response_model=ResponseWithHeaders[list[TagSchema]])
@pass_headers
async def get_tags(request: Request, rep: Annotated[Repository, Depends(get_repository)]) -> list[TagSchema]:
    all_tags = await rep.get_tags()
    return all_tags


@router.get('/tags/{id_}', response_model=ResponseWithHeaders[TagSchema])
@pass_headers
async def get_tag(request: Request, id_: int, rep: Annotated[Repository, Depends(get_repository)]) -> TagResponse:
    tag = await rep.get_tag(id_)
    tasks = await rep.get_tasks_by_tag_id(id_)

    return TagResponse(**tag.__dict__, tasks=tasks)


@router.post('/tags', response_model=ResponseWithHeaders[TagSchema])
@pass_headers
async def create_tag(request: Request, tag: str, rep: Annotated[Repository, Depends(get_repository)]) -> TagSchema:
    tag = await rep.create_tag(tag)
    return tag


@router.post('/tags/{task_id}/{tag_id}')
async def attach_task_to_tag(task_id: int, tag_id: int, rep: Annotated[Repository, Depends(get_repository)]):
    await rep.attach_task_to_tag(task_id, tag_id)


@router.delete('/tags/{id}')
async def delete_tag(id: int, rep: Annotated[Repository, Depends(get_repository)]):
    await rep.delete_tag(id)
