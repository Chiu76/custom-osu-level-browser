from sqlalchemy import Select, Subquery, select, func

from .schemas.identifiers import GroupingTypeIdentifier
from .schemas.requests import GroupingQueryRequest

from src.beatmap_query.repositories import BeatmapQueryRepository

from src.common.models.collections import CollectionItem


def get_aggregated_count_sq(request: GroupingQueryRequest) -> Subquery:
    beatmap_query_stmt = BeatmapQueryRepository.get_beatmap_query_stmt(
        request.beatmap_query_request.core_specs, 
        request.beatmap_query_request.presentation_specs,
    )

    if request.grouping_type == GroupingTypeIdentifier.COLLECTIONS:
        aggregated_count_sq = get_aggregated_count_sq__collections(beatmap_query_stmt)
    
    return aggregated_count_sq


def get_aggregated_count_sq__collections(beatmap_query_stmt: Select) -> Subquery:
    # to get inner FROM content of beatmap_query_stmt which contains the core_stmt_sq
    core_stmt_sq = beatmap_query_stmt.get_final_froms()[0]
    beatmap_query_sq = ( 
        beatmap_query_stmt
            .add_columns(CollectionItem.collection_id)
            .join(CollectionItem, core_stmt_sq.c.beatmap_db_id == CollectionItem.beatmap_db_id)
            .subquery('beatmap_query_sq')
    )

    total_count_sq = (
        select(CollectionItem.collection_id, func.count().label('count'))
        .group_by(CollectionItem.collection_id)
        .subquery('total_count_sq')
    )
    selected_count_sq = (
        select(beatmap_query_sq.c.collection_id, func.count().label('count'))
        .select_from(beatmap_query_sq)
        .group_by(beatmap_query_sq.c.collection_id)
        .subquery('selected_count_sq')
    )

    aggregated_count_sq = (
        select(total_count_sq.c.collection_id.label('grouping_id'), total_count_sq.c.count.label('total_count'), func.coalesce(selected_count_sq.c.count, 0).label('selected_count'))
        .select_from(total_count_sq)
        .outerjoin(selected_count_sq, selected_count_sq.c.collection_id == total_count_sq.c.collection_id)
        .subquery('aggregated_count_sq')
    )   

    return aggregated_count_sq
