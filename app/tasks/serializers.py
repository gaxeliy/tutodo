import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.helpers import ModelConfig


class TagSchema(BaseModel, ModelConfig):
    id: Optional[int]
    title: str
    description: str


class TaskSchema(BaseModel, ModelConfig):
    id: Optional[int]
    title: str
    description: str
    done: bool
    created_at: datetime.datetime
    scheduled_at: Optional[datetime.datetime]
    my_day_date: Optional[datetime.date]
    project_id: Optional[int] = None
    tags: list[TagSchema] = []


class TagResponse(BaseModel):
    id: int
    title: str
    description: str
    tasks: list[TaskSchema] = []


class TaskCreateRequest(BaseModel):
    title: str
    description: str
    done: bool
    scheduled_at: Optional[datetime.datetime]
    my_day_date: Optional[datetime.date]

class ProjectSchema(BaseModel, ModelConfig):
    id: Optional[int]
    title: str
    description: str

class ProjectCreateRequest(BaseModel):
    title: str
    description: str


class ProjectByIdResponse(BaseModel, ModelConfig):
    id: int
    title: str
    description: str
    tasks: list[TaskSchema]
