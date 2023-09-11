from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import sessionmaker

from app.dependencies import has_query_params, get_repository

router = APIRouter(
    prefix='/users', tags=['users'], dependencies=[Depends(has_query_params)],
)


@router.get('/')
async def get_users(async_session: Annotated[sessionmaker, Depends(get_repository)]):

    return {}
