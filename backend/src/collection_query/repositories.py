from sqlalchemy import Select, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.models.collections import Collection

from .schemas.requests import CollectionQueryRow

from src.beatmap_query.repositories import BeatmapQueryRepository


class CollectionQueryRepository:
    @classmethod
    async def query(cls, q: str, session: AsyncSession) -> CollectionQueryRow:
        aggregated_count_sq = await BeatmapQueryRepository.get_aggregated_count_sq(
            grouping_type='collections', 
            request=BeatmapQueryRepository.generate_dummy_beatmap_query_request(), 
        )

        select_collections_stmt = (
            select(
                Collection.id.label('collection_id'), 
                Collection.name.label('name'), 
                aggregated_count_sq.c.total_count, 
                aggregated_count_sq.c.selected_count
            )
            .select_from(Collection)
            .join(aggregated_count_sq, aggregated_count_sq.c.grouping_id == Collection.id)
            .where(Collection.name.ilike(f'%{q}%'))
        )
        
        results = session.execute(select_collections_stmt).mappings().all()
        
        return [CollectionQueryRow.model_validate(result) for result in results]
