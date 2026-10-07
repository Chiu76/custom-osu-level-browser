from fastapi import APIRouter

from src.common.db import SessionMaker
from .repositories import CollectionsRepository

# from .schemas.requests import BeatmapQueryRequest
# from .schemas.identifiers import NoneIdentifier, LocalBeatmapsIdentifier
# from .schemas.specs import CoreSpecs, StarRatingSpec, AttachedScoreSpec, OnlineDetailsSpec, SourceSpec, PresentationSpecs, GroupingSpec, SearchSpec, Filter, FilterSpec, Sorting, SortingSpec


router = APIRouter()


@router.get('/api/collections')
async def collections(q: str):
    with SessionMaker() as session:
        results = await CollectionsRepository.collections(q, session)
    
    return results
