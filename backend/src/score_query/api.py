from fastapi import APIRouter

from src.common.db import SessionMaker
from .repositories import ScoreQueryRepository

from .schemas.requests import ScoreQueryRequest, ScoreQueryResponse


router = APIRouter()


@router.post('/api/score_query')
async def query(request: ScoreQueryRequest) -> ScoreQueryResponse:
    with SessionMaker() as session:
        rows = await ScoreQueryRepository.query(request, session)

    return ScoreQueryResponse(
        rows=rows,
        grouping_type=request.grouping_type,
    )
