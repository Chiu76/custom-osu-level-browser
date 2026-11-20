from sqlalchemy import Select, Subquery, select, func, and_, case, cast, String
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.models.beatmaps import Beatmap
from src.common.models.collections import Collection

from .schemas import GroupingQueryRequest, GroupingQueryRow
from .enums import GroupingTypeEnum

from .yyy_field_groupings import get_artist_grouping_sq, get_overall_difficulty_grouping_sq, get_ranked_year_grouping_sq

import src.api.grouping_query.zzz_aggregated_count as zzz_aggregated_count
import src.api.grouping_query.zzz_grouping_query as zzz_grouping_query


class GroupingQueryRepository:
    @classmethod
    async def query(cls, request: GroupingQueryRequest, session: AsyncSession) -> list[GroupingQueryRow]:
        grouping_query_stmt = zzz_grouping_query.get_grouping_query_stmt(request)
        # aggregated_count_sq = zzz_aggregated_count.get_aggregated_count_sq(request)
        
        # from src.common.db import engine
        # print(grouping_query_stmt.compile(engine))

        results = session.execute(grouping_query_stmt).mappings().all()
        
        return [GroupingQueryRow.model_validate(result) for result in results]


    # @staticmethod
    # def get_grouping_query_stmt__ranked_year(aggregated_count_sq: Subquery, request: GroupingQueryRequest) -> Select:
    #     ranked_year_sq = get_ranked_year_grouping_sq()
        
    #     grouping_query_stmt = (
    #         select(
    #             func.coalesce(request.grouping_type, request.grouping_type).label('grouping_type'),
    #             ranked_year_sq.c.grouping_id,
    #             cast(ranked_year_sq.c.bins.label('grouping_name'), String),
    #             func.coalesce(aggregated_count_sq.c.total_count, 0).label('total_count'), 
    #             func.coalesce(aggregated_count_sq.c.selected_count, 0).label('selected_count'),
    #         )
    #         .select_from(ranked_year_sq)
    #         .outerjoin(aggregated_count_sq, aggregated_count_sq.c.grouping_id == ranked_year_sq.c.grouping_id)
    #         .group_by(ranked_year_sq.c.bins)
    #         .order_by(ranked_year_sq.c.grouping_id)
    #     )

    #     return grouping_query_stmt
