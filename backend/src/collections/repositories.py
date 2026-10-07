from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.models.beatmaps import Beatmap, BeatmapSet

# from .schemas.requests import CollectionsRequest, CollectionsResult
# from .schemas.specs import CoreSpecs, PresentationSpecs

from src.beatmap_query.repositories import BeatmapQueryRepository
import src.beatmap_query.zzz_presentation as zzz_presentation


class CollectionsRepository:
    @classmethod
    async def collections(cls, q: str, session: AsyncSession):
        grouping_type = 'collections'
        request = BeatmapQueryRepository.generate_dummy_beatmap_query_request()
        agg_count = await BeatmapQueryRepository.query_agg_count(grouping_type, request, session)
        print(type(agg_count))
        print(agg_count)
        # return { 'agg_count': agg_count }
    
        # beatmap_query_stmt = cls.get_beatmap_query_stmt(request.core_specs, request.presentation_specs)

        # beatmap_query_stmt = beatmap_query_stmt.limit(500)
        # print(beatmap_query_stmt)

        # results = session.execute(beatmap_query_stmt).mappings().all()     

        # return [BeatmapQueryResult.model_validate(dict(result)) for result in results]
