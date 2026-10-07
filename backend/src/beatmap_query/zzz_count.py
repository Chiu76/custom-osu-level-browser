from sqlalchemy import Select, Subquery, select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.models.beatmaps import Beatmap, BeatmapSet
from src.common.models.collections import CollectionItem 


def get_agg_count_stmt__collections(beatmap_query_stmt: Select):
    # to get inner FROM content of beatmap_query_stmt which contains the core_stmt_sq
    core_stmt_sq = beatmap_query_stmt.get_final_froms()[0]
    beatmap_query_sq = ( 
        beatmap_query_stmt
            .add_columns(CollectionItem.collection_id)
            .join(CollectionItem, core_stmt_sq.c.beatmap_db_id == CollectionItem.beatmap_db_id)
            .subquery('beatmap_query_sq')
    )

    full_count_sq = (
        select(CollectionItem.collection_id, func.count().label('count'))
        .group_by(CollectionItem.collection_id)
        .subquery('full_count_sq')
    )
    selected_count_sq = (
        select(beatmap_query_sq.c.collection_id, func.count().label('count'))
        .select_from(beatmap_query_sq)
        .group_by(beatmap_query_sq.c.collection_id)
        .subquery('selected_count_sq')
    )

    agg_count_stmt = (
        select(full_count_sq.c.collection_id, func.coalesce(selected_count_sq.c.count, 0), full_count_sq.c.count)
        .select_from(full_count_sq)
        .outerjoin(selected_count_sq, selected_count_sq.c.collection_id == full_count_sq.c.collection_id)
    )

    return agg_count_stmt