from sqlalchemy import Select, Subquery, select, func, cast, String, alias

from src.api.beatmap_query.repositories import BeatmapQueryRepository

from .schemas import GroupingQueryRequest
from .yyy_field_groupings import get_grouping_sq


def get_grouping_query_stmt(request: GroupingQueryRequest) -> Select:
    grouping_sq = get_grouping_sq(request.grouping_type)

    stmt = (
        select(
            func.coalesce(request.grouping_type, request.grouping_type).label('grouping_type'),
            grouping_sq.c.grouping_id.label('grouping_id'),
            cast(grouping_sq.c.bins.label('grouping_name'), String),
            func.count().label('total_count'),
        )
        .select_from(grouping_sq)
        .group_by(grouping_sq.c.bins)
        .order_by(grouping_sq.c.grouping_id)
    )

    if request.show_selected_counts:
        selected_count_sq = get_selected_count_sq(request)
        stmt = (
            stmt
                .add_columns(func.coalesce(selected_count_sq.c.selected_count, 0).label('selected_count'))
                .outerjoin(selected_count_sq, selected_count_sq.c.grouping_id == grouping_sq.c.grouping_id)
        )
    else:
        stmt = stmt.add_columns(func.coalesce(0, 0).label('selected_count'))

    if request.q != "":
        print('hohoho')
        stmt = stmt.where(grouping_sq.c.bins.ilike(f'%{request.q}%'))

    return stmt


def get_selected_count_sq(request: GroupingQueryRequest) -> Subquery:
    beatmap_query_stmt = BeatmapQueryRepository.get_beatmap_query_stmt(
        request.beatmap_query_request.core_specs, 
        request.beatmap_query_request.presentation_specs,
    )

    # to get inner FROM content of beatmap_query_stmt which contains the core_sq
    core_sq = beatmap_query_stmt.get_final_froms()[0]

    # alias is required when beatmap_query_stmt already has active grouping(s)
    # so that the below outer reference to the table via join is treated as separate from the inner reference
    grouping_sq = get_grouping_sq(request.grouping_type)
    aliased_grouping_sq = alias(grouping_sq)

    beatmap_query_sq = ( 
        beatmap_query_stmt
            .add_columns(aliased_grouping_sq.c.grouping_id)
            .join(aliased_grouping_sq, core_sq.c.beatmap_db_id == aliased_grouping_sq.c.beatmap_db_id)
            .subquery('beatmap_query_sq')
    )

    selected_count_sq = (
        select(
            beatmap_query_sq.c.grouping_id.label('grouping_id'), 
            func.count().label('selected_count'),
        )
        .select_from(beatmap_query_sq)
        .group_by(beatmap_query_sq.c.grouping_id)
        .subquery('selected_count_sq')
    )

    return selected_count_sq