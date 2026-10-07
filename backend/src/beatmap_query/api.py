from fastapi import APIRouter

from src.common.db import SessionMaker
from .repositories import BeatmapQueryRepository

from .schemas.requests import BeatmapQueryRequest, BeatmapQueryResponse


router = APIRouter()


@router.post('/api/beatmap_query/')
async def query(request: BeatmapQueryRequest) -> BeatmapQueryResponse:
    # print(request)

    with SessionMaker() as session:
        rows = await BeatmapQueryRepository.query(request, session)
        count = len(rows)
    
    return BeatmapQueryResponse(
        rows=rows,
        count=count,
    )
