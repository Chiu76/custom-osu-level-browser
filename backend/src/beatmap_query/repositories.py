from sqlalchemy import Select, Subquery, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.models.beatmaps import Beatmap, BeatmapSet
from src.common.models.collections import CollectionItem 

from .schemas.identifiers import NoneIdentifier, LocalBeatmapsIdentifier, GroupingTypeIdentifier
from .schemas.requests import BeatmapQueryRequest, BeatmapQueryRow, BeatmapQueryResponse
from .schemas.specs import CoreSpecs, StarRatingSpec, AttachedScoreSpec, OnlineDetailsSpec, SourceSpec, PresentationSpecs, GroupingSpec, SearchSpec, Filter, FilterSpec, Sorting, SortingSpec


import src.beatmap_query.zzz_core as zzz_core
import src.beatmap_query.zzz_presentation as zzz_presentation
import src.beatmap_query.zzz_count as zzz_count


class BeatmapQueryRepository:
    @classmethod
    async def query(cls, request: BeatmapQueryRequest, session: AsyncSession) -> list[BeatmapQueryRow]:
        beatmap_query_stmt = cls.get_beatmap_query_stmt(request.core_specs, request.presentation_specs)

        beatmap_query_stmt = beatmap_query_stmt.limit(500)
        # print(beatmap_query_stmt)

        results = session.execute(beatmap_query_stmt).mappings().all()

        return [BeatmapQueryRow.model_validate(dict(result)) for result in results]
    

    @classmethod
    async def query_agg_count(
        cls, 
        grouping_type: GroupingTypeIdentifier, 
        request: BeatmapQueryRequest, 
        session: AsyncSession
    ) -> list[set[int, int, int]]:
        beatmap_query_stmt = cls.get_beatmap_query_stmt(request.core_specs, request.presentation_specs)

        if grouping_type == GroupingTypeIdentifier.COLLECTIONS:
            agg_count_stmt = zzz_count.get_agg_count_stmt__collections(beatmap_query_stmt)
        
        results = session.execute(agg_count_stmt).all()
        ## todo: have a response model, AggregatedCountResponse, grouping type and list of AggregatedCountRow, collection_id selected_count full_count
        return results


    @classmethod
    def get_beatmap_query_stmt(cls, core_specs: CoreSpecs, presentation_specs: PresentationSpecs) -> Select:
        initial_stmt = cls.get_initial_stmt()
        core_stmt = zzz_core.apply_core_specs(initial_stmt, core_specs)
        beatmap_query_stmt = zzz_presentation.apply_presentation_specs(core_stmt, presentation_specs)

        return beatmap_query_stmt


    @staticmethod
    def get_initial_stmt() -> Select:
        stmt = (
            select(
                Beatmap.id.label('beatmap_db_id'),
                Beatmap.beatmap_id,
                Beatmap.beatmap_set_id,
                Beatmap.md5_hash,
                Beatmap.mode,
                Beatmap.bpm,
                Beatmap.difficulty_name,
                Beatmap.ranked_status,
                Beatmap.num_hitcircles,
                Beatmap.num_sliders,
                Beatmap.num_spinners,
                Beatmap.approach_rate,
                Beatmap.overall_difficulty,
                Beatmap.circle_size,
                Beatmap.hp_drain,
                Beatmap.last_played,
                Beatmap.drain_time,
                Beatmap.total_time,
                Beatmap.local_offset,

                BeatmapSet.artist,
                BeatmapSet.title,
                BeatmapSet.owner,
                BeatmapSet.song_source,
                BeatmapSet.song_tags,
            )
            .select_from(Beatmap)
            .join(BeatmapSet, BeatmapSet.beatmap_set_id == Beatmap.beatmap_set_id)
        )

        return stmt

    def generate_dummy_beatmap_query_request():
        core_specs = CoreSpecs(
            star_rating_spec=StarRatingSpec(),
            attached_score_spec=AttachedScoreSpec(),
            online_details_spec=OnlineDetailsSpec(),
            source_spec=LocalBeatmapsIdentifier(type='local_beatmaps'),
            filter_spec=FilterSpec(
                filters=[
                    Filter(field='owner', op='=', value='monstrata'),
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
