from sqlalchemy import select, insert, update, delete

from app.tasks.models import Task, Project, Tag, TaskTag
from app.tasks.serializers import TaskSchema, ProjectSchema, TagSchema


class Repository:
    def __init__(self, async_session):
        self.async_session = async_session

    async def get_tasks(self) -> list[TaskSchema]:
        async with self.async_session() as session:
            query = select(Task)
            query_result = (await session.execute(query)).scalars().all()

            return [TaskSchema.model_validate(task) for task in query_result]

    async def get_task(self, id: int) -> TaskSchema:
        async with self.async_session() as session:
            query = select(Task).where(Task.id == id)
            query_result = (await session.execute(query)).scalars().first()

            task = TaskSchema.model_validate(query_result)
            task.tags = await self.get_all_tags_by_task(task.id)

            return task

    async def get_tasks_by_project_id(self, id: int) -> list[TaskSchema]:
        async with self.async_session() as session:
            query = select(Task).where(Task.project_id == id)
            query_result = (await session.execute(query)).scalars().all()

            return [TaskSchema.model_validate(task) for task in query_result]

    async def get_tasks_by_tag_id(self, id: int) -> list[TaskSchema]:
        async with self.async_session() as session:
            query = select(Task).join(TaskTag).where(TaskTag.tag_id == id)
            query_result = (await session.execute(query)).scalars().all()

            return [TaskSchema.model_validate(task) for task in query_result]

    async def create_task(self, task: TaskSchema) -> TaskSchema:
        async with self.async_session() as session:
            query = insert(Task).values(
                title=task.title,
                description=task.description,
                done=task.done,
                created_at=task.created_at,
                scheduled_at=task.scheduled_at,
                my_day_date=task.my_day_date,
            ).returning(Task)
            query_result = (await session.execute(query)).scalars().first()
            await session.commit()
            result = TaskSchema.model_validate(query_result)
            return result

    async def delete_task(self, id: int):
        async with self.async_session() as session:
            query = delete(Task).where(Task.id == id)
            await session.execute(query)
            await session.commit()

    async def getting_done(self, id: int, done=True) -> TaskSchema:
        async with self.async_session() as session:
            query = update(Task).where(Task.id == id).values(done=done).returning(Task)
            query_result = (await session.execute(query)).scalars().first()
            result = TaskSchema.model_validate(query_result)
            await session.commit()
            return result

    async def get_projects(self) -> list[ProjectSchema]:
        async with self.async_session() as session:
            query = select(Project)
            query_result = (await session.execute(query)).scalars().all()

            return [ProjectSchema.model_validate(project) for project in query_result]

    async def get_project(self, id: int, ) -> ProjectSchema:
        async with self.async_session() as session:
            query = select(Project).where(Project.id == id)
            query_result = (await session.execute(query)).scalars().first()

            return ProjectSchema.model_validate(query_result)

    async def create_project(self, project: ProjectSchema) -> ProjectSchema:
        async with self.async_session() as session:
            query = insert(Project).values(
                title=project.title,
                description=project.description,
            ).returning(Project)
            query_result = (await session.execute(query)).scalars().first()
            await session.commit()
            result = ProjectSchema.model_validate(query_result)
            return result

    async def delete_project(self, id: int):
        async with self.async_session() as session:
            query = delete(Project).where(Project.id == id)
            await session.execute(query)
            await session.commit()

    async def attach_project_task(self, task_id: int, project_id: int) -> TaskSchema:
        async with self.async_session() as session:
            query = update(Task).where(Task.id == task_id).values(project_id=project_id).returning(Task)
            query_result = (await session.execute(query)).scalars().first()
            result = TaskSchema.model_validate(query_result)
            await session.commit()
            return result

    async def get_tags(self) -> list[TagSchema]:
        async with self.async_session() as session:
            query = select(Tag)
            query_result = (await session.execute(query)).scalars().all()

            return [TagSchema.model_validate(tag) for tag in query_result]

    async def get_tag(self, id: int) -> TagSchema:
        async with self.async_session() as session:
            query = select(Tag).where(Tag.id == id)
            query_result = (await session.execute(query)).scalars().first()

            return TagSchema.model_validate(query_result)

    async def get_all_tags_by_task(self, id: int) -> list[TagSchema]:
        async with self.async_session() as session:
            query = select(Tag).join(TaskTag).where(TaskTag.task_id == id)
            query_result = (await session.execute(query)).scalars().all()

            return [TagSchema.model_validate(tag) for tag in query_result]

    async def create_tag(self, tag: str) -> TagSchema:
        async with self.async_session() as session:
            query = insert(Tag).values(
                title=tag,
                description=tag,
            ).returning(Tag)
            query_result = (await session.execute(query)).scalars().first()
            await session.commit()
            result = TagSchema.model_validate(query_result)
            return result

    async def delete_tag(self, id: int):
        async with self.async_session() as session:
            query = delete(Tag).where(Tag.id == id)
            await session.execute(query)
            await session.commit()

    async def attach_task_to_tag(self, task_id: int, tag_id: int):
        async with self.async_session() as session:
            query = insert(TaskTag).values(
                task_id=task_id,
                tag_id=tag_id,
            )
            await session.execute(query)
            await session.commit()
