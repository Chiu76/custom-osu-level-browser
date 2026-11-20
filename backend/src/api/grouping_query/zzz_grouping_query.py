from sqlalchemy import Select, Subquery, select, func, and_, case, cast, String

from src.common.models.collections import Collection

from .schemas import GroupingQueryRequest
from .enums import GroupingTypeEnum

import src.api.grouping_query.yyy_field_groupings as yyy_field_groupings


def get_grouping_query_stmt(request: GroupingQueryRequest) -> Select:
    grouping_sq = get_grouping_sq(request)

    grouping_query_stmt = (
        select(
            func.coalesce(request.grouping_type, request.grouping_type).label('grouping_type'),
            grouping_sq.c.grouping_id,
            cast(grouping_sq.c.bins.label('grouping_name'), String),
            func.count().label('total_count'),
        )
        .select_from(grouping_sq)
        .group_by(grouping_sq.c.bins)
        .order_by(grouping_sq.c.grouping_id)
    )

    return grouping_query_stmt

## todo: use this or something like this in beatmap_query grouping and source selection
def get_grouping_sq(request: GroupingQueryRequest):
    if request.grouping_type == GroupingTypeEnum.COLLECTIONS:
        grouping_sq = yyy_field_groupings.get_collections_grouping_sq()
    
    elif request.grouping_type == GroupingTypeEnum.ARTIST:
        grouping_sq = yyy_field_groupings.get_artist_grouping_sq()
    
    elif request.grouping_type == GroupingTypeEnum.OVERALL_DIFFICULTY:
        grouping_sq = yyy_field_groupings.get_overall_difficulty_grouping_sq()

    elif request.grouping_type == GroupingTypeEnum.RANKED_YEAR:
        grouping_sq = yyy_field_groupings.get_ranked_year_grouping_sq()
    
    elif request.grouping_type == GroupingTypeEnum.RANKED_MONTH:
        grouping_sq = yyy_field_groupings.get_ranked_month_grouping_sq()

    return grouping_sq