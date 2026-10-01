from fastapi import APIRouter, Path

from src.common.db import SessionMaker
from .repositories import BeatmapQueryRepository

from .schemas.requests import BeatmapQueryRequest
from .schemas.identifiers import NoneIdentifier, LocalBeatmapsIdentifier
from .schemas.specs import CoreSpecs, StarRatingSpec, AttachedScoreSpec, OnlineDetailsSpec, SourceSpec, PresentationSpecs, GroupingSpec, SearchSpec, Filter, FilterSpec, Sorting, SortingSpec


router = APIRouter()


@router.post('/api/beatmap_query/')
async def query(request: BeatmapQueryRequest):
    # print(request)

    with SessionMaker() as session:
        results = await BeatmapQueryRepository.query(request, session)
    
    return results


def get_dummy_beatmap_query_request():
    core_specs = CoreSpecs(
        star_rating_spec=StarRatingSpec(),
        attached_score_spec=AttachedScoreSpec(),
        online_details_spec=OnlineDetailsSpec(),
        source_spec=LocalBeatmapsIdentifier(type='local_beatmaps'),
        filter_spec=FilterSpec(
            filters=[
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
    return BeatmapQueryRequest(core_specs=core_specs, presentation_specs=presentation_specs)
