import json

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.models.beatmaps import Beatmap, BeatmapSet

from .schemas.requests import BeatmapQueryRequest, BeatmapQueryResult
from .schemas.specs import CoreSpecs, PresentationSpecs

import src.query.core as core
import src.query.presentation as presentation


class QueryRepository:
    @classmethod
    async def query(cls, request: BeatmapQueryRequest, session: AsyncSession):
        beatmap_query_stmt = cls.get_beatmap_query_stmt(request.core_specs, request.presentation_specs)

        beatmap_query_stmt = beatmap_query_stmt.limit(50)
        print(beatmap_query_stmt)

        results = session.execute(beatmap_query_stmt).mappings().all()     

        return [BeatmapQueryResult.model_validate(dict(result)) for result in results]


    @classmethod
    def get_beatmap_query_stmt(cls, core_specs: CoreSpecs, presentation_specs: PresentationSpecs):
        initial_stmt = cls.get_initial_stmt()
        core_stmt = core.apply_core_specs(initial_stmt, core_specs)
        beatmap_query_stmt = presentation.apply_presentation_specs(core_stmt, presentation_specs)

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
