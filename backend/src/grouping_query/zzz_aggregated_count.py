from sqlalchemy import Select, Subquery, select, func, alias

from .enums import GroupingTypeEnum
from .schemas import GroupingQueryRequest

from .yyy_field_groupings import get_artist_grouping_sq, get_overall_difficulty_grouping_sq

from src.beatmap_query.repositories import BeatmapQueryRepository

from src.common.models.collections import CollectionItem


def get_aggregated_count_sq(request: GroupingQueryRequest) -> Subquery:
    beatmap_query_stmt = BeatmapQueryRepository.get_beatmap_query_stmt(
        request.beatmap_query_request.core_specs, 
        request.beatmap_query_request.presentation_specs,
    )

    if request.grouping_type == GroupingTypeEnum.COLLECTIONS:
        aggregated_count_sq = get_aggregated_count_sq__collections(beatmap_query_stmt)
    
    elif request.grouping_type == GroupingTypeEnum.ARTIST:
        aggregated_count_sq = get_aggregated_count_sq__artist(beatmap_query_stmt)
    
    elif request.grouping_type == GroupingTypeEnum.OVERALL_DIFFICULTY:
        aggregated_count_sq = get_aggregated_count_sq__overall_difficulty(beatmap_query_stmt)
    
    return aggregated_count_sq


def get_aggregated_count_sq__artist(beatmap_query_stmt: Select) -> Subquery:
    artist_grouping_sq = get_artist_grouping_sq()

    total_count_sq = (
        select(artist_grouping_sq.c.grouping_id, func.count().label('count'))
        .group_by(artist_grouping_sq.c.grouping_id)
        .subquery('total_count_sq')
    )

    # to get inner FROM content of beatmap_query_stmt which contains the core_sq
    core_sq = beatmap_query_stmt.get_final_froms()[0]
    # alias is required when beatmap_query_stmt already uses CollectionItem (ie a collection grouping is active)
    # so that the below outer reference to the table via join is treated as separate from the inner reference
    aliased_artist_grouping = alias(artist_grouping_sq)
    beatmap_query_sq = ( 
        beatmap_query_stmt
            .add_columns(aliased_artist_grouping.c.grouping_id)
            .join(aliased_artist_grouping, core_sq.c.beatmap_db_id == aliased_artist_grouping.c.beatmap_db_id)
            .subquery('beatmap_query_sq')
    )

    selected_count_sq = (
        select(beatmap_query_sq.c.grouping_id, func.count().label('count'))
        .select_from(beatmap_query_sq)
        .group_by(beatmap_query_sq.c.grouping_id)
        .subquery('selected_count_sq')
    )

    aggregated_count_sq = (
        select(
            total_count_sq.c.grouping_id.label('grouping_id'), 
            total_count_sq.c.count.label('total_count'), 
            func.coalesce(selected_count_sq.c.count, 0).label('selected_count'),
        )
        .select_from(total_count_sq)
        .outerjoin(selected_count_sq, selected_count_sq.c.grouping_id == total_count_sq.c.grouping_id)
        .subquery('aggregated_count_sq')
    )

    return aggregated_count_sq


def get_aggregated_count_sq__overall_difficulty(beatmap_query_stmt: Select) -> Subquery:
    overall_difficulty_sq = get_overall_difficulty_grouping_sq()

    total_count_sq = (
        select(overall_difficulty_sq.c.grouping_id, func.count().label('count'))
        .group_by(overall_difficulty_sq.c.grouping_id)
        .subquery('total_count_sq')
    )

    # to get inner FROM content of beatmap_query_stmt which contains the core_sq
    core_sq = beatmap_query_stmt.get_final_froms()[0]
    # alias is required when beatmap_query_stmt already uses CollectionItem (ie a collection grouping is active)
    # so that the below outer reference to the table via join is treated as separate from the inner reference
    aliased_overall_difficulty_grouping = alias(overall_difficulty_sq)
    beatmap_query_sq = ( 
        beatmap_query_stmt
            .add_columns(aliased_overall_difficulty_grouping.c.grouping_id)
            .join(aliased_overall_difficulty_grouping, core_sq.c.beatmap_db_id == aliased_overall_difficulty_grouping.c.beatmap_db_id)
            .subquery('beatmap_query_sq')
    )

    selected_count_sq = (
        select(beatmap_query_sq.c.grouping_id, func.count().label('count'))
        .select_from(beatmap_query_sq)
        .group_by(beatmap_query_sq.c.grouping_id)
        .subquery('selected_count_sq')
    )

    aggregated_count_sq = (
        select(
            total_count_sq.c.grouping_id.label('grouping_id'), 
            total_count_sq.c.count.label('total_count'), 
            func.coalesce(selected_count_sq.c.count, 0).label('selected_count'),
        )
        .select_from(total_count_sq)
        .outerjoin(selected_count_sq, selected_count_sq.c.grouping_id == total_count_sq.c.grouping_id)
        .subquery('aggregated_count_sq')
    )

    return aggregated_count_sq


def get_aggregated_count_sq__collections(beatmap_query_stmt: Select) -> Subquery:
    total_count_sq = (
        select(CollectionItem.collection_id, func.count().label('count'))
        .group_by(CollectionItem.collection_id)
        .subquery('total_count_sq')
    )
    
    # to get inner FROM content of beatmap_query_stmt which contains the core_sq
    core_sq = beatmap_query_stmt.get_final_froms()[0]
    # alias is required when beatmap_query_stmt already uses CollectionItem (ie a collection grouping is active)
    # so that the below outer reference to the table via join is treated as separate from the inner reference
    aliased_collection_item = alias(CollectionItem)
    beatmap_query_sq = ( 
        beatmap_query_stmt
            .add_columns(aliased_collection_item.c.collection_id)
            .join(aliased_collection_item, core_sq.c.beatmap_db_id == aliased_collection_item.c.beatmap_db_id)
            .subquery('beatmap_query_sq')
    )

    selected_count_sq = (
        select(beatmap_query_sq.c.collection_id, func.count().label('count'))
        .select_from(beatmap_query_sq)
        .group_by(beatmap_query_sq.c.collection_id)
        .subquery('selected_count_sq')
    )

    aggregated_count_sq = (
        select(
            total_count_sq.c.collection_id.label('grouping_id'), 
            total_count_sq.c.count.label('total_count'), 
            func.coalesce(selected_count_sq.c.count, 0).label('selected_count'),
        )
        .select_from(total_count_sq)
        .outerjoin(selected_count_sq, selected_count_sq.c.collection_id == total_count_sq.c.collection_id)
        .subquery('aggregated_count_sq')
    )

    return aggregated_count_sq
