from fastapi import APIRouter

from src.common.db import SessionMaker
from .repositories import GroupingQueryRepository

from .schemas.requests import GroupingQueryRequest, GroupingQueryResponse


router = APIRouter()


@router.post('/api/grouping_query')
async def query(request: GroupingQueryRequest) -> GroupingQueryResponse:
    with SessionMaker() as session:
        rows = await GroupingQueryRepository.query(request, session)

    return GroupingQueryResponse(
        rows=rows,
        grouping_type=request.grouping_type,
    )
