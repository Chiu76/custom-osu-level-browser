from fastapi import APIRouter, Path

from src.common.db import SessionMaker
from .repositories import QueryRepository

from .schemas.requests import BeatmapQueryRequest
from .schemas.identifiers import NoneIdentifier, LocalBeatmapsIdentifier
from .schemas.specs import CoreSpecs, StarRatingSpec, AttachedScoreSpec, OnlineDetailsSpec, SourceSpec, PresentationSpecs, GroupingSpec, SearchSpec, Filter, FilterSpec, Sorting, SortingSpec


router = APIRouter(prefix='/api/beatmaps')


@router.get('/query/')
async def query():
    core_specs = CoreSpecs(
        star_rating_spec=StarRatingSpec(),
        attached_score_spec=AttachedScoreSpec(),
        online_details_spec=OnlineDetailsSpec(),
        source_spec=LocalBeatmapsIdentifier(type='local_beatmaps'),
        filter_spec=FilterSpec(
            filters=[
                Filter(field='owner', op='=', value='monstrata'),
                Filter(field='bpm', op='>', value='65'),
            ]
        ),
    )
    presentation_specs = PresentationSpecs(
        search_spec=SearchSpec(),
        grouping_spec=NoneIdentifier(type='none'),
        sorting_spec=SortingSpec(
            sortings=[
                Sorting(field='beatmap_set_id', dir='asc'),
            ]
        ),
    )
    request = BeatmapQueryRequest(core_specs=core_specs, presentation_specs=presentation_specs)
    
    with SessionMaker() as session:
        results = await QueryRepository.query(request, session)
    
    return results
