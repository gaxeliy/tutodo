from fastapi import HTTPException

from app.database import async_session


async def has_query_params(q: str | None = None):
    if q is None:
        raise HTTPException(status_code=400, detail='Invalid query')


def get_repository():
    from app.tasks.use_cases import Repository

    return Repository(async_session)


