from fastapi import APIRouter

from src.common.db import SessionMaker
from .repositories import CollectionQueryRepository

from .schemas.requests import CollectionQueryResponse


router = APIRouter()


@router.get('/api/collection_query')
async def query(q: str = '') -> CollectionQueryResponse:
    with SessionMaker() as session:
        rows = await CollectionQueryRepository.query(q, session)
    
    return CollectionQueryResponse(
        rows=rows,
    )
